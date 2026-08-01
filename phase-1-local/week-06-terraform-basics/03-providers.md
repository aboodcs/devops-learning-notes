# 03 - Terraform Providers

Terraform can manage infrastructure on many different platforms.

However, Terraform does not communicate directly with cloud providers.

Instead, it uses **Providers**.

A **Provider** is a plugin that allows Terraform to interact with a specific platform or service.

```text id="n4p7wx"
Terraform
      │
      ▼
Provider
      │
      ▼
Cloud Platform
```

Without a provider, Terraform cannot create or manage infrastructure.

---

# Why Do We Need Providers?

Imagine you want Terraform to create:

```text id="g8m2qy"
EC2 Instance
VPC
S3 Bucket
IAM User
```

Terraform understands the configuration, but it does not know how to communicate with AWS.

The provider translates Terraform code into API requests.

```text id="k5v9rn"
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

# Popular Terraform Providers

Terraform supports thousands of providers.

Some common examples include:

| Provider   | Platform                    |
| ---------- | --------------------------- |
| AWS        | Amazon Web Services         |
| Azure      | Microsoft Azure             |
| Google     | Google Cloud Platform       |
| OCI        | Oracle Cloud Infrastructure |
| Kubernetes | Kubernetes Clusters         |
| Docker     | Docker Engine               |
| Local      | Local Computer              |
| GitHub     | GitHub Repositories         |

Each provider enables Terraform to manage resources on its platform.

---

# Provider Configuration

A provider is configured using the `provider` block.

Example:

```hcl id="m7r4pv"
provider "aws" {

  region = "us-east-1"

}
```

This tells Terraform to use AWS in the `us-east-1` region.

---

# Required Providers

Terraform also needs to know which provider to download.

Example:

```hcl id="q2x8hy"
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

```text id="y6m3tk"
source  → Provider location

version → Provider version
```

---

# Provider Workflow

```text id="h9v5qm"
Terraform Code
        │
        ▼
Provider
        │
        ▼
Cloud API
        │
        ▼
Infrastructure
```

Terraform sends requests through the provider to create or manage resources.

---

# Provider Initialization

Before Terraform can use a provider, it must download it.

Run:

```bash id="w3k7rp"
terraform init
```

Terraform downloads:

```text id="p8x2mc"
Provider Plugins
Dependencies
```

Example output:

```text id="c5v9ny"
Initializing provider plugins...

Terraform has been successfully initialized!
```

---

# Provider Versions

Providers are updated regularly.

Example:

```hcl id="a7r4px"
version = "~> 6.0"
```

This allows Terraform to use compatible versions within the 6.x release.

Pinning provider versions helps keep deployments consistent.

---

# Multiple Providers

A Terraform project can use more than one provider.

Example:

```text id="u4n8kb"
Terraform
      │
      ├── AWS Provider
      │
      └── Local Provider
```

AWS creates cloud resources, while the Local Provider manages files on your computer.

---

# Example Project

```text id="m2q6hv"
Terraform
      │
      ▼
AWS Provider
      │
      ▼
Create EC2 Instance
Create VPC
Create Security Group
```

The provider handles communication with AWS automatically.

---

# Project Structure

A typical Terraform project looks like this:

```text id="z5v3rc"
terraform/
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

Typically:

```text id="t8m1qy"
versions.tf → Terraform and provider requirements

provider.tf → Provider configuration
```

---

# Provider Authentication

Providers usually require authentication.

For AWS, Terraform commonly uses:

```text id="d7k9pn"
AWS Access Key
AWS Secret Access Key
```

Or:

```text id="b4x6mr"
Environment Variables
AWS CLI Configuration
IAM Roles
```

Terraform uses these credentials to authenticate with AWS.

---

# Provider vs Resource

Many beginners confuse these concepts.

```text id="v9p5hx"
Provider
--------
Connects Terraform to AWS

Resource
--------
Creates infrastructure
```

Example:

```text id="n3r8kw"
Terraform
     │
     ├── Provider
     │        │
     │        ▼
     │      AWS API
     │
     └── Resources
              │
              ▼
       EC2
       VPC
       S3
```

The provider communicates with AWS, while resources define what should be created.

---

# Common Beginner Mistakes

### Forgetting terraform init

Bad:

```bash id="g6y2tc"
terraform apply
```

before:

```bash id="r1m8vp"
terraform init
```

Terraform must download the provider first.

---

### Not Pinning Provider Versions

Bad:

```hcl id="k7x4mz"
version = "latest"
```

Better:

```hcl id="q9v3pb"
version = "~> 6.0"
```

This keeps deployments consistent.

---

### Hardcoding Credentials

Bad:

```hcl id="x5n7rh"
provider "aws" {

  access_key = "AKIA..."

  secret_key = "SECRET..."

}
```

Never store credentials inside Terraform files.

---

### Hardcoding the Region

Bad:

```hcl id="h2m6qy"
region = "us-east-1"
```

Better:

```hcl id="w8p4kn"
region = var.aws_region
```

---

### Forgetting Provider Configuration

Terraform cannot create AWS resources without a configured AWS provider.

---

# Best Practices

```text id="j4v9rm"
Pin provider versions
Store configuration in provider.tf
Store requirements in versions.tf
Use variables for configurable values
Authenticate securely
Run terraform init before planning
```

---

# Useful Commands

Initialize Terraform:

```bash id="y7m3qx"
terraform init
```

Show installed providers:

```bash id="c8r5hv"
terraform providers
```

Upgrade providers:

```bash id="n2x9wp"
terraform init -upgrade
```

Validate configuration:

```bash id="f6k4pt"
terraform validate
```

Review changes:

```bash id="u3v8rn"
terraform plan
```

Deploy infrastructure:

```bash id="p5m7kx"
terraform apply
```

---

# Summary

```text id="e1q6mv"
Provider → Connects Terraform to a platform
AWS Provider → Manages AWS resources
provider {} → Configures the provider
required_providers → Downloads provider plugins
terraform init → Installs providers
Provider → Communicates with APIs
```

> Terraform providers are plugins that allow Terraform to communicate with cloud platforms and services. They act as the bridge between Terraform configurations and infrastructure APIs, enabling Terraform to create, update, and manage resources automatically.

