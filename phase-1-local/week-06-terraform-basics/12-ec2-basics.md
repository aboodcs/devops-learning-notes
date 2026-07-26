# 12 - AWS EC2 Basics

Amazon **EC2 (Elastic Compute Cloud)** is one of the core AWS services.

EC2 allows you to launch virtual machines in the AWS cloud.

Instead of buying physical servers, AWS provides virtual servers that you can create, stop, start, and terminate whenever you need.

```text id="r4m8vp"
Your Computer
      │
      ▼
AWS Cloud
      │
      ▼
EC2 Instance
```

---

# Why Do We Need EC2?

Imagine you want to host:

```text id="f7p2wh"
A website
A REST API
A Docker application
A Kubernetes node
A Jenkins server
A database
```

Instead of purchasing hardware, you can launch an EC2 instance within minutes.

Benefits:

```text id="g2v8rn"
Scalable
Pay only for what you use
Easy to manage
Available in multiple regions
Highly reliable
```

---

# What Is an EC2 Instance?

An EC2 instance is simply a virtual machine running in AWS.

It includes:

```text id="q8y3kt"
Operating System
CPU
Memory (RAM)
Storage
Network Interface
Public or Private IP
```

Example:

```text id="w1c9hz"
EC2 Instance
├── Ubuntu Linux
├── 2 vCPUs
├── 4 GB RAM
├── 30 GB EBS Storage
└── Public IP
```

---

# EC2 Architecture

```text id="j6x5qd"
AWS Region
     │
     ▼
Availability Zone
     │
     ▼
VPC
     │
     ▼
Subnet
     │
     ▼
EC2 Instance
```

The EC2 instance is launched inside a subnet within a VPC.

---

# Common EC2 Use Cases

EC2 is commonly used for:

```text id="m5v4pk"
Web servers
Application servers
Docker hosts
Kubernetes worker nodes
CI/CD servers
Development environments
```

---

# Amazon Machine Image (AMI)

An **AMI (Amazon Machine Image)** is a template used to create EC2 instances.

An AMI contains:

```text id="n8g6bx"
Operating System
Pre-installed software
Configuration
```

Examples:

```text id="u3w7cv"
Ubuntu
Amazon Linux
Red Hat Enterprise Linux
Windows Server
```

Terraform example:

```hcl id="s5z2me"
data "aws_ami" "ubuntu" {

  most_recent = true

  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-24.04-amd64-server-*"]
  }
}
```

---

# Instance Types

Each EC2 instance type provides different CPU, memory, and networking capabilities.

Examples:

| Instance Type | Typical Use                    |
| ------------- | ------------------------------ |
| t3.micro      | Learning and testing           |
| t3.small      | Small applications             |
| t3.medium     | Development servers            |
| m7i.large     | General-purpose workloads      |
| c7g.large     | Compute-intensive applications |

Example:

```hcl id="r2f6ta"
instance_type = "t3.micro"
```

---

# Launching an EC2 Instance

Terraform example:

```hcl id="v9m4hx"
resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.web.id
  ]

  key_name = aws_key_pair.main.key_name

  tags = {
    Name = "web-server"
  }
}
```

Terraform creates the virtual machine automatically.

---

# Public vs Private IP

A public subnet can assign a public IP.

```text id="a7d2lr"
Internet
     │
     ▼
Public IP
     │
     ▼
EC2 Instance
```

A private subnet does not expose the instance directly to the internet.

```text id="p3y9sn"
Internet
     │
     ▼
Blocked
     │
     ▼
Private EC2 Instance
```

---

# Connecting to an EC2 Instance

Linux instances are usually accessed using SSH.

Example:

```bash id="b5x8jq"
ssh -i key.pem ubuntu@PUBLIC_IP
```

Components:

```text id="h4v6mz"
key.pem   → Private SSH key
ubuntu    → Default user
PUBLIC_IP → Instance public IP
```

---

# EC2 Key Pair

AWS uses SSH key pairs instead of passwords.

```text id="q2m8yb"
Private Key (.pem)
        │
        ▼
SSH Connection
        ▲
        │
Public Key
Stored on EC2
```

Terraform example:

```hcl id="w7p3kn"
resource "aws_key_pair" "main" {

  key_name = "dev-key"

  public_key = file("~/.ssh/id_ed25519.pub")
}
```

---

# Security Group

Most EC2 instances use a Security Group.

Example:

```text id="x5q7rd"
Allow SSH (22)
Allow HTTP (80)
Allow HTTPS (443)
Block everything else
```

Without the correct Security Group rules, you cannot connect to the instance.

---

# Elastic Block Store (EBS)

Every EC2 instance needs storage.

AWS uses **Elastic Block Store (EBS)**.

```text id="n3u5fh"
EC2 Instance
      │
      ▼
EBS Volume
```

Example:

```text id="z9y2kv"
30 GB
100 GB
500 GB
```

Terraform example:

```hcl id="e8r1cx"
root_block_device {

  volume_size = 30

  volume_type = "gp3"
}
```

---

# Instance Lifecycle

An EC2 instance moves through different states.

```text id="g7k9qw"
Pending
   │
Running
   │
Stopping
   │
Stopped
   │
Starting
   │
Running
   │
Terminated
```

After an instance is terminated, it cannot be restarted.

---

# Starting and Stopping

You can stop an instance:

```text id="t6m2vr"
Running
   │
Stop
   ▼
Stopped
```

Later:

```text id="v4p8hn"
Stopped
   │
Start
   ▼
Running
```

This is useful for development environments.

---

# Terminating an Instance

Termination permanently deletes the EC2 instance.

```text id="y8q3fc"
Running
     │
Terminate
     ▼
Deleted
```

The instance cannot be recovered.

---

# Tags

Tags help organize AWS resources.

Example:

```hcl id="c5n7dy"
tags = {

  Name = "web-server"

  Environment = "Development"

  Project = "Terraform-Lab"
}
```

Benefits:

```text id="r3v6kb"
Organization
Searching
Automation
Cost management
```

---

# Typical Project Structure

```text id="p9m4xa"
terraform/
├── provider.tf
├── network.tf
├── security.tf
├── compute.tf
├── variables.tf
└── outputs.tf
```

The EC2 configuration is commonly placed in:

```text id="b7q2lc"
compute.tf
```

---

# Common Beginner Mistakes

### Choosing the Wrong AMI

Always use a supported and up-to-date AMI.

---

### Forgetting the Security Group

Without an SSH rule:

```text id="h9x5ev"
Cannot connect to EC2
```

---

### Forgetting the Key Pair

Without the correct private key:

```text id="m2z8fs"
SSH connection fails
```

---

### Launching in the Wrong Subnet

A public web server should normally be launched in a public subnet.

---

### Forgetting to Terminate Test Instances

Unused EC2 instances may continue running and generate costs.

Always clean up lab resources when finished.

---

# Best Practices

```text id="v8d4qm"
Use the latest supported AMI
Use Security Groups
Restrict SSH access
Use tags
Keep instances updated
Terminate unused instances
Store Terraform code in separate files
```

---

# Useful Commands

Initialize Terraform:

```bash id="e5r9kh"
terraform init
```

Review changes:

```bash id="g6v3pt"
terraform plan
```

Deploy infrastructure:

```bash id="f1w8yb"
terraform apply
```

Connect using SSH:

```bash id="k3x2rv"
ssh -i key.pem ubuntu@PUBLIC_IP
```

Destroy infrastructure:

```bash id="u7n4jc"
terraform destroy
```

---

# Summary

```text id="s4h7mp"
EC2 → Virtual machine
AMI → Machine image
Instance Type → CPU and memory configuration
Security Group → Virtual firewall
Key Pair → SSH authentication
EBS → Persistent storage
Public IP → Internet access
Tags → Resource organization
```

> Amazon EC2 provides scalable virtual machines in the AWS cloud, allowing you to quickly deploy and manage servers for applications, development environments, and infrastructure workloads using Infrastructure as Code tools such as Terraform.

