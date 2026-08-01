# 04 - Terraform Resources

A **resource** is the most important building block in Terraform.

Resources represent the actual infrastructure that Terraform creates and manages.

Examples include:

```text id="m4v8pk"
EC2 Instances
VPCs
Subnets
Security Groups
S3 Buckets
IAM Roles
```

If Terraform creates something in the cloud, it is usually defined as a resource.

```text id="p7r2xm"
Terraform
      │
      ▼
Resources
      │
      ▼
AWS Infrastructure
```

---

# Why Do We Need Resources?

Imagine you want to create:

```text id="g5k9tw"
One EC2 Instance
One VPC
One Security Group
```

Without Terraform, you would create each resource manually in the AWS Console.

With Terraform:

```text id="q8m3rv"
Terraform Code
       │
       ▼
AWS API
       │
       ▼
Resources Created Automatically
```

Everything can be created with code.

---

# Resource Syntax

Every resource follows the same structure.

```hcl id="d6x4pb"
resource "<RESOURCE_TYPE>" "<RESOURCE_NAME>" {

}
```

Explanation:

```text id="r3h7kw"
resource       → Terraform keyword

RESOURCE_TYPE  → Type of resource

RESOURCE_NAME  → Local name used by Terraform
```

Example:

```hcl id="y5v8mq"
resource "aws_instance" "web" {

}
```

---

# Resource Type

The resource type tells Terraform what to create.

Examples:

```text id="w9n2xr"
aws_instance

aws_vpc

aws_subnet

aws_security_group

aws_s3_bucket
```

Each resource type belongs to a provider.

---

# Resource Name

The resource name is used only inside Terraform.

Example:

```hcl id="t4k6pb"
resource "aws_instance" "web" {

}
```

Here:

```text id="n8q3vc"
Resource Type → aws_instance

Resource Name → web
```

Terraform references it as:

```text id="j7m5zt"
aws_instance.web
```

---

# Creating an EC2 Instance

Example:

```hcl id="u2r8hy"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

}
```

Terraform creates one EC2 instance.

---

# Creating a VPC

Example:

```hcl id="k5x9rv"
resource "aws_vpc" "main" {

  cidr_block = "10.0.0.0/16"

}
```

Terraform creates a Virtual Private Cloud.

---

# Creating a Subnet

Example:

```hcl id="a8p4wn"
resource "aws_subnet" "public" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

}
```

Notice:

```text id="m1q7tc"
aws_vpc.main.id
```

This references another Terraform resource.

---

# Resource Dependencies

Resources can depend on one another.

Example:

```text id="z4n8ph"
VPC
 │
 ▼
Subnet
 │
 ▼
EC2 Instance
```

Terraform automatically determines the correct creation order.

---

# Referencing Resources

Terraform allows one resource to reference another.

Example:

```hcl id="v6y2km"
resource "aws_subnet" "public" {

  vpc_id = aws_vpc.main.id

}
```

General format:

```text id="h9r5xt"
RESOURCE_TYPE.RESOURCE_NAME.ATTRIBUTE
```

Example:

```text id="c3w8pb"
aws_instance.web.public_ip

aws_vpc.main.id

aws_subnet.public.id
```

---

# Resource Attributes

Every resource has attributes.

Example EC2 attributes:

```text id="d7v2mn"
ID

Public IP

Private IP

Availability Zone
```

Example:

```hcl id="x5k9qr"
output "public_ip" {

  value = aws_instance.web.public_ip

}
```

Terraform displays the instance's public IP after deployment.

---

# Multiple Resources

A Terraform project usually contains many resources.

Example:

```text id="p2y6hc"
Provider
    │
    ▼
VPC
    │
    ▼
Subnet
    │
    ▼
Security Group
    │
    ▼
EC2 Instance
```

Terraform creates them in the correct order.

---

# Resource Lifecycle

Terraform manages resources throughout their lifecycle.

```text id="g8m4tv"
Terraform Apply
        │
        ▼
Create Resource
        │
Update Resource
        │
Destroy Resource
```

Terraform automatically tracks these changes using the state file.

---

# Example Project Structure

```text id="q6r3wx"
terraform/
├── provider.tf
├── network.tf
├── security.tf
├── compute.tf
├── variables.tf
└── outputs.tf
```

Resources are usually grouped by purpose.

Example:

```text id="l3x7mp"
network.tf

security.tf

compute.tf
```

---

# Common Resource Examples

EC2 Instance:

```hcl id="n5v8qy"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

}
```

Security Group:

```hcl id="b3y9cv"
resource "aws_security_group" "web" {

  name = "web-security-group"

  vpc_id = aws_vpc.main.id

}
```

S3 Bucket:

```hcl id="r6m1qx"
resource "aws_s3_bucket" "storage" {

  bucket = "my-terraform-demo-bucket"

}
```

---

# Common Beginner Mistakes

### Using Duplicate Resource Names

Bad:

```hcl id="z2n8hf"
resource "aws_instance" "web" {
}

resource "aws_instance" "web" {
}
```

Resource names must be unique within a module.

---

### Hardcoding Everything

Bad:

```hcl id="k4v7mb"
instance_type = "t3.micro"
```

Better:

```hcl id="t9q2wy"
instance_type = var.instance_type
```

---

### Forgetting Resource References

Bad:

```hcl id="x8m3rh"
vpc_id = "vpc-123456"
```

Better:

```hcl id="y5j7ps"
vpc_id = aws_vpc.main.id
```

This allows Terraform to track dependencies automatically.

---

### Creating Resources Manually

If you create infrastructure outside Terraform, Terraform cannot manage it unless it is imported.

Prefer creating resources through Terraform.

---

### Poor Resource Names

Good:

```text id="e4c8nt"
web

database

public

private
```

Avoid:

```text id="u6p9ax"
test

resource1

abc
```

Use descriptive names.

---

# Best Practices

```text id="w1r4kb"
Use descriptive resource names
Group resources into separate files
Reference resources instead of hardcoding IDs
Use variables for configurable values
Keep one responsibility per resource
```

---

# Useful Commands

Initialize Terraform:

```bash id="q7m2vd"
terraform init
```

Review changes:

```bash id="p5x8cy"
terraform plan
```

Deploy infrastructure:

```bash id="l8n6ft"
terraform apply
```

Show infrastructure:

```bash id="c2y5hq"
terraform show
```

Destroy infrastructure:

```bash id="m3k8pv"
terraform destroy
```

---

# Summary

```text id="a6v4rz"
Resource → Infrastructure object
resource → Terraform keyword
Resource Type → What Terraform creates
Resource Name → Local Terraform identifier
Attributes → Resource properties
References → Connect resources together
```

> Resources are the core building blocks of Terraform. They define the cloud infrastructure Terraform creates, manages, updates, and deletes, allowing infrastructure to be described and maintained entirely as code.

