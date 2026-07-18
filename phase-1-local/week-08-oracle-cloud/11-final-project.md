# 11 - Final Project

## Project Name

```text id="ipmw0e"
OCI Highly Available Web Application
```

In this final project, you will build a simple web application architecture on OCI.

The goal is to connect the main OCI concepts together:

```text id="6xq8n2"
Compartment
VCN
Subnets
Security Rules
Compute Instances
Load Balancer
Storage
Terraform idea
Monitoring idea
```

## Project Goal

Build a small cloud environment where users access a public Load Balancer, and the Load Balancer sends traffic to two Compute Instances running Nginx.

```text id="2n64ys"
User
 ↓
Internet
 ↓
OCI Load Balancer
 ↓
Compute Instance 1
Compute Instance 2
```

## What You Will Learn

By doing this project, you will understand:

```text id="z8g5cv"
How OCI resources connect together
How networking works in real cloud projects
How Compute Instances run applications
How Load Balancers distribute traffic
How security rules affect access
How to troubleshoot cloud networking problems
How Terraform can later automate the same setup
```

## Final Architecture

```text id="9a4vcp"
OCI Tenancy
└── Dev Compartment
    └── VCN: 10.0.0.0/16
        ├── Public Subnet: 10.0.1.0/24
        │   └── Public Load Balancer
        │
        └── Web Subnet: 10.0.2.0/24
            ├── Compute Instance 1
            └── Compute Instance 2
```

Traffic flow:

```text id="q7h0vy"
User
 ↓
Load Balancer Public IP
 ↓
Backend Set
 ↓
web-1 and web-2
```

## Required OCI Resources

You will create:

```text id="ci0kd7"
1. Compartment
2. VCN
3. Public Subnet
4. Web Subnet
5. Internet Gateway
6. Route Table
7. Security Rules
8. Two Compute Instances
9. Load Balancer
10. Backend Set
11. Listener
12. Health Check
```

## Recommended Names

Use clear names for your resources.

```text id="f8l50o"
Compartment: dev-project
VCN: dev-vcn
Public Subnet: public-subnet
Web Subnet: web-subnet
Compute Instance 1: web-1
Compute Instance 2: web-2
Load Balancer: public-web-lb
Backend Set: web-backend-set
```

## Step 1 - Create a Compartment

Create a compartment for the project.

Console path:

```text id="b9qvq3"
OCI Console
→ Identity & Security
→ Compartments
→ Create Compartment
```

Example:

```text id="n3i5rz"
Name: dev-project
Description: Final OCI learning project
```

## Step 2 - Create a VCN

Create a VCN for the project.

Console path:

```text id="e27qee"
OCI Console
→ Networking
→ Virtual Cloud Networks
→ Create VCN
```

Example:

```text id="k8edpw"
VCN Name: dev-vcn
CIDR Block: 10.0.0.0/16
Compartment: dev-project
```

## Step 3 - Create Subnets

Create two subnets.

### Public Subnet

```text id="f1dl9m"
Name: public-subnet
CIDR: 10.0.1.0/24
Purpose: Load Balancer
```

### Web Subnet

```text id="r9cnr7"
Name: web-subnet
CIDR: 10.0.2.0/24
Purpose: Compute Instances
```

Simple design:

```text id="lrl6rn"
VCN: 10.0.0.0/16
├── public-subnet: 10.0.1.0/24
└── web-subnet: 10.0.2.0/24
```

## Step 4 - Create Internet Gateway

The Internet Gateway allows public internet access.

Console path:

```text id="pjqva9"
VCN
→ Internet Gateways
→ Create Internet Gateway
```

Example:

```text id="glal0v"
Name: dev-internet-gateway
```

## Step 5 - Configure Route Table

For public internet access, add this route rule:

```text id="3jij32"
Destination: 0.0.0.0/0
Target: Internet Gateway
```

Meaning:

```text id="vpp8uw"
Send internet traffic to the Internet Gateway.
```

## Step 6 - Configure Security Rules

You need security rules for the Load Balancer and web servers.

## Load Balancer Security Rules

Allow HTTP traffic from the internet:

```text id="bnswp5"
Source: 0.0.0.0/0
Protocol: TCP
Port: 80
```

Optional HTTPS:

```text id="2cit0z"
Source: 0.0.0.0/0
Protocol: TCP
Port: 443
```

## Web Server Security Rules

Allow traffic from the Load Balancer to the backend servers:

```text id="44k75k"
Source: public-subnet CIDR
Protocol: TCP
Port: 80
```

For learning only, if you need SSH:

```text id="7940or"
Source: your-public-ip/32
Protocol: TCP
Port: 22
```

Do not open SSH to everyone.

Bad:

```text id="wmzdvs"
0.0.0.0/0 → port 22
```

Better:

```text id="k56ffo"
your-public-ip/32 → port 22
```

## Step 7 - Create Two Compute Instances

Create two Compute Instances inside the `web-subnet`.

Console path:

```text id="xw3p5j"
OCI Console
→ Compute
→ Instances
→ Create Instance
```

Create:

```text id="o4cd93"
web-1
web-2
```

Recommended image:

```text id="uwfw7q"
Ubuntu
```

Add your SSH public key when creating each instance.

## Step 8 - Install Nginx on web-1

SSH into `web-1`:

```bash id="h9s3bq"
ssh -i ~/.ssh/id_ed25519 ubuntu@WEB_1_PUBLIC_IP
```

Install Nginx:

```bash id="ut2e1i"
sudo apt update
sudo apt install nginx -y
```

Create a custom page:

```bash id="hv9d5p"
echo "Hello from web-1" | sudo tee /var/www/html/index.html
```

Check Nginx:

```bash id="khi6y6"
systemctl status nginx
```

## Step 9 - Install Nginx on web-2

SSH into `web-2`:

```bash id="d9ihzy"
ssh -i ~/.ssh/id_ed25519 ubuntu@WEB_2_PUBLIC_IP
```

Install Nginx:

```bash id="qpu6a5"
sudo apt update
sudo apt install nginx -y
```

Create a custom page:

```bash id="px2t7w"
echo "Hello from web-2" | sudo tee /var/www/html/index.html
```

Check Nginx:

```bash id="h2iooj"
systemctl status nginx
```

## Step 10 - Create Load Balancer

Console path:

```text id="f6yhrh"
OCI Console
→ Networking
→ Load Balancers
→ Create Load Balancer
```

Example:

```text id="rur8ak"
Name: public-web-lb
Visibility: Public
VCN: dev-vcn
Subnet: public-subnet
```

## Step 11 - Create Backend Set

Create a Backend Set for the web servers.

Example:

```text id="4ztnmb"
Backend Set Name: web-backend-set
Policy: Round Robin
Health Check Protocol: HTTP
Health Check Port: 80
Health Check Path: /
```

Meaning:

```text id="9j8cxx"
The Load Balancer will check if each backend server responds on port 80.
```

## Step 12 - Add Backend Servers

Add both Compute Instances as backend servers.

```text id="m69zc8"
web-1 private IP : 80
web-2 private IP : 80
```

Example:

```text id="4s2wnx"
10.0.2.10:80
10.0.2.11:80
```

The Load Balancer should use the private IPs of the backend servers.

## Step 13 - Create Listener

Create a listener for HTTP traffic.

```text id="6i9nq0"
Protocol: HTTP
Port: 80
Backend Set: web-backend-set
```

Meaning:

```text id="wbaac0"
When users visit the Load Balancer on port 80, traffic goes to the backend set.
```

## Step 14 - Test the Project

Get the Load Balancer public IP.

Open in browser:

```text id="8x7p2e"
http://LOAD_BALANCER_PUBLIC_IP
```

You should see:

```text id="e0oxix"
Hello from web-1
```

or:

```text id="sq4ea7"
Hello from web-2
```

Refresh the page multiple times.

The Load Balancer may send traffic to different backend servers.

## Step 15 - Test High Availability

Stop Nginx on `web-1`:

```bash id="i2wj24"
sudo systemctl stop nginx
```

Now the Load Balancer health check should detect that `web-1` is unhealthy.

Traffic should continue going to `web-2`.

Start Nginx again:

```bash id="owtrui"
sudo systemctl start nginx
```

## What This Proves

This project proves that:

```text id="ued86b"
The Load Balancer is the public entry point
Backend servers run the application
Health checks detect broken servers
Traffic can continue if one server fails
Networking and security rules must be correct
```

## Optional - Use Cloud-Init

Instead of installing Nginx manually, you can use cloud-init during instance creation.

Example:

```bash id="nno0rb"
#!/bin/bash
sudo apt update
sudo apt install nginx -y
echo "Hello from OCI Compute" | sudo tee /var/www/html/index.html
sudo systemctl enable nginx
sudo systemctl start nginx
```

This automatically installs Nginx when the instance starts.

## Optional - Add Object Storage

Create an Object Storage bucket for backups or logs.

Console path:

```text id="zqfirc"
OCI Console
→ Storage
→ Object Storage
→ Buckets
→ Create Bucket
```

Example:

```text id="3qc86m"
Bucket name: web-app-backups
```

Use it for:

```text id="c26czd"
Application backups
Nginx logs backup
Static files
Terraform state in future projects
```

## Optional - Terraform Version

After you build the project manually, try to automate it with Terraform.

Terraform files:

```text id="d30t0r"
oci-final-project/
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── network.tf
├── compute.tf
├── load-balancer.tf
├── outputs.tf
└── .gitignore
```

Terraform can create:

```text id="ublw3m"
VCN
Subnets
Internet Gateway
Route Tables
Security Rules
Compute Instances
Load Balancer
Backend Set
Listener
```

This is the DevOps way.

```text id="wq4551"
Manual Console Project → Understand the idea
Terraform Project      → Automate the idea
```

## Optional - OKE Version

You can later build the same idea using OKE.

Instead of Compute Instances running Nginx manually:

```text id="lmpp1w"
OKE Cluster
├── Deployment
├── Pods
└── Service type LoadBalancer
```

Traffic flow:

```text id="yqhcnk"
User
 ↓
OCI Load Balancer
 ↓
Kubernetes Service
 ↓
Pods
```

This is better when you want to run containerized applications.

## Project Folder Structure

Recommended repo structure:

```text id="kmsbao"
oci-final-project/
├── README.md
├── architecture.md
├── screenshots/
│   ├── vcn.png
│   ├── compute-instances.png
│   ├── load-balancer.png
│   └── application-test.png
├── manual-steps.md
├── troubleshooting.md
└── terraform/
    ├── provider.tf
    ├── variables.tf
    ├── main.tf
    ├── outputs.tf
    └── .gitignore
```

## README Should Explain

Your README should include:

```text id="egkwel"
Project goal
Architecture diagram
OCI services used
Steps to create the project
Screenshots
Testing result
Problems faced
How to clean up resources
```

## Useful Screenshots

Take screenshots of:

```text id="zc65pq"
VCN
Subnets
Security rules
Compute Instances
Nginx pages
Load Balancer
Backend health
Browser showing the app
```

These screenshots make the project stronger for GitHub and LinkedIn.

## Common Problems

### Load Balancer Shows Error

Check:

```text id="onmmah"
Are backend servers healthy?
Is Nginx running?
Is port 80 open?
Is the health check path correct?
Are security rules correct?
```

### Backend Servers Are Unhealthy

Check on each server:

```bash id="epwxjx"
systemctl status nginx
curl localhost
```

Also check security rules:

```text id="5yxy7o"
Load Balancer subnet must reach backend servers on port 80.
```

### Cannot SSH

Check:

```text id="s2a1c5"
Correct public IP
Correct username
Correct private key
Port 22 allowed from your IP
Instance is running
Subnet has internet route
```

### Website Works on Instance but Not Load Balancer

This usually means the issue is between the Load Balancer and backend servers.

Check:

```text id="ayicab"
Backend set
Backend health
Backend private IP
Backend port
Security rules
Health check path
```

## Cleanup

When done, delete resources to avoid unwanted cost.

Delete in this order:

```text id="ee3v2g"
1. Load Balancer
2. Compute Instances
3. Block Volumes if not needed
4. Subnets
5. Internet Gateway
6. Route Tables
7. VCN
8. Object Storage bucket if created
9. Compartment if empty
```

Always check:

```text id="y7xsh4"
No running Compute Instances
No Load Balancers
No unused Block Volumes
No public buckets
```

## Final Project Summary

```text id="b5b6me"
Compartment     → Organizes the project
VCN             → Main private network
Subnets         → Separate Load Balancer and web servers
Internet Gateway → Allows public traffic
Security Rules  → Control allowed traffic
Compute Instances → Run Nginx web servers
Load Balancer   → Public entry point
Backend Set     → Group of web servers
Health Check    → Detects working and broken servers
Object Storage  → Optional backup/static file storage
Terraform       → Optional automation
OKE             → Optional Kubernetes version
```

## Final Architecture Summary

```text id="sp23k7"
User
 ↓
Internet
 ↓
Public Load Balancer
 ↓
Backend Set
 ├── web-1 running Nginx
 └── web-2 running Nginx
```

> This final project connects the core OCI concepts together: networking, compute, security, storage, and load balancing. It is a strong beginner cloud project because it looks like a real production architecture in a simplified way.
