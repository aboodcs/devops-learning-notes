# 08 - Terraform Local Provider

Terraform is commonly used to create cloud infrastructure such as EC2 instances, VPCs, and S3 buckets.

However, Terraform can also manage resources **on your local computer**.

This is done using the **Local Provider**.

```text
Terraform
      │
      ├── AWS Provider
      │        │
      │        ▼
      │   AWS Resources
      │
      └── Local Provider
               │
               ▼
        Local Files
```

The Local Provider allows Terraform to create and manage files on your local machine.

---

# Why Do We Need the Local Provider?

Imagine you want Terraform to automatically generate:

```text
Configuration files
README files
Environment files
Scripts
Logs
```

Instead of creating them manually, Terraform can create them for you.

Benefits:

```text
Automation
Consistency
Repeatable configuration
Useful for testing and learning
```

---

# Installing the Local Provider

Terraform downloads providers automatically during initialization.

Example:

```hcl
terraform {

  required_providers {

    local = {

      source  = "hashicorp/local"

      version = "~> 2.5"
    }
  }
}
```

After running:

```bash
terraform init
```

Terraform downloads the Local Provider.

---

# Local Provider Configuration

Unlike cloud providers, the Local Provider usually requires no configuration.

Example:

```hcl
provider "local" {
}
```

This tells Terraform to use the Local Provider.

---

# The local_file Resource

The most common resource is:

```text
local_file
```

It creates a file on your local computer.

Example:

```hcl
resource "local_file" "readme" {

  filename = "README.txt"

  content  = "Hello from Terraform!"
}
```

Running:

```bash
terraform apply
```

creates:

```text
README.txt
```

with the content:

```text
Hello from Terraform!
```

---

# Example Project

Project structure:

```text
terraform/
├── main.tf
├── terraform.tfstate
└── README.txt
```

Terraform manages the generated file.

---

# Using Variables

Instead of hardcoding values:

```hcl
content = "Hello"
```

Use variables.

```hcl
variable "project_name" {

  default = "Terraform Lab"

}
```

Resource:

```hcl
resource "local_file" "readme" {

  filename = "README.txt"

  content = "Project: ${var.project_name}"
}
```

Generated file:

```text
Project: Terraform Lab
```

---

# Using Heredoc Strings

For multi-line files:

```hcl
resource "local_file" "config" {

  filename = "config.txt"

  content = <<EOF
Application=Terraform
Environment=Development
Version=1.0
EOF
}
```

Terraform preserves the formatting.

---

# Dynamic File Names

The filename can use variables.

Example:

```hcl
variable "environment" {

  default = "dev"

}
```

```hcl
resource "local_file" "config" {

  filename = "${var.environment}.txt"

  content = "Development Environment"
}
```

Terraform creates:

```text
dev.txt
```

---

# Updating Files

Suppose:

```text
README.txt

Version 1
```

You change:

```hcl
content = "Version 2"
```

Then run:

```bash
terraform apply
```

Terraform updates the file automatically.

---

# Destroying Files

Terraform also manages deletion.

Running:

```bash
terraform destroy
```

removes:

```text
README.txt
```

from your local computer.

---

# Terraform State

The Local Provider is managed exactly like cloud resources.

Terraform stores information in:

```text
terraform.tfstate
```

Example:

```text
Terraform
      │
      ▼
State File
      │
      ▼
README.txt
```

Terraform knows whether the file already exists.

---

# Multiple Files

Terraform can create multiple files.

Example:

```hcl
resource "local_file" "readme" {

  filename = "README.md"

  content = "Terraform Project"
}

resource "local_file" "config" {

  filename = "config.txt"

  content = "Development"
}
```

Terraform creates both files.

---

# Example Project Structure

```text
terraform/
├── provider.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── README.md
├── config.txt
└── terraform.tfstate
```

---

# Local Provider vs AWS Provider

```text
Local Provider
--------------
Creates local files

AWS Provider
------------
Creates AWS resources
```

Example:

```text
Terraform
     │
     ├── Local Provider
     │        │
     │        ▼
     │    README.md
     │
     └── AWS Provider
              │
              ▼
          EC2 Instance
```

---

# Common Beginner Mistakes

### Forgetting terraform init

Bad:

```bash
terraform apply
```

before:

```bash
terraform init
```

Terraform must download the Local Provider first.

---

### Editing Managed Files Manually

Suppose you edit:

```text
README.txt
```

manually.

The next:

```bash
terraform apply
```

may overwrite your changes.

---

### Hardcoding Everything

Bad:

```hcl
filename = "dev.txt"
```

Better:

```hcl
filename = "${var.environment}.txt"
```

---

### Forgetting terraform destroy

Terraform manages the files it creates.

Use:

```bash
terraform destroy
```

to remove them when finished.

---

# Best Practices

```text
Use variables
Keep generated files inside the project directory
Use Heredoc for multi-line files
Avoid manually editing Terraform-managed files
Run terraform init before applying
```

---

# Useful Commands

Initialize Terraform:

```bash
terraform init
```

Review changes:

```bash
terraform plan
```

Create files:

```bash
terraform apply
```

Show infrastructure:

```bash
terraform show
```

Destroy managed files:

```bash
terraform destroy
```

---

# Summary

```text
Local Provider → Manages local resources
local_file → Creates local files
terraform init → Downloads the provider
terraform apply → Creates or updates files
terraform destroy → Removes managed files
terraform.tfstate → Tracks managed resources
```

> The Local Provider allows Terraform to manage resources on your local computer, making it useful for creating configuration files, scripts, documentation, and other local artifacts while still benefiting from Terraform's state management and automation.

