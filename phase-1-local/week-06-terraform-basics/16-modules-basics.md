# 16 - Terraform Modules Basics

A **Terraform module** is a reusable collection of Terraform resources.

Instead of writing the same infrastructure multiple times, you write it once inside a module and reuse it whenever needed.

```text id="k1p3a8"
Without Modules
---------------
main.tf
├── VCN
├── Subnet
├── Internet Gateway
├── Route Table
├── Security List
├── Compute Instance

Copied again...
Copied again...
Copied again...

With Modules
------------
modules/
├── network/
└── compute/

main.tf
├── module.network
└── module.compute
```

## Why Do We Need Modules?

Imagine you need to create:

```text id="r5g8nq"
Development environment
Testing environment
Production environment
```

Without modules, you may copy hundreds of lines of Terraform code.

With modules:

```text id="b4y6mz"
Write once
Reuse many times
```

Benefits:

```text id="w2f9ht"
Less duplicated code
Easier maintenance
Cleaner projects
Reusable infrastructure
```

---

# What Is a Module?

A module is simply a folder containing Terraform files.

Example:

```text id="c7l2vn"
modules/
└── network/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

Terraform automatically treats this folder as a module.

---

# Root Module vs Child Module

Every Terraform project has one **root module**.

Example:

```text id="m8q3kr"
terraform/
├── main.tf
├── variables.tf
└── outputs.tf
```

When you create another module inside `modules/`, it becomes a **child module**.

Example:

```text id="n6x4we"
terraform/
├── main.tf
└── modules/
    └── network/
```

```text id="h3r8zs"
Root Module
     │
     ▼
Child Module
```

---

# Typical Project Structure

```text id="p2k7ua"
terraform/
├── main.tf
├── provider.tf
├── variables.tf
├── outputs.tf
└── modules/
    ├── network/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    └── compute/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

# Example Network Module

Directory:

```text id="d5v1cl"
modules/
└── network/
```

Inside `main.tf`:

```hcl id="f9j2wa"
resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_id
  cidr_blocks    = [var.vcn_cidr]
  display_name   = var.vcn_name
}
```

Variables:

```hcl id="y4u8ms"
variable "compartment_id" {}

variable "vcn_name" {}

variable "vcn_cidr" {}
```

Outputs:

```hcl id="g6e0tr"
output "vcn_id" {
  value = oci_core_vcn.main.id
}
```

---

# Calling a Module

From the root module:

```hcl id="v7s3ld"
module "network" {
  source = "./modules/network"

  compartment_id = var.compartment_id
  vcn_name       = "dev-vcn"
  vcn_cidr       = "10.0.0.0/16"
}
```

Terraform now creates everything inside the module.

---

# Understanding source

The `source` argument tells Terraform where the module is located.

Local module:

```hcl id="z8c5nr"
source = "./modules/network"
```

Parent directory:

```hcl id="o3m1xy"
source = "../modules/network"
```

Terraform Registry:

```hcl id="s9q6eh"
source = "terraform-oci-modules/vcn/oci"
```

Git repository:

```hcl id="l5d7pb"
source = "git::https://github.com/example/modules.git//network"
```

---

# Passing Variables to Modules

Modules accept input variables.

Root module:

```hcl id="e4j2mv"
module "network" {
  source = "./modules/network"

  compartment_id = var.compartment_id
  vcn_name       = "production-vcn"
  vcn_cidr       = "10.0.0.0/16"
}
```

Inside module:

```hcl id="a7t5uk"
variable "vcn_name" {}
```

Terraform passes the value into the module.

---

# Using Module Outputs

Modules can return values.

Module output:

```hcl id="m2n8fv"
output "vcn_id" {
  value = oci_core_vcn.main.id
}
```

Root module:

```hcl id="t6q1rz"
output "network_id" {
  value = module.network.vcn_id
}
```

Notice:

```text id="u4w9ld"
module.network.vcn_id
```

Terraform uses:

```text id="x1h6pg"
module
   ↓
Module name
   ↓
Output name
```

---

# Connecting Modules Together

Modules often depend on one another.

Example:

```text id="v3y8nk"
Network Module
      │
      ▼
Creates VCN
      │
Outputs VCN ID
      │
      ▼
Compute Module
```

Network module:

```hcl id="j5m7ds"
output "subnet_id" {
  value = oci_core_subnet.public.id
}
```

Root module:

```hcl id="q4n1wb"
module "compute" {
  source = "./modules/compute"

  subnet_id = module.network.subnet_id
}
```

Now the compute module automatically uses the subnet created by the network module.

---

# Example OCI Project

```text id="k8v4qe"
terraform/
│
├── provider.tf
├── variables.tf
├── outputs.tf
│
└── modules/
    ├── network/
    │
    │   Creates:
    │   • VCN
    │   • Subnet
    │   • Internet Gateway
    │   • Route Table
    │
    └── compute/
        Creates:
        • Compute Instance
        • VNIC
```

Root module:

```hcl id="w5f3ba"
module "network" {
  source = "./modules/network"
}

module "compute" {
  source = "./modules/compute"

  subnet_id = module.network.public_subnet_id
}
```

---

# Reusing the Same Module

One module can be used multiple times.

Example:

```hcl id="h7j2vx"
module "development_network" {
  source = "./modules/network"

  vcn_name = "dev-vcn"
  vcn_cidr = "10.0.0.0/16"
}
```

Another:

```hcl id="n2u5qm"
module "production_network" {
  source = "./modules/network"

  vcn_name = "prod-vcn"
  vcn_cidr = "172.16.0.0/16"
}
```

Same module.

Different infrastructure.

---

# Module Inputs

Inputs are variables.

Example:

```hcl id="y6k1nt"
variable "instance_shape" {
  type = string
}
```

Passed from root module:

```hcl id="e5r7az"
module "compute" {
  source = "./modules/compute"

  instance_shape = "VM.Standard.E2.1.Micro"
}
```

---

# Module Outputs

Outputs expose useful values.

Example:

```hcl id="s1w8qo"
output "public_ip" {
  value = oci_core_instance.web.public_ip
}
```

Root module:

```hcl id="b3x2pf"
output "server_ip" {
  value = module.compute.public_ip
}
```

---

# Module Dependency

Terraform automatically understands dependencies.

Example:

```text id="r9m4vu"
Network Module
      │
Creates subnet
      │
Outputs subnet_id
      │
      ▼
Compute Module
```

Because:

```hcl id="k2d7oq"
subnet_id = module.network.subnet_id
```

Terraform knows:

```text id="x6e9ha"
Create network first
Create compute second
```

---

# Best Practices

## Keep Modules Small

Bad:

```text id="j4p7ul"
One module creates everything
```

Better:

```text id="o8r1kt"
Network module
Compute module
Storage module
Security module
```

---

## Keep Modules Reusable

Bad:

```hcl id="d7v6ab"
display_name = "My Personal Server"
```

Better:

```hcl id="t3q5lw"
display_name = var.instance_name
```

---

## Use Variables

Avoid hardcoded values.

Bad:

```hcl id="x5m8rz"
cidr_blocks = ["10.0.0.0/16"]
```

Better:

```hcl id="n9j4ec"
cidr_blocks = [var.vcn_cidr]
```

---

## Return Useful Outputs

Examples:

```text id="h6u3yb"
VCN ID
Subnet ID
Public IP
Private IP
Instance ID
```

Avoid outputs that nobody uses.

---

## Document Modules

Each module should have:

```text id="z7p2mk"
Purpose
Required variables
Outputs
Example usage
```

---

# Common Beginner Mistakes

### Copying Resources Instead of Using Modules

Bad:

```text id="l1n4gw"
Same VCN code copied 5 times
```

Better:

```text id="q8s6yb"
One reusable module
```

---

### Hardcoding Values

Bad:

```hcl id="m5v9rc"
display_name = "Server1"
```

Better:

```hcl id="k7w1zn"
display_name = var.instance_name
```

---

### Forgetting Outputs

Without outputs, other modules cannot reuse resources.

Always expose important IDs.

---

### Making Modules Too Large

Bad:

```text id="u2f8eq"
500-line module
```

Better:

```text id="v9x5ta"
Several focused modules
```

---

### Ignoring Documentation

Another developer should understand how to use your module without reading all the code.

---

# Typical OCI Module Structure

```text id="g5r1wp"
modules/
├── network/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── compute/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── security/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── storage/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

# Useful Commands

Initialize modules:

```bash id="m8d4qs"
terraform init
```

Validate configuration:

```bash id="a2k9vc"
terraform validate
```

Review execution plan:

```bash id="e7r3jt"
terraform plan
```

Deploy infrastructure:

```bash id="c5u6qx"
terraform apply
```

View outputs:

```bash id="r1n8zw"
terraform output
```

---

# Summary

```text id="f4w6yu"
Module = Reusable Terraform code
Root module = Main Terraform project
Child module = Reusable module
source = Module location
Variables = Module inputs
Outputs = Module results
Modules reduce duplication
Modules improve organization
Modules make infrastructure reusable
```

> Terraform modules let you organize infrastructure into reusable building blocks, making your code cleaner, easier to maintain, and scalable across multiple environments.

