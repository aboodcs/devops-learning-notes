
**Terraform** is an Infrastructure as Code tool.

It lets you create cloud resources using code instead of clicking manually in the OCI Console.

```text id="239pzy"
Terraform code → OCI Provider → Oracle Cloud resources
```

With Terraform, you can create:

```text id="6a0j0h"
VCN
Subnets
Compute Instances
Block Volumes
Load Balancers
Security Lists
Internet Gateways
Route Tables
```

## Why Use Terraform with OCI?

Without Terraform, you create resources manually from the Console.

That is okay for learning, but it becomes hard when the project grows.

Terraform helps you:

```text id="i9c9mr"
Create infrastructure from code
Repeat the same setup many times
Track changes in Git
Destroy resources safely
Build real DevOps projects
```

## Main Terraform Files

A basic OCI Terraform project usually looks like this:

```text id="skyp5z"
oci-terraform-lab/
├── main.tf
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
└── .gitignore
```

## 1. provider.tf

The provider tells Terraform which cloud platform to use.

For OCI, we use the Oracle Cloud provider.

```hcl id="6lr128"
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 6.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}
```

## 2. variables.tf

Variables make the code reusable.

```hcl id="8tvnip"
variable "tenancy_ocid" {
  description = "OCI tenancy OCID"
  type        = string
}

variable "user_ocid" {
  description = "OCI user OCID"
  type        = string
}

variable "fingerprint" {
  description = "API key fingerprint"
  type        = string
}

variable "private_key_path" {
  description = "Path to OCI private API key"
  type        = string
}

variable "region" {
  description = "OCI region"
  type        = string
}

variable "compartment_ocid" {
  description = "OCI compartment OCID"
  type        = string
}
```

## 3. terraform.tfvars

`terraform.tfvars` contains the real values.

```hcl id="e2fv4f"
tenancy_ocid     = "ocid1.tenancy.oc1..example"
user_ocid        = "ocid1.user.oc1..example"
fingerprint      = "aa:bb:cc:dd:ee:ff"
private_key_path = "/home/abood/.oci/oci_api_key.pem"
region           = "me-riyadh-1"
compartment_ocid = "ocid1.compartment.oc1..example"
```

Do not push this file to GitHub because it may contain sensitive information.

## 4. .gitignore

Create `.gitignore`:

```text id="uzsrr2"
terraform.tfvars
.terraform/
*.tfstate
*.tfstate.backup
*.pem
```

This prevents secrets and Terraform state files from being uploaded to GitHub.

## 5. main.tf

Example: create a simple VCN.

```hcl id="xx9upe"
resource "oci_core_vcn" "dev_vcn" {
  compartment_id = var.compartment_ocid

  cidr_block   = "10.0.0.0/16"
  display_name = "dev-vcn"
  dns_label    = "devvcn"
}
```

This creates a Virtual Cloud Network in OCI.

## 6. outputs.tf

Outputs show useful information after Terraform finishes.

```hcl id="ao2ff7"
output "vcn_id" {
  value = oci_core_vcn.dev_vcn.id
}

output "vcn_name" {
  value = oci_core_vcn.dev_vcn.display_name
}
```

## Terraform Workflow

The basic Terraform workflow is:

```text id="b6se7k"
init → plan → apply → destroy
```

## 1. terraform init

```bash id="1emhmz"
terraform init
```

This downloads the OCI provider.

Run this once when starting a new Terraform project.

## 2. terraform plan

```bash id="3m95vy"
terraform plan
```

This shows what Terraform will create, change, or delete.

It does not create anything yet.

## 3. terraform apply

```bash id="14z5ho"
terraform apply
```

Terraform will ask for confirmation.

Type:

```text id="sqmc6z"
yes
```

Or apply directly:

```bash id="c23iqi"
terraform apply -auto-approve
```

## 4. terraform destroy

```bash id="cza0ha"
terraform destroy
```

This removes the resources created by Terraform.

Use carefully.

## Example Full Commands

```bash id="kezdxe"
mkdir oci-terraform-lab
cd oci-terraform-lab

touch provider.tf variables.tf main.tf outputs.tf terraform.tfvars .gitignore

terraform init
terraform plan
terraform apply
```

## Important OCI Authentication Values

Terraform needs these values to connect to OCI:

```text id="83wvoe"
tenancy_ocid
user_ocid
fingerprint
private_key_path
region
compartment_ocid
```

You usually get them from:

```text id="pitbyf"
OCI Console
Identity & Security
User settings
API Keys
Tenancy details
Compartment details
```

## What Is an OCID?

An **OCID** is a unique ID for OCI resources.

Examples:

```text id="t6yepi"
Tenancy OCID
User OCID
Compartment OCID
VCN OCID
Instance OCID
```

Terraform uses OCIDs to know exactly where to create resources.

## Simple VCN Project

```text id="ho0ta9"
Terraform
   │
   ▼
OCI VCN
   │
   ▼
Network for future resources
```

A VCN is usually the first resource you create before Compute Instances, Load Balancers, or databases.

## Terraform State

Terraform creates a state file:

```text id="rs7vbc"
terraform.tfstate
```

This file records what Terraform created.

Do not delete it randomly.

Do not upload it to GitHub.

The state file may contain sensitive information.

## Common Terraform Commands

Initialize project:

```bash id="fek2ee"
terraform init
```

Format files:

```bash id="qsjqe4"
terraform fmt
```

Validate syntax:

```bash id="dmeqtk"
terraform validate
```

Preview changes:

```bash id="yflstn"
terraform plan
```

Apply changes:

```bash id="wnhnpy"
terraform apply
```

Destroy resources:

```bash id="7j10mj"
terraform destroy
```

Show state:

```bash id="iwyja4"
terraform state list
```

## Common Mistakes

### Wrong Region

If the region is wrong, Terraform may fail or create resources in the wrong place.

Example:

```hcl id="aw3qls"
region = "me-riyadh-1"
```

### Wrong Compartment OCID

If the compartment OCID is wrong, Terraform may create resources in the wrong compartment or fail with permission errors.

### Missing API Key

If the private key or fingerprint is wrong, Terraform cannot authenticate with OCI.

### Uploading Sensitive Files

Do not upload:

```text id="a6llci"
terraform.tfvars
terraform.tfstate
private keys
.pem files
```

## Terraform with OCI Summary

```text id="vf5s4r"
Terraform      → Creates infrastructure using code
OCI Provider   → Allows Terraform to talk to Oracle Cloud
provider.tf    → Provider configuration
variables.tf   → Input variables
terraform.tfvars → Real values
main.tf        → Resources to create
outputs.tf     → Useful output values
state file     → Tracks created resources
```

> Terraform with OCI lets you build Oracle Cloud infrastructure using code instead of manual console steps.

