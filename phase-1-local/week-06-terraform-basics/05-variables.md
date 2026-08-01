# 05 - Terraform Variables

Terraform variables allow you to make your infrastructure code **flexible**, **reusable**, and **easy to maintain**.

Instead of hardcoding values inside your Terraform configuration, you can store them in variables.

```text id="m4x8kp"
Hardcoded Values
        │
        ▼
Terraform Variables
        │
        ▼
Reusable Configuration
```

Variables are one of the most important features in Terraform.

---

# Why Do We Need Variables?

Imagine creating an EC2 instance.

Without variables:

```hcl id="p7v2hn"
resource "aws_instance" "web" {

  instance_type = "t3.micro"

}
```

If you later want:

```text id="g5r9mx"
t3.small

t3.medium

t3.large
```

You must edit the code every time.

With variables:

```hcl id="q8m3yt"
instance_type = var.instance_type
```

Only the variable value changes.

The Terraform code remains the same.

---

# Declaring a Variable

Variables are usually stored in:

```text id="d6x4pw"
variables.tf
```

Example:

```hcl id="r3h7kn"
variable "instance_type" {

  type = string

}
```

Explanation:

```text id="y5v8mq"
variable → Declares a variable

instance_type → Variable name

type → Data type
```

---

# Using a Variable

Variables are accessed using:

```text id="w9n2xr"
var.variable_name
```

Example:

```hcl id="t4k6pb"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = var.instance_type

}
```

Terraform replaces:

```text id="n8q3vc"
var.instance_type
```

with the actual value.

---

# Variable Workflow

```text id="j7m5zt"
Declare Variable
        │
        ▼
Assign Value
        │
        ▼
Use Variable
```

Example:

```text id="u2r8hy"
variables.tf

↓

terraform.tfvars

↓

compute.tf
```

---

# Variable Types

Terraform supports multiple data types.

### String

```hcl id="k5x9rv"
variable "region" {

  type = string

}
```

Example value:

```text id="a8p4wn"
us-east-1
```

---

### Number

```hcl id="m1q7tc"
variable "instance_count" {

  type = number

}
```

Example:

```text id="z4n8ph"
3
```

---

### Boolean

```hcl id="v6y2km"
variable "enable_monitoring" {

  type = bool

}
```

Example:

```text id="h9r5xt"
true
```

---

### List

```hcl id="c3w8pb"
variable "availability_zones" {

  type = list(string)

}
```

Example:

```text id="d7v2mn"
[
  "us-east-1a",
  "us-east-1b"
]
```

---

### Map

```hcl id="x5k9qr"
variable "tags" {

  type = map(string)

}
```

Example:

```text id="p2y6hc"
{
  Environment = "Development"
  Project     = "Terraform Lab"
}
```

---

# Default Values

Variables can have default values.

Example:

```hcl id="g8m4tv"
variable "instance_type" {

  type = string

  default = "t3.micro"

}
```

If no value is provided, Terraform uses the default.

---

# Required Variables

Variables without a default value are required.

Example:

```hcl id="q6r3wx"
variable "aws_region" {

  type = string

}
```

Terraform asks for a value if none is provided.

---

# Assigning Variable Values

Values can be assigned in several ways.

Example using:

```text id="l3x7mp"
terraform.tfvars
```

```hcl id="n5v8qy"
instance_type = "t3.micro"

aws_region = "us-east-1"
```

Terraform automatically loads this file.

---

# Command-Line Variables

Variables can also be provided directly.

Example:

```bash id="f4r9zw"
terraform apply -var="instance_type=t3.small"
```

This overrides the default value.

---

# Sensitive Variables

Some variables contain confidential information.

Example:

```hcl id="k2m6px"
variable "db_password" {

  type = string

  sensitive = true

}
```

Terraform hides sensitive values in its output.

---

# Example Project Structure

```text id="w8p5nr"
terraform/
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

Variables are usually declared in:

```text id="c7v3qy"
variables.tf
```

---

# Using Variables for Tags

Example:

```hcl id="j4x9hm"
variable "project_name" {

  default = "Terraform Lab"

}
```

Resource:

```hcl id="e5n2kp"
tags = {

  Name = var.project_name

}
```

Terraform creates resources with dynamic tag values.

---

# Variable Naming

Good variable names:

```text id="m9r4tv"
aws_region

instance_type

project_name

environment
```

Avoid vague names like:

```text id="y6q8hc"
x

value

test
```

Choose names that clearly describe their purpose.

---

# Common Beginner Mistakes

### Hardcoding Values

Bad:

```hcl id="r7w3nb"
instance_type = "t3.micro"
```

Better:

```hcl id="a2k9xp"
instance_type = var.instance_type
```

---

### Forgetting var.

Bad:

```hcl id="u8m4cy"
instance_type = instance_type
```

Correct:

```hcl id="b5r7hv"
instance_type = var.instance_type
```

---

### Using the Wrong Data Type

Example:

```hcl id="q3n8zt"
variable "instance_count" {

  type = number

}
```

Do not assign:

```text id="h6v2pm"
"three"
```

Use:

```text id="x9r5wk"
3
```

---

### Storing Secrets in Git

Avoid committing passwords or API keys.

Use:

```text id="f2k8mq"
Sensitive variables

Environment variables

GitHub Secrets
```

instead.

---

### Poor Variable Names

Use descriptive names that make the configuration easier to understand.

---

# Best Practices

```text id="z7m4pv"
Declare variables in variables.tf
Use descriptive names
Use defaults when appropriate
Mark secrets as sensitive
Avoid hardcoded values
Reuse variables across resources
```

---

# Useful Commands

Initialize Terraform:

```bash id="c6v9rx"
terraform init
```

Review changes:

```bash id="g4m2kw"
terraform plan
```

Provide a variable:

```bash id="t8q5hp"
terraform apply -var="instance_type=t3.small"
```

Deploy infrastructure:

```bash id="y3n7vc"
terraform apply
```

Destroy infrastructure:

```bash id="k5x8mr"
terraform destroy
```

---

# Summary

```text id="v1q6pt"
Variables → Reusable values
variables.tf → Declares variables
var.name → Access a variable
default → Default value
type → Variable data type
sensitive = true → Protect confidential values
```

> Terraform variables make infrastructure code reusable, configurable, and easier to maintain by separating configuration values from the Terraform resources that use them.

