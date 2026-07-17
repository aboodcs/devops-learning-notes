# 06 - Compute Instances

A **Compute Instance** is a virtual server in OCI.

It is like a computer running in Oracle Cloud.

You can install an operating system on it and use it to run applications.

```text id="lg3s0h"
Compute Instance = Virtual Machine in OCI
```

Examples:

```text id="y9a8dq"
Ubuntu server
Oracle Linux server
Web server
Docker host
Application server
Database server
DevOps tools server
```

## Simple Explanation

Instead of buying a physical server, you create a virtual server in OCI.

```text id="q2mqob"
Physical server → Expensive hardware
OCI Compute Instance → Virtual server in the cloud
```

You can connect to it using SSH and manage it like a normal Linux machine.

## Why Do We Use Compute Instances?

Compute Instances are used to run workloads.

Examples:

```text id="qzqor9"
Run web applications
Run Docker containers
Host APIs
Run Nginx or Apache
Run Jenkins
Run monitoring tools
Run test environments
Run Kubernetes worker nodes
```

## Basic Compute Architecture

```text id="9cyimf"
OCI Tenancy
└── Compartment
    └── VCN
        └── Subnet
            └── Compute Instance
```

A Compute Instance must be created inside:

```text id="25jyx2"
Compartment
VCN
Subnet
Availability Domain
```

## Main Compute Instance Parts

When creating a Compute Instance, you usually choose:

```text id="s8v8dm"
Name
Compartment
Availability Domain
Image
Shape
VCN
Subnet
Public IP option
SSH key
Boot volume
```

## 1. Image

An **Image** is the operating system used by the instance.

Examples:

```text id="2bo7i0"
Oracle Linux
Ubuntu
CentOS
Windows Server
```

Simple meaning:

```text id="c2ti2h"
Image = Operating system template
```

Example:

```text id="zl6w66"
Ubuntu image → Ubuntu Compute Instance
```

## 2. Shape

A **Shape** defines the CPU and memory of the instance.

Simple meaning:

```text id="9v65xh"
Shape = Instance size
```

Example:

```text id="qkd7x3"
Small shape  → Less CPU and memory
Large shape  → More CPU and memory
```

A shape controls:

```text id="g6vvbl"
CPU
RAM
Network performance
Cost
```

For learning, start with a small shape.

For production, choose the shape based on the application needs.

## 3. Boot Volume

A **Boot Volume** is the disk that contains the operating system.

When you create a Compute Instance, OCI creates a Boot Volume automatically.

```text id="8wm2bd"
Compute Instance
└── Boot Volume
    └── Operating System
```

Example:

```text id="xdyh08"
Ubuntu OS is stored on the Boot Volume.
```

## Boot Volume vs Block Volume

| Boot Volume                 | Block Volume        |
| --------------------------- | ------------------- |
| Created with the instance   | Added separately    |
| Contains operating system   | Used for extra data |
| Required to boot the server | Optional extra disk |
| Attached automatically      | Attached manually   |

Example:

```text id="f21a4b"
Compute Instance
├── Boot Volume  → Ubuntu OS
└── Block Volume → Application data
```

## 4. VNIC

A **VNIC** means **Virtual Network Interface Card**.

It connects the Compute Instance to the VCN network.

Simple meaning:

```text id="i4i9em"
VNIC = Network card for the cloud server
```

Through the VNIC, the instance gets:

```text id="l6k3jv"
Private IP address
Optional public IP address
Connection to subnet
Security rules
```

## 5. Private IP

Every Compute Instance gets a private IP address.

Example:

```text id="h3f0ds"
10.0.1.25
```

Private IP is used for communication inside the VCN.

Example:

```text id="rn8w93"
Web Server → Database Server
```

## 6. Public IP

A public IP allows access from the internet.

Example:

```text id="p2xdqn"
Your laptop
   ↓
Internet
   ↓
Compute Instance Public IP
```

Use public IP for:

```text id="qjg1we"
SSH access
Public web server
Testing application from browser
```

But not every server should have a public IP.

Databases and private services should usually stay private.

## Public Instance vs Private Instance

| Public Instance                         | Private Instance                               |
| --------------------------------------- | ---------------------------------------------- |
| Has public IP                           | No public IP                                   |
| Can be reached from internet if allowed | Only reachable inside VCN                      |
| Good for bastion or web server          | Good for database or internal app              |
| Needs Internet Gateway route            | Usually uses NAT Gateway for outbound internet |

## 7. SSH Key

For Linux instances, you usually connect using SSH.

OCI does not usually use password login by default.

You need an SSH key pair:

```text id="w7q28q"
Private key → stays on your laptop
Public key  → added to OCI instance
```

Create SSH key:

```bash id="iwewul"
ssh-keygen -t ed25519 -C "oci-instance"
```

This creates:

```text id="emk4sd"
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

When creating the instance, upload the public key.

## Connect to a Compute Instance

Example SSH command:

```bash id="wlfrrt"
ssh -i ~/.ssh/id_ed25519 ubuntu@PUBLIC_IP
```

For Oracle Linux, the username is usually:

```text id="xcdl4k"
opc
```

Example:

```bash id="zwb3bt"
ssh -i ~/.ssh/id_ed25519 opc@PUBLIC_IP
```

For Ubuntu, the username is usually:

```text id="72z3r3"
ubuntu
```

Example:

```bash id="lajuz8"
ssh -i ~/.ssh/id_ed25519 ubuntu@PUBLIC_IP
```

## Important SSH Requirements

To connect using SSH, you need:

```text id="oojx2d"
Instance is running
Public IP exists
Subnet is public
Internet Gateway exists
Route table allows internet traffic
Security rule allows port 22
Correct SSH private key
Correct username
```

## Security Rule for SSH

Allow SSH only from your public IP.

Bad:

```text id="0ntz3b"
Source: 0.0.0.0/0
Port: 22
```

Better:

```text id="03hf42"
Source: your-public-ip/32
Port: 22
```

This is safer because only your IP can connect.

## Running a Web Server

After connecting to the instance, you can install Nginx.

For Ubuntu:

```bash id="9kx09x"
sudo apt update
sudo apt install nginx -y
```

Check Nginx:

```bash id="1auc86"
systemctl status nginx
```

Then open:

```text id="d58g2j"
http://PUBLIC_IP
```

To access the website, security rules must allow port `80`.

## Security Rule for HTTP

Allow HTTP traffic:

```text id="7sqmbc"
Source: 0.0.0.0/0
Protocol: TCP
Port: 80
```

For HTTPS:

```text id="m74nqq"
Source: 0.0.0.0/0
Protocol: TCP
Port: 443
```

## Compute Instance Lifecycle

A Compute Instance can have different states.

Common states:

```text id="vn25fa"
Provisioning
Running
Stopped
Starting
Stopping
Terminated
```

## Stop vs Terminate

### Stop

Stopping an instance turns it off.

```text id="wto04w"
Instance stopped
Boot volume remains
You can start it again
```

Use stop when you want to pause the server.

### Terminate

Terminating deletes the instance.

```text id="ze42qr"
Instance deleted
May delete boot volume depending on option
Cannot use the same instance again
```

Use terminate carefully.

## Stop vs Reboot vs Terminate

| Action    | Meaning                  |
| --------- | ------------------------ |
| Stop      | Turn off the instance    |
| Start     | Turn on stopped instance |
| Reboot    | Restart the instance     |
| Terminate | Delete the instance      |

## Metadata and Cloud-Init

When creating an instance, you can pass startup commands.

This is often called:

```text id="ucyjkx"
cloud-init
user data
startup script
```

Example user data:

```bash id="i5vnlz"
#!/bin/bash
sudo apt update
sudo apt install nginx -y
echo "Hello from OCI Compute" | sudo tee /var/www/html/index.html
```

This installs Nginx automatically when the instance starts.

## Compute Instance with Docker

A Compute Instance can run Docker.

Example:

```text id="4guy84"
OCI Compute Instance
└── Docker
    └── Containers
```

Install Docker on Ubuntu:

```bash id="k81k1j"
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
```

Run Nginx container:

```bash id="4my520"
sudo docker run -d --name nginx -p 80:80 nginx:alpine
```

Open:

```text id="a97tv6"
http://PUBLIC_IP
```

## Compute Instance and VCN

A Compute Instance needs networking to be useful.

For a public web server, you usually need:

```text id="kjf6jm"
VCN
Public Subnet
Internet Gateway
Route Table
Security List or NSG
Public IP
```

Simple architecture:

```text id="l6e31c"
Internet
   ↓
Internet Gateway
   ↓
Public Subnet
   ↓
Compute Instance
```

## Compute Instance and Block Volume

You can attach extra storage to a Compute Instance.

```text id="jwzq9m"
Compute Instance
├── Boot Volume
└── Block Volume
```

Use extra Block Volume for:

```text id="16g8uf"
Application data
Docker data
Database files
Logs
Backups before upload to Object Storage
```

## Compute Instance and Load Balancer

In production, users should usually access a Load Balancer, not the instance directly.

```text id="796bdt"
User
 ↓
Load Balancer
 ↓
Compute Instance 1
 ↓
Compute Instance 2
```

This improves availability and allows scaling.

## Console Path

To create or manage Compute Instances:

```text id="vw5q4h"
OCI Console
→ Compute
→ Instances
```

When creating an instance, select:

```text id="ne2v5e"
Compartment
Name
Placement
Image
Shape
Networking
SSH key
Boot volume
```

## Beginner Lab Example

Goal:

```text id="iwzk8y"
Create one Ubuntu Compute Instance
Connect using SSH
Install Nginx
Open website from browser
```

Basic design:

```text id="xmw8u3"
VCN: 10.0.0.0/16
└── Public Subnet: 10.0.1.0/24
    └── Ubuntu Compute Instance
        └── Nginx
```

Needed ports:

```text id="r6hle4"
22 → SSH from your IP only
80 → HTTP from internet
443 → HTTPS from internet if needed
```

## Basic Commands After SSH

Update packages:

```bash id="fmna16"
sudo apt update
```

Install Nginx:

```bash id="hfshwj"
sudo apt install nginx -y
```

Create simple page:

```bash id="uk36ro"
echo "Hello from OCI" | sudo tee /var/www/html/index.html
```

Check service:

```bash id="x6u97c"
systemctl status nginx
```

Check IP:

```bash id="tjcuu6"
curl ifconfig.me
```

## Common Beginner Mistakes

### Cannot SSH to Instance

Check:

```text id="w82798"
Is the instance running?
Does it have public IP?
Is it in a public subnet?
Does route table use Internet Gateway?
Does security rule allow port 22?
Are you using the correct private key?
Are you using the correct username?
```

### Website Not Opening

Check:

```text id="dnl66f"
Is Nginx running?
Is port 80 allowed in security rules?
Is the instance firewall blocking traffic?
Is the app listening on 0.0.0.0?
Are you using the correct public IP?
```

### Wrong Username

Common usernames:

```text id="vvfgux"
Ubuntu image       → ubuntu
Oracle Linux image → opc
```

### Opening All Ports

Bad:

```text id="gbykfs"
Allow all traffic from 0.0.0.0/0
```

Better:

```text id="ac3c9d"
Allow only required ports
SSH 22 only from your IP
HTTP 80 if web server is public
HTTPS 443 if needed
```

### Forgetting the Private Key

If you lose the private key, connecting to the instance becomes difficult.

Keep your private key safe.

Do not upload it to GitHub.

## Security Best Practices

```text id="ebdo2k"
Use SSH keys, not passwords
Allow SSH only from your IP
Do not expose databases publicly
Use private subnets for internal servers
Use NSGs for specific traffic control
Keep the operating system updated
Do not store secrets in plain text
Use IAM policies carefully
```

## Compute in DevOps

Compute Instances are useful for DevOps learning and projects.

You can use them to run:

```text id="b3bgdb"
Docker
Jenkins
GitHub Actions self-hosted runner
Monitoring tools
Nginx reverse proxy
Testing environments
Kubernetes nodes
Terraform labs
```

Example DevOps flow:

```text id="cvr7fj"
Terraform creates Compute Instance
        ↓
cloud-init installs Docker
        ↓
Docker runs application container
        ↓
Security rules expose port 80
        ↓
User opens application in browser
```

## Summary

```text id="lw2wbd"
Compute Instance → Virtual server in OCI
Image            → Operating system template
Shape            → CPU and memory size
Boot Volume      → OS disk
VNIC             → Network card
Private IP       → Internal network address
Public IP        → Internet reachable address
SSH Key          → Secure login method
Subnet           → Network where instance lives
Security Rule    → Controls allowed traffic
```

> A Compute Instance is a virtual server in OCI. It runs inside a VCN, uses an image and shape, and can host applications, containers, and DevOps tools.

