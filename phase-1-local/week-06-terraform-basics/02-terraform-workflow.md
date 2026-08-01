# 02 - Terraform Workflow

Terraform follows a simple workflow to create, update, and destroy infrastructure.

Every Terraform project typically goes through the same sequence of steps.

```text id="w8m3kp"
Write Code
     │
     ▼
Initialize
     │
     ▼
Validate
     │
     ▼
Plan
     │
     ▼
Apply
     │
     ▼
Infrastructure Created
```

Understanding this workflow is essential before working with any cloud provider.

---

# Why Do We Need a Workflow?

Imagine you want to create:

```text id="k4v9rn"
EC2 Instance
VPC
Subnet
Security Group
```

Terraform should not immediately create resources.

Instead, it follows a controlled process to verify the configuration and preview changes before making them.

Benefits:

```text id="r7x2mw"
Detect errors early
Preview infrastructure changes
Reduce deployment mistakes
Maintain predictable infrastructure
```

---

# Step 1 - Write Terraform Configuration

The first step is writing Terraform code.

Example:

```hcl id="n5q8pv"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

}
```

Terraform configuration files usually use the `.tf` extension.

Example project:

```text id="y3m7kt"
terraform/
├── provider.tf
├── variables.tf
├── network.tf
├── compute.tf
└── outputs.tf
```

---

# Step 2 - Initialize the Project

Initialize the working directory.

```bash id="f8v4qx"
terraform init
```

Terraform:

```text id="c2p9hw"
Downloads providers
Initializes the backend
Creates the .terraform directory
```

Example output:

```text id="m6x3rn"
Terraform has been successfully initialized!
```

This command is usually run only once for a new project or after changing providers or backends.

---

# Step 3 - Validate the Configuration

Check the syntax of the Terraform configuration.

```bash id="q1k7mv"
terraform validate
```

Example output:

```text id="a5r8py"
Success! The configuration is valid.
```

Validation checks:

```text id="u4m2kx"
Syntax errors
Missing arguments
Invalid resource references
```

It does **not** contact the cloud provider.

---

# Step 4 - Format the Code

Terraform includes a formatter that keeps code consistent.

```bash id="v7p5tn"
terraform fmt
```

Example:

Before:

```hcl id="e3q9mw"
resource "aws_vpc" "main"{cidr_block="10.0.0.0/16"}
```

After:

```hcl id="x8m4rv"
resource "aws_vpc" "main" {

  cidr_block = "10.0.0.0/16"

}
```

Formatting improves readability and consistency.

---

# Step 5 - Review the Execution Plan

Preview the changes Terraform will make.

```bash id="t6k2qx"
terraform plan
```

Terraform compares:

```text id="h9v3rm"
Configuration
State File
Actual Infrastructure
```

Then it displays:

```text id="n4p7wy"
Resources to create
Resources to update
Resources to destroy
```

No infrastructure changes are made during this step.

---

# Step 6 - Apply the Changes

Deploy the infrastructure.

```bash id="b5x8kn"
terraform apply
```

Terraform displays the plan and asks for confirmation.

```text id="z2m6pv"
Do you want to perform these actions?

Enter a value:
```

Type:

```text id="j7q4hr"
yes
```

Terraform creates or updates the infrastructure.

---

# Step 7 - Review the Outputs

After deployment, Terraform displays output values.

Example:

```text id="r8v1py"
instance_id = "i-0123456789abcdef0"

public_ip = "54.xxx.xxx.xxx"
```

You can display them again:

```bash id="g4m9tx"
terraform output
```

---

# Step 8 - Modify Infrastructure

To make changes, edit the Terraform configuration.

Example:

```hcl id="k9w3pb"
instance_type = "t3.small"
```

Run:

```bash id="n6x2qm"
terraform plan
```

Terraform shows only the required changes.

Then apply them:

```bash id="u5r8vn"
terraform apply
```

---

# Step 9 - Destroy Infrastructure

Remove all managed resources.

```bash id="d3p7ky"
terraform destroy
```

Terraform displays the destruction plan before deleting resources.

This is useful for cleaning up development or lab environments.

---

# Complete Workflow

```text id="m2v9rx"
Write Configuration
        │
        ▼
terraform init
        │
        ▼
terraform validate
        │
        ▼
terraform fmt
        │
        ▼
terraform plan
        │
        ▼
terraform apply
        │
        ▼
terraform output
        │
        ▼
terraform destroy
```

---

# Terraform State in the Workflow

Terraform stores information about managed resources in the state file.

```text id="w6k3pn"
Terraform Code
       │
       ▼
terraform.tfstate
       │
       ▼
Cloud Infrastructure
```

The state file allows Terraform to detect changes and manage existing resources safely.

---

# Typical Project Structure

```text id="q7m5hv"
terraform/
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
├── security.tf
└── terraform.tfstate
```

---

# Common Beginner Mistakes

### Skipping terraform init

Bad:

```bash id="x1r8qt"
terraform plan
```

before:

```bash id="h5v2mw"
terraform init
```

Terraform must download the required providers first.

---

### Skipping terraform validate

Always validate the configuration before planning or applying changes.

---

### Applying Without Reviewing the Plan

Bad:

```bash id="p8k4rv"
terraform apply -auto-approve
```

Review the execution plan whenever possible before making infrastructure changes.

---

### Editing Infrastructure Manually

Making changes directly in the cloud console can cause infrastructure drift.

Prefer managing infrastructure through Terraform.

---

### Forgetting terraform destroy

Development resources continue running until they are destroyed, which may result in unnecessary cloud costs.

---

# Best Practices

```text id="f9m6px"
Run terraform fmt regularly
Validate before planning
Always review terraform plan
Store code in Git
Use variables instead of hardcoded values
Destroy unused lab resources
```

---

# Useful Commands

Initialize Terraform:

```bash id="t2q8wn"
terraform init
```

Format configuration:

```bash id="c7m4ry"
terraform fmt
```

Validate configuration:

```bash id="v3p9kx"
terraform validate
```

Review changes:

```bash id="g6x1mt"
terraform plan
```

Deploy infrastructure:

```bash id="n8r5pv"
terraform apply
```

Display outputs:

```bash id="u4k7qh"
terraform output
```

Destroy infrastructure:

```bash id="e9m2wx"
terraform destroy
```

---

# Summary

```text id="b7v3pn"
terraform init → Initialize project
terraform validate → Check configuration
terraform fmt → Format code
terraform plan → Preview changes
terraform apply → Create or update infrastructure
terraform output → Display outputs
terraform destroy → Remove infrastructure
```

> The Terraform workflow provides a safe and predictable process for managing infrastructure, allowing you to validate configurations, preview changes, deploy resources, and remove them when they are no longer needed.

