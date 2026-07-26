# 09 - Terraform Count and for_each

Terraform often needs to create multiple similar resources.

Instead of copying the same resource many times, Terraform provides two meta-arguments:

```text id="m4v8xp"
count
for_each
```

Both allow Terraform to create multiple resources automatically, but they work in different ways.

```text id="p7r3yn"
Terraform
     │
     ├── count
     │
     └── for_each
```

---

# Why Do We Need Them?

Imagine you need three EC2 instances.

Without `count`:

```hcl id="a1b2c3"
resource "aws_instance" "web1" {}

resource "aws_instance" "web2" {}

resource "aws_instance" "web3" {}
```

This creates unnecessary duplication.

With `count`:

```hcl id="d4e5f6"
resource "aws_instance" "web" {

  count = 3

}
```

Terraform automatically creates three instances.

---

# What Is count?

`count` creates multiple copies of the same resource using a number.

Example:

```hcl id="g7h8i9"
resource "aws_instance" "web" {

  count = 3

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"
}
```

Terraform creates:

```text id="j1k2l3"
aws_instance.web[0]

aws_instance.web[1]

aws_instance.web[2]
```

---

# How count Works

```text id="m5n6o7"
count = 3

        │
        ▼

0

1

2
```

Terraform assigns an index starting from zero.

---

# Using count.index

Each resource has an index.

Example:

```hcl id="p8q9r0"
resource "aws_instance" "web" {

  count = 3

  tags = {
    Name = "web-${count.index}"
  }

}
```

Terraform creates:

```text id="s1t2u3"
web-0

web-1

web-2
```

---

# count with Variables

Instead of hardcoding:

```hcl id="v4w5x6"
count = 3
```

Use a variable:

```hcl id="y7z8a9"
variable "instance_count" {

  default = 3

}
```

Then:

```hcl id="b2c3d4"
count = var.instance_count
```

This makes the configuration reusable.

---

# Example Project

```text id="e5f6g7"
Terraform
      │
      ▼
count = 3
      │
      ▼
EC2 #1

EC2 #2

EC2 #3
```

---

# Limitations of count

Suppose:

```text id="h8i9j0"
web-0

web-1

web-2
```

You remove the second instance.

Terraform may need to recreate resources because the indexes change.

```text id="k1l2m3"
Before

0
1
2

After

0
1
```

This can cause unnecessary replacements.

---

# What Is for_each?

`for_each` creates resources from a collection.

Instead of indexes, each resource has its own key.

Example:

```hcl id="n4o5p6"
resource "aws_instance" "web" {

  for_each = toset([
    "frontend",
    "backend",
    "monitoring"
  ])

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

  tags = {
    Name = each.key
  }

}
```

Terraform creates:

```text id="q7r8s9"
frontend

backend

monitoring
```

---

# How for_each Works

```text id="t1u2v3"
frontend

backend

monitoring
        │
        ▼
One Resource Per Key
```

Each key uniquely identifies a resource.

---

# Using each.key

Example:

```hcl id="w4x5y6"
tags = {

  Name = each.key

}
```

Terraform generates:

```text id="z7a8b9"
frontend

backend

monitoring
```

---

# Using each.value

`for_each` also works with maps.

Example:

```hcl id="c1d2e3"
locals {

  instances = {

    web = "t3.micro"

    api = "t3.small"

    db = "t3.medium"

  }

}
```

Resource:

```hcl id="f4g5h6"
resource "aws_instance" "servers" {

  for_each = local.instances

  instance_type = each.value

  tags = {
    Name = each.key
  }

}
```

Terraform creates:

```text id="i7j8k9"
web → t3.micro

api → t3.small

db → t3.medium
```

---

# count vs for_each

| Feature          | count               | for_each        |
| ---------------- | ------------------- | --------------- |
| Uses             | Number              | Collection      |
| Identifier       | Index               | Key             |
| Best For         | Identical resources | Named resources |
| Resource Address | web[0]              | web["frontend"] |

---

# Which One Should You Use?

Use **count** when resources are identical.

Example:

```text id="l1m2n3"
Three identical EC2 instances
```

Use **for_each** when resources have unique names or configurations.

Example:

```text id="o4p5q6"
frontend

backend

database
```

---

# Example Project Structure

```text id="r7s8t9"
terraform/
├── provider.tf
├── network.tf
├── compute.tf
├── variables.tf
└── outputs.tf
```

`count` and `for_each` are commonly used inside:

```text id="u1v2w3"
compute.tf

network.tf
```

---

# Common Beginner Mistakes

### Using count for Named Resources

Bad:

```text id="x4y5z6"
web[0]

web[1]

web[2]
```

Better:

```text id="a7b8c9"
frontend

backend

database
```

using `for_each`.

---

### Mixing count and for_each

A single resource cannot use both.

Bad:

```hcl id="d1e2f3"
resource "aws_instance" "web" {

  count = 2

  for_each = {}

}
```

Choose only one.

---

### Forgetting count.index

When using `count`, access the current index with:

```hcl id="g4h5i6"
count.index
```

---

### Forgetting each.key

When using `for_each`, use:

```hcl id="j7k8l9"
each.key
```

or:

```hcl id="m1n2o3"
each.value
```

depending on the collection type.

---

### Using Lists with Duplicate Values

`for_each` requires unique keys.

Bad:

```text id="p4q5r6"
web

web

api
```

Keys must be unique.

---

# Best Practices

```text id="s7t8u9"
Use count for identical resources
Use for_each for named resources
Prefer variables over hardcoded values
Use meaningful resource names
Avoid unnecessary duplication
```

---

# Useful Commands

Initialize Terraform:

```bash id="v1w2x3"
terraform init
```

Review changes:

```bash id="y4z5a6"
terraform plan
```

Deploy infrastructure:

```bash id="b7c8d9"
terraform apply
```

Show infrastructure:

```bash id="e1f2g3"
terraform show
```

Destroy infrastructure:

```bash id="h4i5j6"
terraform destroy
```

---

# Summary

```text id="k7l8m9"
count → Creates resources using numbers
count.index → Current resource index
for_each → Creates resources from collections
each.key → Resource key
each.value → Resource value
count → Best for identical resources
for_each → Best for named resources
```

> `count` and `for_each` are Terraform meta-arguments that automate the creation of multiple resources. Use `count` for identical resources and `for_each` when each resource has its own unique identity or configuration.

