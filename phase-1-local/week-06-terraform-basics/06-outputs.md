# 06 - Terraform Outputs

Terraform creates infrastructure such as EC2 instances, VPCs, and Security Groups.

After creating these resources, you often need information about them.

For example:

```text id="p8m4vr"
Public IP Address
VPC ID
Subnet ID
Security Group ID
Instance ID
```

Terraform provides this information using **Outputs**.

```text id="g7k2mx"
Terraform
      │
Creates Resources
      │
      ▼
Outputs
      │
      ▼
Display Important Information
```

---

# Why Do We Need Outputs?

Imagine Terraform creates an EC2 instance.

```text id="w5r8hn"
EC2 Instance

Public IP:
54.xxx.xxx.xxx
```

Without outputs, you would have to find the IP address manually in the AWS Console.

With outputs:

```bash id="v6p2yt"
terraform apply
```

Terraform displays:

```text id="q3m7kx"
web_public_ip = "54.xxx.xxx.xxx"
```

This saves time and makes automation easier.

---

# Creating an Output

Outputs are usually stored in:

```text id="k9v4np"
outputs.tf
```

Example:

```hcl id="d2x7qb"
output "instance_id" {

  value = aws_instance.web.id
}
```

After:

```bash id="a8m5tr"
terraform apply
```

Terraform displays:

```text id="h4y6wp"
instance_id = "i-0123456789abcdef0"
```

---

# Output Workflow

```text id="f7r2mz"
Terraform
      │
Creates Resource
      │
      ▼
Output Value
      │
      ▼
Displayed to User
```

Outputs are generated automatically after a successful apply.

---

# Displaying a Public IP

Example:

```hcl id="j6n8vc"
output "public_ip" {

  value = aws_instance.web.public_ip
}
```

Terraform output:

```text id="r5q1kd"
public_ip = "54.xxx.xxx.xxx"
```

You can immediately use this IP to connect to the server.

---

# Multiple Outputs

You can create as many outputs as needed.

Example:

```hcl id="m3w9py"
output "instance_id" {

  value = aws_instance.web.id
}

output "public_ip" {

  value = aws_instance.web.public_ip
}

output "vpc_id" {

  value = aws_vpc.main.id
}
```

Terraform displays each output after applying the configuration.

---

# Using Descriptions

Outputs can include descriptions.

Example:

```hcl id="x2h7vr"
output "public_ip" {

  description = "Public IP address of the EC2 instance"

  value = aws_instance.web.public_ip
}
```

Descriptions help document the purpose of each output.

---

# Sensitive Outputs

Some outputs contain confidential information.

Example:

```hcl id="u5m8qx"
output "database_password" {

  value = var.db_password

  sensitive = true
}
```

Terraform hides sensitive outputs:

```text id="n7k4pb"
database_password = (sensitive value)
```

This helps prevent accidental exposure.

---

# Viewing Outputs

After deploying infrastructure:

```bash id="y8p3mc"
terraform output
```

Example:

```text id="z6r1wt"
instance_id = "i-0123456789abcdef0"

public_ip = "54.xxx.xxx.xxx"
```

---

# Viewing One Output

Retrieve a single output:

```bash id="b4v7qn"
terraform output public_ip
```

Example:

```text id="e9m2ks"
54.xxx.xxx.xxx
```

---

# JSON Output

Terraform can return outputs as JSON.

```bash id="q8r5vx"
terraform output -json
```

Example:

```json id="l2x9tp"
{
  "public_ip": {
    "value": "54.xxx.xxx.xxx"
  }
}
```

This is useful for automation and scripts.

---

# Example Project Structure

```text id="c5p8wn"
terraform/
├── provider.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── compute.tf
└── security.tf
```

Outputs are typically stored in:

```text id="t4y6mq"
outputs.tf
```

---

# Common Output Examples

```hcl id="g1n5rv"
output "vpc_id" {

  value = aws_vpc.main.id
}

output "subnet_id" {

  value = aws_subnet.public.id
}

output "security_group_id" {

  value = aws_security_group.web.id
}

output "instance_public_ip" {

  value = aws_instance.web.public_ip
}
```

These outputs make it easy to reference important resources after deployment.

---

# Outputs and State

Terraform stores output values inside the state file.

```text id="p7w3zx"
Terraform State
       │
       ▼
Outputs
```

When resources change, Terraform automatically updates the outputs.

---

# Common Beginner Mistakes

### Forgetting Outputs

Without outputs, you may need to manually search for resource IDs or IP addresses.

---

### Outputting Sensitive Data

Bad:

```hcl id="k8q4hm"
output "password" {

  value = var.password
}
```

Better:

```hcl id="r3v6nt"
output "password" {

  value = var.password

  sensitive = true
}
```

---

### Wrong Resource Reference

Bad:

```hcl id="j9m5qy"
value = aws_instance.server.public_ip
```

if the resource is actually named:

```hcl id="v2x7pk"
resource "aws_instance" "web" {
}
```

Use:

```hcl id="f6n3wc"
value = aws_instance.web.public_ip
```

---

### Using Outputs Before Apply

Outputs are available only after Terraform creates the resources.

---

### Storing Secrets in Git

Sensitive outputs may still exist in the Terraform state file.

Protect your state file and avoid exposing secrets.

---

# Best Practices

```text id="w8p2kr"
Store outputs in outputs.tf
Use descriptive output names
Add descriptions
Mark secrets as sensitive
Output only useful information
Keep state files secure
```

---

# Useful Commands

Initialize Terraform:

```bash id="n5r8yt"
terraform init
```

Review changes:

```bash id="h2v4qm"
terraform plan
```

Deploy infrastructure:

```bash id="m7x3pc"
terraform apply
```

Show all outputs:

```bash id="a4q9vz"
terraform output
```

Show one output:

```bash id="u6k1rn"
terraform output public_ip
```

Show outputs as JSON:

```bash id="d9p5wb"
terraform output -json
```

Destroy infrastructure:

```bash id="c3m7hx"
terraform destroy
```

---

# Summary

```text id="t8v4py"
Outputs → Display useful resource information
outputs.tf → Stores output definitions
terraform output → Show all outputs
terraform output NAME → Show one output
terraform output -json → JSON format
sensitive = true → Hide confidential values
```

> Terraform Outputs expose useful information about the infrastructure Terraform creates, making it easy to retrieve resource IDs, IP addresses, and other important values for use by users, scripts, or other Terraform configurations.

