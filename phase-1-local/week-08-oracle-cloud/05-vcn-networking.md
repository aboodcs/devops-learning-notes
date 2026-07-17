# 05 - VCN Networking

**VCN** means **Virtual Cloud Network**.

A VCN is your private network inside OCI.

```text id="es64po"
VCN = Virtual Cloud Network
```

Think of it like your own network in Oracle Cloud where your servers, databases, and load balancers live.

```text id="mw35ea"
OCI Tenancy
└── Compartment
    └── VCN
        ├── Subnet
        ├── Route Table
        ├── Security List
        ├── Internet Gateway
        └── Compute Instance
```

## Why Do We Need a VCN?

Before creating Compute Instances, Load Balancers, or private databases, you need networking.

The VCN controls how resources communicate.

A VCN helps you manage:

```text id="ajc7sp"
Private IP addresses
Public access
Internet access
Subnet separation
Security rules
Routing
Traffic control
```

## Simple Explanation

A VCN is like the network inside a company.

Example:

```text id="rqsq7s"
Company Network
├── Public area
│   └── Website server
└── Private area
    └── Database server
```

In OCI:

```text id="zubk1o"
VCN
├── Public Subnet
│   └── Web Server
└── Private Subnet
    └── Database
```

## Main VCN Components

The main VCN networking components are:

```text id="pub2pu"
VCN
CIDR Block
Subnet
Public Subnet
Private Subnet
Route Table
Internet Gateway
NAT Gateway
Security List
Network Security Group
```

## 1. CIDR Block

A **CIDR block** defines the IP address range of the VCN.

Example:

```text id="b8jadx"
10.0.0.0/16
```

This means the VCN can use private IP addresses from this range.

Example:

```text id="gc66xz"
VCN CIDR: 10.0.0.0/16
```

Then you can create smaller subnets inside it:

```text id="hsr6hd"
Public Subnet:  10.0.1.0/24
Private Subnet: 10.0.2.0/24
```

## 2. Subnet

A **Subnet** is a smaller network inside a VCN.

```text id="k5pwjq"
VCN
├── Subnet 1
├── Subnet 2
└── Subnet 3
```

Subnets help you organize resources.

Example:

```text id="1k1icq"
Public Subnet  → Web servers
Private Subnet → Databases
```

## 3. Public Subnet

A **Public Subnet** is a subnet where resources can have public IP addresses.

Use it for resources that need internet access.

Examples:

```text id="d0unx5"
Load Balancer
Bastion Host
Public Web Server
```

Example:

```text id="8qjhaj"
Internet
   ↓
Internet Gateway
   ↓
Public Subnet
   ↓
Web Server
```

## 4. Private Subnet

A **Private Subnet** is a subnet where resources do not have public IP addresses.

Use it for internal resources.

Examples:

```text id="ny74qz"
Database
Private application server
Internal services
```

Example:

```text id="j5sbr2"
Private Subnet
└── Database
```

The database should usually not be directly accessible from the internet.

## Public vs Private Subnet

| Public Subnet                           | Private Subnet                             |
| --------------------------------------- | ------------------------------------------ |
| Can use public IP                       | No public IP                               |
| Can receive internet traffic if allowed | Not directly reachable from internet       |
| Used for web servers/load balancers     | Used for databases/internal services       |
| Needs Internet Gateway route            | Usually uses NAT Gateway for outbound only |

## 5. Route Table

A **Route Table** controls where network traffic goes.

It contains route rules.

Example:

```text id="tq6x35"
Destination: 0.0.0.0/0
Target: Internet Gateway
```

Meaning:

```text id="b961yz"
Send internet traffic to the Internet Gateway.
```

## Route Table Example

For a public subnet:

```text id="8z5oxh"
0.0.0.0/0 → Internet Gateway
```

For a private subnet:

```text id="murzt0"
0.0.0.0/0 → NAT Gateway
```

## 6. Internet Gateway

An **Internet Gateway** allows resources in a public subnet to communicate with the internet.

```text id="89rlab"
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Subnet
   │
   ▼
Compute Instance
```

To access a Compute Instance from the internet, you usually need:

```text id="o5v2k9"
Public IP address
Internet Gateway
Route Table rule
Security rule allowing traffic
```

## 7. NAT Gateway

A **NAT Gateway** allows private resources to access the internet without being accessed from the internet.

Example:

```text id="8vv0b1"
Private Compute Instance
   ↓
NAT Gateway
   ↓
Internet
```

Use NAT Gateway when a private server needs to:

```text id="g6xlhr"
Install packages
Download updates
Pull Docker images
Access external APIs
```

But users from the internet cannot directly connect to it.

## Internet Gateway vs NAT Gateway

| Internet Gateway                                            | NAT Gateway                              |
| ----------------------------------------------------------- | ---------------------------------------- |
| Used with public subnets                                    | Used with private subnets                |
| Allows inbound and outbound traffic if security rules allow | Allows outbound traffic only             |
| Resource may have public IP                                 | Resource stays private                   |
| Good for web servers                                        | Good for private servers needing updates |

## 8. Security List

A **Security List** controls allowed traffic at the subnet level.

It has two types of rules:

```text id="e0wkaq"
Ingress rules → Incoming traffic
Egress rules  → Outgoing traffic
```

Example ingress rule:

```text id="w82vf0"
Allow TCP port 22 from your IP
```

Example:

```text id="6tyf6v"
Source: 203.0.113.10/32
Port: 22
Protocol: TCP
```

This allows SSH only from one IP.

## 9. Network Security Group

A **Network Security Group**, or **NSG**, controls traffic for specific resources.

Security Lists work on subnets.

NSGs work on selected resources.

```text id="oibqhx"
Security List → Subnet level
NSG           → Resource level
```

Example:

```text id="oo066f"
Web Server NSG
├── Allow HTTP 80
├── Allow HTTPS 443
└── Allow SSH 22 from my IP
```

## Security List vs NSG

| Security List               | NSG                            |
| --------------------------- | ------------------------------ |
| Applied to subnet           | Applied to specific resource   |
| Broader control             | More specific control          |
| Good for simple labs        | Better for real projects       |
| Affects resources in subnet | Affects attached resource only |

## Common Ports

| Port | Usage           |
| ---: | --------------- |
|   22 | SSH             |
|   80 | HTTP            |
|  443 | HTTPS           |
| 3306 | MySQL           |
| 5432 | PostgreSQL      |
| 8080 | Web app testing |

## Basic VCN Architecture

```text id="af106m"
VCN: 10.0.0.0/16

├── Public Subnet: 10.0.1.0/24
│   ├── Load Balancer
│   └── Web Server
│
└── Private Subnet: 10.0.2.0/24
    └── Database
```

Traffic flow:

```text id="kfcpta"
User
 ↓
Internet
 ↓
Internet Gateway
 ↓
Load Balancer
 ↓
Web Server
 ↓
Database
```

## Beginner Lab Design

For learning, start with a simple VCN:

```text id="lvcmfv"
VCN: 10.0.0.0/16
└── Public Subnet: 10.0.1.0/24
    └── Ubuntu Compute Instance
```

Allow only:

```text id="ykih22"
SSH 22 from your IP
HTTP 80 from internet
HTTPS 443 from internet
```

Do not open all ports.

## Example Security Rules

Allow SSH from your IP only:

```text id="q76v7r"
Source CIDR: your-public-ip/32
Protocol: TCP
Destination Port: 22
```

Allow HTTP from internet:

```text id="grtzy8"
Source CIDR: 0.0.0.0/0
Protocol: TCP
Destination Port: 80
```

Allow HTTPS from internet:

```text id="71e4xp"
Source CIDR: 0.0.0.0/0
Protocol: TCP
Destination Port: 443
```

## Important Security Note

Do not allow SSH from everywhere unless this is only a temporary lab.

Bad:

```text id="6xx78t"
0.0.0.0/0 → port 22
```

Better:

```text id="d6hvzp"
your-public-ip/32 → port 22
```

## Console Path

To create or manage a VCN:

```text id="ajyj4f"
OCI Console
→ Networking
→ Virtual Cloud Networks
```

Inside a VCN, you can manage:

```text id="derb5y"
Subnets
Route Tables
Security Lists
Internet Gateways
NAT Gateways
Network Security Groups
```

## Common Beginner Mistakes

### Instance Has Public IP but Still Not Accessible

Check these things:

```text id="t8n8x9"
Public IP exists
Internet Gateway exists
Route Table points to Internet Gateway
Security rule allows the port
Operating system firewall allows the port
Application is listening on the correct port
```

### Opening SSH to the Whole Internet

Bad:

```text id="0s1gun"
Allow 0.0.0.0/0 on port 22
```

Better:

```text id="pget4u"
Allow only your IP on port 22
```

### Putting Database in Public Subnet

Bad:

```text id="d5d60i"
Public Subnet
└── Database
```

Better:

```text id="rmp86s"
Private Subnet
└── Database
```

### Confusing Route Table with Security Rules

Route Table decides where traffic goes.

Security rules decide whether traffic is allowed.

```text id="asffqe"
Route Table → path
Security Rule → permission
```

## Simple Troubleshooting Flow

If you cannot access your server:

```text id="dr1hcb"
1. Check instance is running
2. Check public IP
3. Check subnet is public
4. Check route table has Internet Gateway
5. Check security rule allows the port
6. Check server firewall
7. Check application is running
```

## Summary

```text id="7kx2kg"
VCN              → Private network in OCI
CIDR Block       → IP range for the network
Subnet           → Smaller network inside VCN
Public Subnet    → Can connect to internet with public IP
Private Subnet   → No direct internet access
Route Table      → Controls traffic path
Internet Gateway → Connects public subnet to internet
NAT Gateway      → Lets private resources access internet
Security List    → Subnet-level traffic rules
NSG              → Resource-level traffic rules
```

> A VCN is the foundation of OCI networking. It controls where resources live, how they communicate, and what traffic is allowed.

