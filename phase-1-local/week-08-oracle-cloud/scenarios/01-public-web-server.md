# Scenario 01 - Deploy a Public Web Server

## Goal

In this scenario, we will deploy a simple public web server that anyone on the Internet can access.

This is usually the first architecture every cloud engineer builds because it introduces the core networking concepts of Oracle Cloud Infrastructure.

By the end of this scenario, you will understand how networking resources work together to make a Compute Instance reachable from the Internet.

---

# Final Architecture

```text
                    Internet
                        │
                        ▼
               Internet Gateway
                        │
                        ▼
                     Route Table
                        │
                        ▼
                 Public Subnet
                        │
                        ▼
              Security List / NSG
                        │
                        ▼
                 Compute Instance
                        │
                        ▼
                     Nginx Website
```

---

# What We Want To Build

We want to create an Ubuntu Compute Instance.

The server will have:

- Public IP
- Internet access
- SSH access
- HTTP access

After installing Nginx, opening the public IP in a browser should display the default Nginx page.

---

# OCI Services Used

| Service | Purpose |
|----------|----------|
| Compartment | Organize resources |
| VCN | Private virtual network |
| Internet Gateway | Connect the VCN to the Internet |
| Route Table | Tell traffic where to go |
| Public Subnet | Place internet-facing resources |
| Security List | Allow SSH and HTTP |
| Compute Instance | Virtual machine |
| Public IP | Public address for the VM |

---

# Why Do We Need Every Service?

## Compartment

Keeps resources organized.

Everything we create belongs to a compartment.

---

## VCN

Creates our own isolated network inside Oracle Cloud.

Think of it as your own private data center.

---

## Public Subnet

A subnet divides the VCN into smaller networks.

Since we want users from the Internet to reach our server, the subnet must be public.

---

## Internet Gateway

Without an Internet Gateway, the VCN has no connection to the Internet.

It acts as the bridge between Oracle Cloud and the outside world.

---

## Route Table

The Route Table tells Oracle where to send traffic.

For Internet traffic it usually contains:

Destination

```
0.0.0.0/0
```

Target

```
Internet Gateway
```

Meaning:

> Any traffic leaving the VCN should go through the Internet Gateway.

---

## Security List

Even if the server has Internet access, Oracle blocks incoming traffic unless we allow it.

We must allow:

SSH

```
TCP 22
```

HTTP

```
TCP 80
```

HTTPS (optional)

```
TCP 443
```

---

## Compute Instance

The virtual machine where our application runs.

In this scenario we will use Ubuntu.

---

## Public IP

This is the address users use to reach the server.

Example:

```
129.xxx.xxx.xxx
```

---

# Resource Relationships

```text
Compartment
    │
    ▼
VCN
    │
    ▼
Public Subnet
    │
    ├──────── Route Table
    │
    ├──────── Security List
    │
    ▼
Compute Instance
    │
    ▼
Public IP
```

Notice that every resource depends on another.

You cannot create a Compute Instance without first having a subnet.

You cannot have a subnet without a VCN.

---

# Build Order

Create resources in this order:

1. Create Compartment
2. Create VCN
3. Create Internet Gateway
4. Create Route Table
5. Create Public Subnet
6. Configure Security List
7. Launch Compute Instance
8. Assign Public IP
9. SSH into the server
10. Install Nginx

---

# Traffic Flow

When someone opens your website:

```text
Browser

↓

Internet

↓

Internet Gateway

↓

Route Table

↓

Public Subnet

↓

Security List

↓

Compute Instance

↓

Nginx
```

The request travels through every resource above.

---

# OCI Console Navigation

## Create VCN

Networking

↓

Virtual Cloud Networks

↓

Create VCN

---

## Create Internet Gateway

Networking

↓

Virtual Cloud Networks

↓

Your VCN

↓

Internet Gateway

---

## Create Route Table

Networking

↓

Virtual Cloud Networks

↓

Route Tables

---

## Create Public Subnet

Networking

↓

Virtual Cloud Networks

↓

Subnets

---

## Launch Compute Instance

Compute

↓

Instances

↓

Create Instance

---

# Validation

Verify the Public IP

```bash
ping PUBLIC_IP
```

SSH

```bash
ssh ubuntu@PUBLIC_IP
```

Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

Open

```
http://PUBLIC_IP
```

You should see:

```
Welcome to nginx!
```

---

# Common Beginner Mistakes

❌ Forgot to attach Internet Gateway

❌ Missing Route Table rule

❌ Security List blocks port 80

❌ Instance has no Public IP

❌ SSH uses wrong username

---

# What You Learned

After completing this scenario you should understand:

- Why a VCN is required
- What a Public Subnet is
- Why an Internet Gateway is necessary
- How Route Tables work
- Why Security Lists exist
- How Internet traffic reaches a Compute Instance
- The relationship between all OCI networking components

---

# Next Scenario

Scenario 02

Private Backend with Public Load Balancer

Instead of exposing the Compute Instance directly to the Internet, we will expose only the Load Balancer while keeping the servers inside a private subnet.
