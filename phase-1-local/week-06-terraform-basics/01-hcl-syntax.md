# 01 - HCL Syntax

Terraform uses a language called **HCL (HashiCorp Configuration Language)**.

HCL is a human-readable configuration language used to describe infrastructure as code.

Instead of clicking through a cloud console, you define your infrastructure in HCL files, and Terraform creates it automatically.

```text id="m4v8pk"
HCL Code
    │
    ▼
Terraform
    │
    ▼
Cloud Infrastructure
```

HCL is designed to be simple, readable, and easy to maintain.

---

# Why Do We Need HCL?

Imagine creating an EC2 instance manually.

You would need to:

```text id="p7r2xm"
Open the AWS Console
Choose an AMI
Select an instance type
Configure networking
Create security rules
Launch the instance
```

Instead, you can describe the infrastructure once using HCL.

Example:

```hcl id="g5k9tw"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

}
```

Terraform reads the HCL configuration and creates the infrastructure automatically.

---

# HCL File Extension

Terraform configuration files use the:

```text id="q8m3rv"
.tf
```

extension.

Common examples:

```text id="d6x4pb"
provider.tf

variables.tf

network.tf

compute.tf

outputs.tf
```

Terraform automatically loads all `.tf` files in the current directory.

---

# Basic Structure

HCL is made of **blocks**.

General syntax:

```hcl id="r3h7kw"
BLOCK_TYPE "LABEL1" "LABEL2" {

}
```

Example:

```hcl id="y5v8mq"
resource "aws_instance" "web" {

}
```

Explanation:

```text id="w9n2xr"
resource → Block type

aws_instance → Resource type

web → Resource name
```

---

# Arguments

Blocks contain **arguments**.

Example:

```hcl id="t4k6pb"
resource "aws_instance" "web" {

  instance_type = "t3.micro"

}
```

Here:

```text id="n8q3vc"
instance_type → Argument

t3.micro → Value
```

Arguments configure the behavior of a block.

---

# Strings

Text values are enclosed in quotation marks.

Example:

```hcl id="j7m5zt"
region = "us-east-1"
```

Examples:

```text id="u2r8hy"
"Development"

"Terraform"

"t3.micro"
```

---

# Numbers

Numbers are written without quotes.

Example:

```hcl id="k5x9rv"
volume_size = 30
```

Examples:

```text id="a8p4wn"
1

10

100
```

---

# Booleans

Boolean values are either:

```text id="m1q7tc"
true

false
```

Example:

```hcl id="z4n8ph"
associate_public_ip_address = true
```

---

# Lists

Lists store multiple values.

Example:

```hcl id="v6y2km"
availability_zones = [

  "us-east-1a",

  "us-east-1b"

]
```

Terraform processes each item in the list.

---

# Maps

Maps store key-value pairs.

Example:

```hcl id="h9r5xt"
tags = {

  Environment = "Development"

  Project = "Terraform Lab"

}
```

Maps are commonly used for resource tags.

---

# Comments

Single-line comment:

```hcl id="c3w8pb"
# Create the web server
```

or:

```hcl id="d7v2mn"
// Create the web server
```

Multi-line comment:

```hcl id="x5k9qr"
/*
Create the
web server
*/
```

Comments improve readability and documentation.

---

# References

HCL allows one resource to reference another.

Example:

```hcl id="p2y6hc"
vpc_id = aws_vpc.main.id
```

General format:

```text id="g8m4tv"
RESOURCE_TYPE.RESOURCE_NAME.ATTRIBUTE
```

Example:

```text id="q6r3wx"
aws_instance.web.public_ip

aws_vpc.main.id

aws_subnet.public.id
```

---

# Variables

Variables make HCL reusable.

Declaration:

```hcl id="l3x7mp"
variable "instance_type" {

  default = "t3.micro"

}
```

Usage:

```hcl id="n5v8qy"
instance_type = var.instance_type
```

---

# Outputs

Outputs display useful information after deployment.

Example:

```hcl id="b3y9cv"
output "public_ip" {

  value = aws_instance.web.public_ip

}
```

Terraform displays the instance's public IP after deployment.

---

# Functions

HCL includes built-in functions.

Example:

```hcl id="r6m1qx"
file("startup.sh")
```

Reads the contents of a file.

Example:

```hcl id="z2n8hf"
length(var.subnets)
```

Returns the number of items in a list.

---

# Example Terraform File

```hcl id="k4v7mb"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

  tags = {

    Name = "Web Server"

  }

}
```

This HCL configuration creates an EC2 instance with a tag.

---

# Example Project Structure

```text id="t9q2wy"
terraform/
├── provider.tf
├── versions.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

Terraform reads all `.tf` files together as one configuration.

---

# Common Beginner Mistakes

### Forgetting Quotes

Bad:

```hcl id="x8m3rh"
region = us-east-1
```

Correct:

```hcl id="y5j7ps"
region = "us-east-1"
```

---

### Incorrect Braces

Every block must have matching braces.

Bad:

```hcl id="e4c8nt"
resource "aws_vpc" "main" {
```

Correct:

```hcl id="u6p9ax"
resource "aws_vpc" "main" {

}
```

---

### Using Tabs and Inconsistent Formatting

Run:

```bash id="w1r4kb"
terraform fmt
```

to automatically format HCL files.

---

### Hardcoding Values

Bad:

```hcl id="q7m2vd"
instance_type = "t3.micro"
```

Better:

```hcl id="p5x8cy"
instance_type = var.instance_type
```

---

### Poor Naming

Good:

```text id="l8n6ft"
web

database

public
```

Avoid:

```text id="c2y5hq"
x

test

resource1
```

Use descriptive names.

---

# Best Practices

```text id="m3k8pv"
Use terraform fmt regularly
Keep one purpose per file
Use variables instead of hardcoded values
Use meaningful names
Add comments when necessary
Group related resources together
```

---

# Useful Commands

Format configuration:

```bash id="a6v4rz"
terraform fmt
```

Validate syntax:

```bash id="k8m5pw"
terraform validate
```

Initialize Terraform:

```bash id="r2v7nx"
terraform init
```

Review changes:

```bash id="y4q3mt"
terraform plan
```

Deploy infrastructure:

```bash id="n9x6pk"
terraform apply
```

---

# Summary

```text id="b7v3pn"
HCL → HashiCorp Configuration Language
.tf → Terraform configuration file
Blocks → Main building blocks
Arguments → Configure blocks
Variables → Reusable values
Outputs → Display resource information
References → Connect resources
terraform fmt → Format HCL code
```

> HCL (HashiCorp Configuration Language) is Terraform's configuration language. It provides a simple, human-readable way to describe infrastructure as code, making cloud resources easy to create, manage, and maintain.

