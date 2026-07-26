# 15 - Terraform Remote Backend

By default, Terraform stores its state locally in a file called:

```text
terraform.tfstate
```

This works for learning and small personal projects, but it is **not recommended** for production or team environments.

A **remote backend** stores the Terraform state in a shared remote location instead of on your local computer.

```text
Local Backend
-------------
Your Computer
     │
     ▼
terraform.tfstate

Remote Backend
--------------
Terraform
     │
     ▼
Remote Storage
(OCI Object Storage)
```

## Why Do We Need a Remote Backend?

Imagine you and your teammate both manage the same infrastructure.

With a local backend:

```text
Developer A
└── terraform.tfstate

Developer B
└── terraform.tfstate
```

Each developer has a different state file.

This can lead to:

```text
Conflicting changes
Lost resources
State corruption
Infrastructure drift
```

With a remote backend:

```text
Developer A
      │
      ▼
OCI Object Storage
      ▲
      │
Developer B
```

Everyone uses the same state file.

Benefits:

```text
Shared state
Team collaboration
Centralized storage
Safer infrastructure management
```

---

# What Is a Terraform State File?

The state file keeps track of everything Terraform creates.

It contains information such as:

```text
Resource IDs
Instance OCIDs
Subnet IDs
VCN IDs
Public IP addresses
Metadata
```

Terraform compares:

```text
Configuration
        │
        ▼
Terraform State
        │
        ▼
Actual Cloud Resources
```

This allows Terraform to determine what needs to be created, updated, or destroyed.

---

# Local Backend

Without a backend configuration:

```text
project/
├── main.tf
├── variables.tf
└── terraform.tfstate
```

Terraform automatically creates:

```text
terraform.tfstate
```

This file remains on your computer.

---

# Why Local State Is Not Ideal

Problems with local state:

```text
Not shared
Easy to lose
Cannot collaborate easily
Hard to back up
May contain sensitive information
```

If your computer fails, the state file may be lost.

---

# Remote Backend

A remote backend stores the state in cloud storage.

For Oracle Cloud Infrastructure, a common choice is:

```text
OCI Object Storage
```

The architecture looks like this:

```text
Terraform
      │
      ▼
OCI Object Storage Bucket
      │
      ▼
terraform.tfstate
```

---

# OCI Object Storage

Object Storage is an OCI service used to store files (objects).

Examples:

```text
Images
Backups
Logs
Terraform state files
```

Terraform uploads and updates the state automatically.

---

# Backend Configuration

Example backend configuration:

```hcl
terraform {
  backend "s3" {
    endpoint                    = "https://<namespace>.compat.objectstorage.<region>.oraclecloud.com"
    bucket                      = "terraform-state"
    key                         = "dev/terraform.tfstate"
    region                      = "us-ashburn-1"
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    use_path_style              = true
  }
}
```

Although the backend type is `s3`, Terraform communicates with **OCI Object Storage's S3-compatible API**.

---

# Understanding Backend Settings

Example:

```hcl
bucket = "terraform-state"
```

The Object Storage bucket where the state is stored.

---

```hcl
key = "dev/terraform.tfstate"
```

The object name inside the bucket.

Example:

```text
terraform-state
└── dev/
    └── terraform.tfstate
```

---

```hcl
region = "us-ashburn-1"
```

The OCI region hosting the Object Storage bucket.

---

```hcl
endpoint = "https://<namespace>.compat.objectstorage.<region>.oraclecloud.com"
```

The S3-compatible endpoint used by OCI Object Storage.

---

# Initialize the Backend

After adding the backend configuration:

```bash
terraform init
```

Terraform initializes the backend.

Example:

```text
Initializing the backend...

Successfully configured the backend.
```

---

# Migrating Existing State

Suppose you already have:

```text
terraform.tfstate
```

After configuring a remote backend, run:

```bash
terraform init
```

Terraform asks whether to migrate the existing state.

Example:

```text
Do you want to copy the existing state to the new backend?
```

Answer:

```text
yes
```

Terraform uploads the local state to Object Storage.

---

# Typical Workflow

```bash
terraform init
terraform plan
terraform apply
```

Terraform automatically downloads the latest state before planning and uploads changes after applying.

---

# Remote Backend Workflow

```text
terraform apply
        │
        ▼
Read remote state
        │
Compare infrastructure
        │
Apply changes
        │
Upload updated state
```

The process is automatic.

---

# State File Is Sensitive

A Terraform state file may contain:

```text
Instance IDs
Network IDs
Public IPs
Resource metadata
Configuration values
```

Protect it carefully.

Do **not**:

```text
Upload it to GitHub
Email it
Share it publicly
```

---

# .gitignore

Never commit local state files.

Example:

```text
.terraform/
terraform.tfstate
terraform.tfstate.*
crash.log
```

This keeps sensitive files out of your repository.

---

# Backend vs Provider

Many beginners confuse these.

Provider:

```text
Talks to OCI
Creates resources
Deletes resources
Updates resources
```

Backend:

```text
Stores Terraform state
```

Simple diagram:

```text
Terraform
   │
   ├── Provider ──► OCI Resources
   │
   └── Backend ──► State File
```

They solve different problems.

---

# Example Project Structure

```text
terraform/
├── backend.tf
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
└── main.tf
```

The backend configuration is usually placed in:

```text
backend.tf
```

---

# Using Different State Files

You can organize multiple environments.

Example:

```text
terraform-state
├── dev/
│   └── terraform.tfstate
├── staging/
│   └── terraform.tfstate
└── production/
    └── terraform.tfstate
```

Each environment has its own state file.

---

# Backend Initialization Is Required

Whenever you:

```text
Clone a repository
Change backend settings
Create a new project
```

Run:

```bash
terraform init
```

Terraform initializes providers and the backend.

---

# Common Beginner Mistakes

### Uploading State to GitHub

Bad:

```text
terraform.tfstate
```

Better:

```text
.gitignore
```

---

### Thinking Backend Creates Resources

Wrong:

```text
Backend creates OCI resources.
```

Correct:

```text
Provider creates OCI resources.

Backend stores Terraform state.
```

---

### Editing State Manually

Avoid editing:

```text
terraform.tfstate
```

Terraform manages it automatically.

Manual edits can corrupt the state.

---

### Forgetting terraform init

After adding or changing a backend:

```bash
terraform init
```

must be run again.

---

### Using One State for Everything

Bad:

```text
One state file for development and production.
```

Better:

```text
Separate state files for each environment.
```

---

# Best Practices

```text
Use a remote backend for team projects
Protect the state file
Never commit state files
Use separate state per environment
Keep backend configuration in backend.tf
Run terraform init after backend changes
Back up important state files
```

---

# Useful Commands

Initialize backend:

```bash
terraform init
```

Show current state:

```bash
terraform show
```

List managed resources:

```bash
terraform state list
```

Show one resource:

```bash
terraform state show RESOURCE_NAME
```

Refresh state:

```bash
terraform refresh
```

---

# Summary

```text
Local Backend  → Stores state on your computer
Remote Backend → Stores state in shared remote storage
State File     → Tracks infrastructure
Provider       → Creates cloud resources
Backend        → Stores Terraform state
terraform init → Initializes providers and backend
```

> A Terraform remote backend stores the Terraform state in shared remote storage, making collaboration safer, keeping state centralized, and reducing the risk of losing or corrupting infrastructure state.

