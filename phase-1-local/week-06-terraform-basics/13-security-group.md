# 13 - Security Groups (AWS)

Cloud resources should never be directly exposed to the internet without protection.

A **Security Group** is a virtual firewall that controls which network traffic is allowed to enter or leave an AWS resource.

Security Groups are commonly attached to:

```text id="k3m7v9"
EC2 Instances
Application Load Balancers
Elastic Network Interfaces (ENIs)
RDS Databases
```

```text id="t8y2wc"
Internet
    │
    ▼
Security Group
    │
    ▼
EC2 Instance
```

Only traffic that matches the Security Group rules is allowed.

---

# Why Do We Need Security Groups?

Imagine you launch an EC2 instance.

Without a Security Group:

```text id="r1v5ha"
Internet
     │
     ▼
Every Port Open
```

Anyone could attempt to connect.

With a Security Group:

```text id="c9w6jx"
Internet
     │
     ▼
Allow HTTP (80)
Allow HTTPS (443)
Allow SSH (22)
Block Everything Else
```

Benefits:

```text id="m4f8qe"
Protect EC2 instances
Reduce attack surface
Control inbound traffic
Control outbound traffic
```

---

# Inbound vs Outbound Rules

A Security Group has two types of rules.

## Inbound Rules

Inbound rules control **incoming** traffic.

Example:

```text id="a6n2pr"
Internet
     │
     ▼
EC2 Instance
```

Allow:

```text id="h7y4dl"
SSH
HTTP
HTTPS
```

---

## Outbound Rules

Outbound rules control **traffic leaving** the instance.

Example:

```text id="x3u8kv"
EC2 Instance
      │
      ▼
Internet
```

Examples:

```text id="v2e5as"
Download updates
Access APIs
Install software
```

---

# Example AWS Architecture

```text id="p5m1rf"
Internet
      │
      ▼
Internet Gateway
      │
      ▼
Public Subnet
      │
      ▼
Security Group
      │
      ▼
EC2 Instance
```

The Security Group acts as a firewall before traffic reaches the EC2 instance.

---

# Creating a Security Group

Example:

```hcl id="n4w8cx"
resource "aws_security_group" "web" {

  name        = "web-security-group"

  description = "Security group for web server"

  vpc_id      = aws_vpc.main.id
}
```

This creates an empty Security Group.

No inbound traffic is allowed until rules are added.

---

# Allow SSH

```hcl id="k6j9dp"
ingress {

  description = "SSH"

  from_port = 22

  to_port = 22

  protocol = "tcp"

  cidr_blocks = [var.allowed_ssh_cidr]
}
```

Allows:

```text id="z8p3uy"
TCP
Port 22
Only from allowed_ssh_cidr
```

---

# Allow HTTP

```hcl id="q5x1wb"
ingress {

  description = "HTTP"

  from_port = 80

  to_port = 80

  protocol = "tcp"

  cidr_blocks = ["0.0.0.0/0"]
}
```

Allows web traffic.

---

# Allow HTTPS

```hcl id="m7r4sn"
ingress {

  description = "HTTPS"

  from_port = 443

  to_port = 443

  protocol = "tcp"

  cidr_blocks = ["0.0.0.0/0"]
}
```

Allows secure web traffic.

---

# Allow Outbound Traffic

AWS Security Groups allow all outbound traffic by default.

You can define it explicitly:

```hcl id="e2f6zg"
egress {

  from_port = 0

  to_port = 0

  protocol = "-1"

  cidr_blocks = ["0.0.0.0/0"]
}
```

This allows the instance to communicate with the internet.

---

# Complete Example

```hcl id="y4h9la"
resource "aws_security_group" "web" {

  name   = "web-security-group"

  vpc_id = aws_vpc.main.id

  ingress {

    from_port = 22

    to_port = 22

    protocol = "tcp"

    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {

    from_port = 80

    to_port = 80

    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {

    from_port = 443

    to_port = 443

    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

# Attach Security Group to an EC2 Instance

Example:

```hcl id="u7b3rd"
resource "aws_instance" "web" {

  ami           = data.aws_ami.ubuntu.id

  instance_type = "t3.micro"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.web.id
  ]
}
```

The EC2 instance is now protected by the Security Group.

---

# Restrict SSH Access

Avoid:

```text id="r8v2mc"
0.0.0.0/0
```

This allows SSH from anywhere.

Better:

```text id="q9w6yt"
203.0.113.10/32
```

Or:

```hcl id="d5k7en"
variable "allowed_ssh_cidr" {
  type = string
}
```

Example value:

```text id="x1m4ph"
203.0.113.10/32
```

Only your IP address can connect using SSH.

---

# Common Ports

| Service    | Protocol | Port |
| ---------- | -------- | ---: |
| SSH        | TCP      |   22 |
| HTTP       | TCP      |   80 |
| HTTPS      | TCP      |  443 |
| PostgreSQL | TCP      | 5432 |
| MySQL      | TCP      | 3306 |
| Redis      | TCP      | 6379 |

Open only the ports required by your application.

---

# Principle of Least Privilege

Only allow the minimum permissions required.

Bad:

```text id="z5r8qa"
Allow every port
Allow everyone
```

Better:

```text id="f7v2ty"
Allow SSH only from your IP
Allow HTTP
Allow HTTPS
Block everything else
```

---

# Example Web Server

```text id="p8n5lw"
Internet
     │
     ▼
80 (HTTP)
443 (HTTPS)
     │
     ▼
Security Group
     │
     ▼
EC2 Instance
```

SSH is restricted to the administrator's IP.

---

# Example Database Server

```text id="t2h7mc"
Internet
      │
      ▼
Blocked
      │
      ▼
Private Subnet
      │
      ▼
Amazon RDS
```

Instead:

```text id="g3q6wv"
Application Server
      │
      ▼
PostgreSQL 5432
      │
      ▼
Database
```

Databases should remain private whenever possible.

---

# Security Groups vs Network ACLs

AWS provides two network security mechanisms.

```text id="v5m9zs"
Security Group
--------------
Attached to EC2 instances
Stateful

Network ACL
-----------
Attached to subnets
Stateless
```

Most applications primarily use Security Groups.

---

# Testing Connectivity

Connect through SSH:

```bash id="l4w8qe"
ssh -i key.pem ubuntu@PUBLIC_IP
```

Test the web server:

```bash id="c8d3yx"
curl http://PUBLIC_IP
```

Or open:

```text id="j6k2ta"
http://PUBLIC_IP
```

---

# Example Project Structure

```text id="u9v1nf"
terraform/
├── provider.tf
├── network.tf
├── security.tf
├── compute.tf
├── variables.tf
└── outputs.tf
```

Security Group resources are usually stored in:

```text id="h2q5wr"
security.tf
```

---

# Common Beginner Mistakes

### Opening SSH to Everyone

Bad:

```text id="s8x3pj"
0.0.0.0/0
```

Better:

```text id="e4w7ln"
Your public IP/32
```

---

### Opening Unused Ports

Only open the ports your application needs.

---

### Forgetting HTTPS

Production web applications should use HTTPS.

---

### Forgetting Outbound Rules

If outbound traffic is restricted, the instance may not be able to:

```text id="n6t9gv"
Download updates
Install packages
Access external services
```

---

### Exposing Databases

Bad:

```text id="q1r5bz"
Internet
    │
    ▼
Database
```

Better:

```text id="p3w8mc"
Application
     │
     ▼
Database
```

Keep databases inside private subnets.

---

# Best Practices

```text id="b9m4xs"
Allow only required ports
Restrict SSH to trusted IP addresses
Use variables instead of hardcoded CIDRs
Keep databases private
Use HTTPS
Follow the principle of least privilege
Store Security Group resources in security.tf
```

---

# Useful Commands

Initialize Terraform:

```bash id="g5y7va"
terraform init
```

Review changes:

```bash id="j2x6cp"
terraform plan
```

Deploy infrastructure:

```bash id="r8m4zh"
terraform apply
```

Connect to EC2:

```bash id="f6n2qd"
ssh -i key.pem ubuntu@PUBLIC_IP
```

Test the web server:

```bash id="k3v8tx"
curl http://PUBLIC_IP
```

---

# Summary

```text id="d4h7pr"
Security Group → Virtual firewall
Inbound Rules  → Incoming traffic
Outbound Rules → Outgoing traffic
Port 22         → SSH
Port 80         → HTTP
Port 443        → HTTPS
Least Privilege → Allow only required access
```

> AWS Security Groups are stateful virtual firewalls that protect cloud resources by controlling inbound and outbound network traffic, allowing only the connections required by your application.

