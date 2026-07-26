# 17 - Terraform Best Practices

Writing Terraform code is easy.

Writing **maintainable, secure, reusable, and production-ready** Terraform code is much harder.

Terraform best practices help you build infrastructure that is:

```text
Easy to read
Easy to maintain
Reusable
Secure
Consistent
Reliable
```

## Why Best Practices Matter

Imagine two projects.

Project A:

```text
Everything is inside one main.tf
Hardcoded values
No variables
No outputs
No documentation
```

Project B:

```text
Organized folders
Variables
Outputs
Modules
Remote state
Version control
Documentation
```

Both projects may work today.

Only Project B will still be manageable months later.

---

# 1. Keep Files Organized

Avoid putting everything inside one file.

Bad structure:

```text
terraform/
└── main.tf
```

Better structure:

```text
terraform/
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
├── storage.tf
├── security.tf
├── terraform.tfvars.example
└── README.md
```

Benefits:

```text
Easy navigation
Cleaner code
Better teamwork
```

---

# 2. Use Meaningful Resource Names

Bad:

```hcl
resource "oci_core_instance" "vm1" {}
```

Better:

```hcl
resource "oci_core_instance" "web_server" {}
```

Even better:

```hcl
resource "oci_core_instance" "jenkins_server" {}
```

Good names explain the resource purpose.

---

# 3. Never Hardcode Values

Bad:

```hcl
availability_domain = "Uocm:PHX-AD-1"

shape = "VM.Standard.E2.1.Micro"
```

Better:

```hcl
availability_domain = var.availability_domain

shape = var.instance_shape
```

variables.tf

```hcl
variable "instance_shape" {
  type    = string
  default = "VM.Standard.E2.1.Micro"
}
```

Now the value can be changed without editing resources.

---

# 4. Use Variables

Store configurable values inside variables.

Examples:

```text
Region
Compartment ID
VCN CIDR
Instance shape
SSH key
Environment
Project name
```

Example:

```hcl
variable "region" {
  type = string
}
```

---

# 5. Use Outputs

Outputs expose useful information after deployment.

Example:

```hcl
output "public_ip" {
  value = oci_core_instance.web_server.public_ip
}
```

Run:

```bash
terraform output
```

Example output:

```text
public_ip = 150.230.xxx.xxx
```

---

# 6. Pin Provider Versions

Avoid automatically downloading new provider versions.

Bad:

```hcl
terraform {
  required_providers {
    oci = {
      source = "oracle/oci"
    }
  }
}
```

Better:

```hcl
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 7.0"
    }
  }
}
```

Benefits:

```text
Stable builds
Predictable behavior
Fewer breaking changes
```

---

# 7. Commit the Lock File

Terraform creates:

```text
.terraform.lock.hcl
```

Commit it to Git.

Do **not** delete it.

It keeps provider versions consistent for everyone.

---

# 8. Ignore Temporary Files

Create `.gitignore`

```text
.terraform/
*.tfstate
*.tfstate.*
crash.log
terraform.tfvars
```

Never upload state files to GitHub.

---

# 9. Protect Secrets

Never store secrets inside Terraform files.

Bad:

```hcl
variable "password" {
  default = "MySecretPassword123"
}
```

Better:

```hcl
variable "password" {}
```

Provide it securely:

```bash
export TF_VAR_password="MySecretPassword123"
```

Or use:

```text
OCI Vault
GitHub Secrets
Environment variables
```

---

# 10. Never Commit terraform.tfvars

Bad:

```text
terraform.tfvars
```

Good:

```text
terraform.tfvars.example
```

Example:

```hcl
region = "eu-frankfurt-1"

compartment_id = "replace-me"

ssh_public_key = "replace-me"
```

Users copy:

```bash
cp terraform.tfvars.example terraform.tfvars
```

---

# 11. Use Remote State

Avoid local state for team projects.

Bad:

```text
terraform.tfstate
```

Better:

```text
OCI Object Storage
```

Benefits:

```text
Shared state
State locking
Backups
Team collaboration
```

---

# 12. Use Modules

Instead of repeating resources:

```text
Instance 1
Instance 2
Instance 3
```

Create one reusable module.

Example:

```text
modules/
└── compute/
```

Use:

```hcl
module "web_server" {
  source = "./modules/compute"
}
```

Benefits:

```text
Reusable
Cleaner
Less duplication
```

---

# 13. Tag Everything

OCI supports tags.

Example:

```hcl
freeform_tags = {
  Project = "DevOps-Learning"
  Owner   = "abood"
  Env     = "Development"
}
```

Benefits:

```text
Organization
Cost tracking
Searching
Automation
```

---

# 14. Keep Resources Small

Avoid creating huge files.

Instead of:

```text
network.tf
(900 lines)
```

Split into:

```text
vcn.tf
subnets.tf
internet-gateway.tf
security-lists.tf
route-tables.tf
```

---

# 15. Use terraform fmt

Automatically format code.

```bash
terraform fmt
```

Recursive:

```bash
terraform fmt -recursive
```

Always format before committing.

---

# 16. Validate Configuration

Check syntax:

```bash
terraform validate
```

Terraform catches many errors before deployment.

---

# 17. Review Execution Plan

Never run:

```bash
terraform apply
```

without checking:

```bash
terraform plan
```

Typical workflow:

```bash
terraform fmt
terraform validate
terraform plan
terraform apply
```

---

# 18. Destroy Test Resources

After finishing a lab:

```bash
terraform destroy
```

Otherwise cloud resources may continue running and generate costs.

---

# 19. Use Descriptive Outputs

Bad:

```hcl
output "ip" {}
```

Better:

```hcl
output "web_server_public_ip" {}
```

---

# 20. Keep Documentation Updated

Every Terraform project should include a README.

Example:

```text
Project overview
Requirements
Variables
Outputs
How to initialize
How to deploy
How to destroy
```

---

# 21. Follow a Consistent Workflow

A common workflow:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform output
terraform destroy
```

---

# 22. Separate Environments

Do not use one configuration for everything.

Example:

```text
terraform/
├── dev/
├── staging/
└── production/
```

Each environment can have different:

```text
Variables
State
Resources
Permissions
```

---

# 23. Keep State Safe

The Terraform state file contains infrastructure information.

It may include:

```text
Resource IDs
IP addresses
Configuration details
Metadata
```

Treat it as sensitive.

Do not:

```text
Upload it to GitHub
Email it
Share it publicly
```

---

# 24. Use Consistent Naming

Instead of random names:

```text
vm1
server2
instance-test
```

Use meaningful names:

```text
web-server
database-server
jenkins-agent
private-subnet
public-subnet
```

---

# 25. Use Comments Sparingly

Good code should be easy to understand.

Use comments only when they add useful context.

Example:

```hcl
# Public subnet for web servers
resource "oci_core_subnet" "public_subnet" {
```

Avoid comments that repeat the code.

---

# Common Beginner Mistakes

### Hardcoding Values

Bad:

```hcl
shape = "VM.Standard.E2.1.Micro"
```

Better:

```hcl
shape = var.instance_shape
```

---

### Using Local State Forever

Bad:

```text
terraform.tfstate
```

Better:

```text
Remote backend
```

---

### Skipping terraform plan

Bad:

```bash
terraform apply
```

Better:

```bash
terraform plan
terraform apply
```

---

### Committing Secrets

Bad:

```text
terraform.tfvars
```

Better:

```text
terraform.tfvars.example
```

---

### Not Formatting Code

Bad:

Messy formatting.

Better:

```bash
terraform fmt
```

---

### Forgetting terraform destroy

Test resources may continue running and increase cloud costs.

Always clean up lab resources:

```bash
terraform destroy
```

---

# Best Practice Checklist

Before deploying, ask yourself:

```text
Are variables used?
Are secrets protected?
Is the provider version pinned?
Is the code formatted?
Did validation pass?
Did I review the plan?
Are outputs useful?
Is state stored safely?
Is documentation updated?
Can another person understand this project?
```

---

# Useful Commands

Initialize project:

```bash
terraform init
```

Format code:

```bash
terraform fmt -recursive
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

Show outputs:

```bash
terraform output
```

Destroy infrastructure:

```bash
terraform destroy
```

---

# Summary

```text
Organize files
Use variables
Use outputs
Protect secrets
Pin provider versions
Commit the lock file
Ignore state files
Use remote state
Use modules
Tag resources
Run terraform fmt
Run terraform validate
Review terraform plan
Document the project
Destroy lab resources
```

> Following Terraform best practices makes your infrastructure easier to maintain, safer to use, and more reliable as your projects grow.

