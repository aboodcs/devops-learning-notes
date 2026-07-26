# 10 - Terraform State

Terraform needs a way to remember the infrastructure it creates.

It does this using a **Terraform State** file.

The state file records every resource Terraform manages and keeps infrastructure synchronized with your Terraform configuration.

```text id="b6w4kn"
Terraform Configuration
         │
         ▼
Terraform State
         │
         ▼
Cloud Infrastructure
```

Without the state file, Terraform would not know which resources already exist.

---

# Why Do We Need Terraform State?

Imagine you create an EC2 instance.

```hcl id="s9m3xd"
resource "aws_instance" "web" {

  instance_type = "t3.micro"

}
```

Terraform creates the instance.

Later, you run:

```bash id="r2n8kp"
terraform apply
```

Terraform checks the state file to determine:

```text id="v7q5rh"
Already exists?
Needs updating?
Needs deleting?
```

Without the state, Terraform would try to recreate resources every time.

---

# What Is Stored in the State?

The state file contains information such as:

```text id="n4c7wy"
Resource IDs
Resource names
Instance IDs
Public IP addresses
Private IP addresses
Network IDs
Metadata
```

Example:

```text id="j6x3fa"
EC2 Instance
ID: i-0ab12345cd67890ef

Public IP:
54.201.xxx.xxx

Subnet:
subnet-01234567
```

Terraform stores these values in the state file.

---

# The State File

After running:

```bash id="u8m2zr"
terraform apply
```

Terraform creates:

```text id="h3k5mv"
terraform.tfstate
```

Project example:

```text id="w7p4lg"
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
└── terraform.tfstate
```

---

# State Workflow

```text id="c9r6qs"
Terraform Code
       │
       ▼
Read State
       │
Compare Infrastructure
       │
Plan Changes
       │
Apply Changes
       │
Update State
```

Terraform automatically updates the state after every successful apply.

---

# Local State

By default, Terraform stores the state locally.

```text id="g5v2nk"
Your Computer
      │
      ▼
terraform.tfstate
```

This works well for:

```text id="x2y8ph"
Learning
Personal projects
Small labs
```

---

# Remote State

For team projects, the state is usually stored remotely.

Example:

```text id="d8m4qc"
Terraform
      │
      ▼
Amazon S3 Bucket
      │
      ▼
terraform.tfstate
```

Remote state improves collaboration and reduces the risk of losing the state file.

---

# Terraform Refresh

Terraform compares:

```text id="q4z6wt"
Terraform Code
State File
Actual AWS Infrastructure
```

If resources have changed outside Terraform, the state is updated during planning or refresh operations.

---

# State and Resources

Example:

```hcl id="k7h9pd"
resource "aws_vpc" "main" {
}

resource "aws_subnet" "public" {
}
```

The state keeps track of both resources.

```text id="p3n8yb"
aws_vpc.main

aws_subnet.public
```

Terraform knows they already exist.

---

# Viewing the State

Show the current infrastructure:

```bash id="r6x2mw"
terraform show
```

List resources:

```bash id="n9w5vc"
terraform state list
```

Example output:

```text id="t4q8zs"
aws_vpc.main

aws_subnet.public

aws_instance.web
```

---

# Inspect a Resource

Show details for one resource:

```bash id="m2j7pk"
terraform state show aws_instance.web
```

Example:

```text id="k8p3wd"
AMI

Instance Type

Public IP

Private IP

Tags
```

---

# State Lifecycle

```text id="y5v9qt"
terraform apply
        │
Create Resources
        │
Update State
        │
terraform plan
        │
Read State
        │
terraform destroy
        │
Delete Resources
        │
Update State
```

---

# Infrastructure Drift

Sometimes resources are changed manually.

Example:

```text id="z6r2hw"
Terraform → t3.micro

AWS Console → t3.small
```

Terraform detects the difference during planning.

```text id="g9k4pn"
Terraform Code
        │
        ▼
State
        │
        ▼
AWS
```

If they differ, Terraform proposes changes.

---

# State Locking

When multiple people use Terraform simultaneously, only one person should modify the state at a time.

```text id="u3v7mc"
Developer A
      │
      ▼
State Locked

Developer B
Waits
```

State locking prevents corruption.

Remote backends such as Amazon S3 with DynamoDB locking (or newer locking mechanisms) are commonly used for this purpose.

---

# Sensitive Information

The state file may contain:

```text id="m6q2fa"
Public IPs
Resource IDs
Configuration values
Metadata
```

Some providers may also store sensitive values.

Protect the state file carefully.

Never upload it publicly.

---

# Ignore State Files in Git

Never commit local state files.

Example `.gitignore`:

```text id="x8r5lu"
.terraform/
terraform.tfstate
terraform.tfstate.*
crash.log
```

---

# Example Project Structure

```text id="h7p4ny"
terraform/
├── provider.tf
├── network.tf
├── security.tf
├── compute.tf
├── variables.tf
├── outputs.tf
└── terraform.tfstate
```

In production, the state is typically stored remotely instead of inside the project directory.

---

# Common Beginner Mistakes

### Deleting the State File

Bad:

```text id="p4x8qm"
Delete terraform.tfstate
```

Terraform loses track of managed resources.

---

### Editing the State Manually

Avoid modifying:

```text id="j5w2zt"
terraform.tfstate
```

Manual edits can corrupt the state.

---

### Committing State to GitHub

Bad:

```text id="e7n3kp"
git add terraform.tfstate
```

Use:

```text id="t8v6hr"
.gitignore
```

instead.

---

### Creating Resources Outside Terraform

Changing infrastructure manually can cause infrastructure drift.

Prefer managing resources through Terraform whenever possible.

---

### Forgetting Remote State

Local state is fine for learning, but production teams should use a remote backend.

---

# Best Practices

```text id="f2k9mb"
Protect the state file
Never commit state to Git
Use remote state for teams
Do not edit state manually
Keep backups of important state
Use terraform state commands when needed
```

---

# Useful Commands

Initialize Terraform:

```bash id="g3m7qx"
terraform init
```

Review changes:

```bash id="k6v8ps"
terraform plan
```

Deploy infrastructure:

```bash id="y9q2nh"
terraform apply
```

Show infrastructure:

```bash id="d4r5zt"
terraform show
```

List resources:

```bash id="n8m3kw"
terraform state list
```

Show one resource:

```bash id="u7x5pc"
terraform state show aws_instance.web
```

Destroy infrastructure:

```bash id="w2p6fd"
terraform destroy
```

---

# Summary

```text id="a5m9kr"
Terraform State → Tracks infrastructure
terraform.tfstate → State file
terraform show → Display infrastructure
terraform state list → List managed resources
terraform state show → Inspect a resource
Local State → Stored on your computer
Remote State → Shared storage for teams
```

> Terraform State is the source of truth for Terraform-managed infrastructure, allowing Terraform to track resources, detect changes, and safely update cloud infrastructure over time.

