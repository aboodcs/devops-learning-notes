# 07 - Terraform Variables Files (tfvars)

Terraform uses **variables** to make configurations reusable and flexible.

Instead of changing values directly inside the Terraform code, you can store them in a separate **`.tfvars`** file.

```text id="v4k8xm"
Terraform Code
       │
       ▼
Variables
       │
       ▼
terraform.tfvars
```

This allows you to use the same Terraform configuration with different values.

---

# Why Do We Need tfvars?

Imagine you have this configuration:

```hcl id="m9p3zc"
instance_type = "t3.micro"

region = "us-east-1"
```

If you want a different region or instance type, you must edit the code.

Instead, use variables.

```text id="n7q5hy"
Terraform Code
        │
        ▼
Variables
        │
        ▼
terraform.tfvars
```

Benefits:

```text id="h2v8ra"
Reusable configuration
Cleaner code
Easy environment management
Separate configuration from values
```

---

# Declaring Variables

Variables are usually declared in:

```text id="j5m9ws"
variables.tf
```

Example:

```hcl id="p4r6kt"
variable "aws_region" {

  type = string

}

variable "instance_type" {

  type = string

}
```

These variables do not yet have values.

---

# Creating terraform.tfvars

Create:

```text id="f8x2ld"
terraform.tfvars
```

Example:

```hcl id="g7w4pn"
aws_region   = "us-east-1"

instance_type = "t3.micro"
```

Terraform automatically loads this file.

---

# Using Variables

Example provider:

```hcl id="b3y9cv"
provider "aws" {

  region = var.aws_region
}
```

Example resource:

```hcl id="r6m1qx"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = var.instance_type
}
```

Terraform replaces:

```text id="z2n8hf"
var.aws_region

var.instance_type
```

with the values from `terraform.tfvars`.

---

# Variable Workflow

```text id="k4v7mb"
variables.tf
      │
Declare Variables
      │
      ▼
terraform.tfvars
      │
Provide Values
      │
      ▼
Terraform Configuration
```

---

# Default Values

Variables may have default values.

Example:

```hcl id="t9q2wy"
variable "instance_type" {

  type = string

  default = "t3.micro"
}
```

If no value is provided, Terraform uses the default.

---

# Overriding Defaults

Example:

variables.tf

```hcl id="x8m3rh"
variable "instance_type" {

  default = "t3.micro"
}
```

terraform.tfvars

```hcl id="y5j7ps"
instance_type = "t3.small"
```

Terraform uses:

```text id="e4c8nt"
t3.small
```

The value in the `.tfvars` file overrides the default.

---

# Multiple tfvars Files

You can create multiple variable files.

Example:

```text id="u6p9ax"
terraform.tfvars

development.tfvars

staging.tfvars

production.tfvars
```

Each file contains values for a different environment.

---

# Using a Specific tfvars File

Terraform automatically loads:

```text id="w1r4kb"
terraform.tfvars
```

To use another file:

```bash id="q7m2vd"
terraform apply -var-file="production.tfvars"
```

Or:

```bash id="p5x8cy"
terraform plan -var-file="development.tfvars"
```

---

# Example Project

```text id="l8n6ft"
terraform/
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
└── compute.tf
```

Example:

variables.tf

```hcl id="c2y5hq"
variable "project_name" {

  type = string
}
```

terraform.tfvars

```hcl id="m3k8pv"
project_name = "Terraform Lab"
```

Usage:

```hcl id="a6v4rz"
tags = {

  Name = var.project_name
}
```

---

# Sensitive Variables

Some variables contain sensitive information.

Examples:

```text id="j9t3qx"
Passwords
API Tokens
Access Keys
Database Credentials
```

Example:

```hcl id="b8m5kp"
variable "db_password" {

  type = string

  sensitive = true
}
```

Do **not** commit secret values to Git.

---

# tfvars vs variables.tf

| File             | Purpose            |
| ---------------- | ------------------ |
| variables.tf     | Declares variables |
| terraform.tfvars | Assigns values     |

Example:

```text id="r4y6wm"
variables.tf
--------------
variable "region"

terraform.tfvars
----------------
region = "us-east-1"
```

---

# Variable Precedence

Terraform loads variables in a specific order.

Highest priority:

```text id="n2h7qx"
Command-line -var

Specific -var-file

terraform.tfvars

Default value
```

Higher-priority values override lower-priority ones.

---

# Example Project Structure

```text id="k6v9zt"
terraform/
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

---

# Common Beginner Mistakes

### Hardcoding Values

Bad:

```hcl id="u4r8px"
instance_type = "t3.micro"
```

Better:

```hcl id="h1n6kv"
instance_type = var.instance_type
```

---

### Committing Secrets

Bad:

```text id="v7m3sy"
terraform.tfvars

Contains passwords
```

Use:

```text id="c5x8ra"
GitHub Secrets

Environment Variables
```

for sensitive values whenever possible.

---

### Forgetting Variable Values

If a required variable has no value, Terraform asks for it during execution.

---

### Confusing variables.tf and terraform.tfvars

Remember:

```text id="f2q9mb"
variables.tf → Declares variables

terraform.tfvars → Provides values
```

---

### Creating Duplicate Variables

Declare each variable only once.

---

# Best Practices

```text id="p8v4nt"
Keep variables in variables.tf
Store values in terraform.tfvars
Use defaults when appropriate
Keep secrets out of Git
Create separate tfvars files for each environment
Use meaningful variable names
```

---

# Useful Commands

Initialize Terraform:

```bash id="x3q7hw"
terraform init
```

Review changes:

```bash id="k9m2pv"
terraform plan
```

Use a specific variable file:

```bash id="r5x8zn"
terraform plan -var-file="production.tfvars"
```

Deploy infrastructure:

```bash id="d4w1kt"
terraform apply
```

Deploy with a specific variable file:

```bash id="j7v6pc"
terraform apply -var-file="development.tfvars"
```

---

# Summary

```text id="m1p8rw"
variables.tf → Declares variables
terraform.tfvars → Assigns values
var.name → Access a variable
default → Optional fallback value
-var-file → Load a specific variables file
sensitive = true → Hide sensitive values
```

> A `.tfvars` file stores values for Terraform variables, allowing the same Terraform configuration to be reused across different environments while keeping configuration values separate from the infrastructure code.

