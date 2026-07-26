# 11 - AWS Provider Basics

Terraform supports many cloud platforms through **providers**.

A **provider** is a plugin that allows Terraform to communicate with a specific platform or service.

For AWS, Terraform uses the **AWS Provider**.

```text id="n4k7pv"
Terraform
      │
      ▼
AWS Provider
      │
      ▼
AWS Services
(EC2, VPC, S3, IAM...)
```

Without a provider, Terraform does not know how to create or manage AWS resources.

---

# Why Do We Need a Provider?

Imagine writing this Terraform resource:

```hcl
resource "aws_instance" "web" {
}
```

Terraform understands the syntax, but it does not know how to communicate with AWS.

The AWS Provider translates Terraform configuration into AWS API requests.

```text id="m8w3zt"
Terraform Code
      │
      ▼
AWS Provider
      │
      ▼
AWS API
      │
      ▼
AWS Resources
```

---

# Installing the AWS Provider

Terraform downloads providers automatically during initialization.

Example:

```hcl
terraform {

  required_providers {

    aws = {

      source  = "hashicorp/aws"

      version = "~> 6.0"
    }
  }
}
```

Explanation:

```text id="h2v9yx"
source  → Provider location
version → Provider version
```

---

# Configure the Provider

After declaring the provider, configure it.

Example:

```hcl
provider "aws" {

  region = var.aws_region
}
```

Terraform now knows which AWS Region to use.

---

# AWS Regions

AWS has data centers around the world.

Examples:

```text id="t7p4nh"
us-east-1
us-west-2
eu-west-1
eu-central-1
ap-southeast-1
```

Example:

```hcl
provider "aws" {

  region = "us-east-1"
}
```

Or better:

```hcl
provider "aws" {

  region = var.aws_region
}
```

---

# Using Variables

Instead of hardcoding the Region:

```hcl
provider "aws" {

  region = var.aws_region
}
```

variables.tf

```hcl
variable "aws_region" {

  type = string

  default = "us-east-1"
}
```

This makes the configuration reusable.

---

# AWS Credentials

Terraform needs permission to manage AWS resources.

The AWS Provider uses AWS credentials.

Typical credentials include:

```text id="d6q8rx"
Access Key ID
Secret Access Key
```

The safest approach is to provide credentials through environment variables.

Example:

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"

export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"

export AWS_DEFAULT_REGION="us-east-1"
```

Terraform automatically detects these variables.

---

# Provider Authentication

The authentication process looks like this:

```text id="p5m1wa"
Terraform
      │
Reads Credentials
      │
      ▼
AWS Provider
      │
      ▼
AWS API
      │
      ▼
AWS Account
```

If the credentials are valid, Terraform can create and manage resources.

---

# Initialize the Provider

Before using Terraform, initialize the project.

```bash
terraform init
```

Terraform downloads:

```text id="v9r6mk"
AWS Provider
Required plugins
Dependencies
```

Example output:

```text id="u3y8lh"
Initializing the backend...

Initializing provider plugins...

Terraform has been successfully initialized!
```

---

# Provider Lock File

After initialization, Terraform creates:

```text
.terraform.lock.hcl
```

This file stores the provider version.

It should be committed to Git.

---

# Project Structure

Example:

```text id="f2q4kp"
terraform/
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

Usually:

```text id="x8n5rd"
versions.tf → Terraform version and provider requirements

provider.tf → Provider configuration
```

---

# Provider vs Resources

Many beginners confuse these.

Provider:

```text id="z4t6wp"
Communicates with AWS
Authenticates
Sends API requests
```

Resource:

```text id="w7j2ke"
Creates EC2
Creates VPC
Creates S3 Bucket
Creates Security Groups
```

Example:

```text id="c9h5xn"
Terraform
     │
     ├── Provider
     │       │
     │       ▼
     │     AWS API
     │
     └── Resources
             │
             ▼
      EC2, VPC, S3...
```

---

# Example Provider Configuration

```hcl
terraform {

  required_providers {

    aws = {

      source  = "hashicorp/aws"

      version = "~> 6.0"
    }
  }

  required_version = ">= 1.6.0"
}

provider "aws" {

  region = var.aws_region
}
```

---

# Verify the Provider

After initialization:

```bash
terraform providers
```

Example output:

```text
Providers required by configuration:

.
└── provider[registry.terraform.io/hashicorp/aws]
```

---

# Upgrading the Provider

Download newer compatible versions:

```bash
terraform init -upgrade
```

Terraform updates the provider if allowed by the version constraint.

---

# Best Practices

```text id="k8r3ph"
Pin provider versions
Use variables for the Region
Store credentials securely
Commit .terraform.lock.hcl
Separate provider.tf and versions.tf
Run terraform init before planning
```

---

# Common Beginner Mistakes

### Hardcoding Credentials

Bad:

```hcl
provider "aws" {

  access_key = "AKIA..."

  secret_key = "SECRET..."
}
```

Never store credentials inside Terraform files.

---

### Forgetting terraform init

Bad:

```bash
terraform plan
```

before:

```bash
terraform init
```

Terraform cannot use the provider until it is initialized.

---

### Using Different Provider Versions

Without version constraints, different developers may use different provider versions.

Always pin the version.

---

### Hardcoding the Region

Bad:

```hcl
region = "us-east-1"
```

Better:

```hcl
region = var.aws_region
```

---

### Committing Secrets

Never upload:

```text
AWS Access Keys
terraform.tfvars (if it contains secrets)
.env files
```

Use:

```text
Environment variables
GitHub Secrets
AWS IAM Roles (when running on AWS)
```

---

# Useful Commands

Initialize Terraform:

```bash
terraform init
```

Show installed providers:

```bash
terraform providers
```

Upgrade providers:

```bash
terraform init -upgrade
```

Validate configuration:

```bash
terraform validate
```

Review changes:

```bash
terraform plan
```

Deploy infrastructure:

```bash
terraform apply
```

---

# Summary

```text id="j6v2me"
Provider → Connects Terraform to AWS
AWS Provider → hashicorp/aws
Region → AWS location
Credentials → Authenticate with AWS
terraform init → Downloads providers
provider.tf → Provider configuration
versions.tf → Provider requirements
```

> The AWS Provider is the bridge between Terraform and AWS, allowing Terraform to authenticate with your AWS account and manage cloud resources through the AWS API.

