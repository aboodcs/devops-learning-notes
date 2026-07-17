# 01 - OCI Overview

**OCI** means **Oracle Cloud Infrastructure**.

OCI is Oracle's cloud platform used to create and manage cloud resources such as:

```text id="vct206"
Compute Instances
Virtual Networks
Storage
Databases
Load Balancers
Security Services
Kubernetes Clusters
```

OCI allows you to run applications without buying and managing physical servers yourself.

## What Is Cloud Computing?

Cloud computing means using servers, storage, databases, and networking over the internet.

Instead of buying your own server, you use cloud services from a provider.

Examples of cloud providers:

```text id="9qxg16"
Oracle Cloud Infrastructure
Amazon Web Services
Microsoft Azure
Google Cloud Platform
```

## Why Do We Use OCI?

Without cloud computing, a company needs to buy physical servers.

That means the company must manage:

```text id="pi1w97"
Hardware
Power
Cooling
Network cables
Physical security
Maintenance
Scaling
Backups
```

With OCI, Oracle manages the physical infrastructure, and you create resources from the console or using code.

```text id="3pkqi3"
You manage cloud resources
Oracle manages physical data centers
```

## What Can You Create in OCI?

OCI provides many cloud services.

For beginners, focus on these first:

```text id="9152zu"
Compute
Networking
Storage
IAM
Load Balancer
Databases
Monitoring
Terraform
```

## 1. Compute

**Compute** means virtual servers in the cloud.

In OCI, a virtual server is called a:

```text id="xji9f9"
Compute Instance
```

A Compute Instance is like a Linux or Windows machine running in Oracle Cloud.

You can use it to run:

```text id="s6kcc0"
Web applications
Docker containers
APIs
Databases
DevOps tools
Testing environments
```

Example:

```text id="03qnk9"
OCI Compute Instance
└── Ubuntu Server
    └── Docker
        └── Application
```

## 2. Networking

OCI networking allows cloud resources to communicate.

The main networking service is:

```text id="v8lnip"
VCN = Virtual Cloud Network
```

A VCN is like your private network inside OCI.

Inside a VCN, you can create:

```text id="v3ehip"
Subnets
Route Tables
Internet Gateway
NAT Gateway
Security Lists
Network Security Groups
```

Example:

```text id="y26qt8"
VCN
├── Public Subnet
│   └── Web Server
└── Private Subnet
    └── Database
```

## 3. Storage

OCI provides storage services for different use cases.

Main storage types:

```text id="wmw356"
Block Volume
Object Storage
File Storage
```

### Block Volume

A Block Volume is like a virtual hard disk attached to a Compute Instance.

Use it for:

```text id="h9f8ky"
Operating system disks
Application data
Database storage
Docker volumes
```

### Object Storage

Object Storage is used to store files as objects.

Use it for:

```text id="jey1qm"
Backups
Images
Videos
Logs
Static files
Archives
```

### File Storage

File Storage provides shared file systems.

Use it when many servers need to access the same files.

## 4. IAM

**IAM** means **Identity and Access Management**.

IAM controls:

```text id="8sjfga"
Who can access OCI
What they can do
Where they can do it
```

Main IAM parts:

```text id="nx8ve3"
Users
Groups
Policies
Compartments
Domains
```

Example:

```text id="4swagq"
User → Group → Policy → Permission
```

A user does not get access automatically.

Access is given through groups and policies.

## 5. Compartments

A **Compartment** is a logical place to organize OCI resources.

Example:

```text id="oxvksw"
Tenancy
├── Dev Compartment
├── Test Compartment
└── Production Compartment
```

You can place resources inside compartments:

```text id="x09s89"
Compute Instances
VCNs
Subnets
Block Volumes
Load Balancers
Databases
```

Compartments help with organization and access control.

## 6. Load Balancer

A **Load Balancer** distributes traffic across multiple servers.

Example:

```text id="2aebg8"
User
 │
 ▼
Load Balancer
 ├── Compute Instance 1
 ├── Compute Instance 2
 └── Compute Instance 3
```

If one server fails, traffic can go to another healthy server.

Load Balancers are used for:

```text id="x4psot"
High availability
Traffic distribution
Production web applications
```

## 7. Databases

Oracle Cloud provides managed database services.

Examples:

```text id="t9smwx"
Oracle Autonomous Database
MySQL Database Service
Database Systems
```

A managed database means OCI handles many database operations for you.

Examples:

```text id="liwls3"
Provisioning
Patching
Backups
Scaling
Monitoring
```

## 8. Monitoring

OCI Monitoring helps you watch your cloud resources.

You can monitor:

```text id="qz2cjl"
CPU usage
Memory usage
Network traffic
Storage usage
Instance health
Application metrics
```

Monitoring helps you know if something is slow, broken, or using too many resources.

## 9. Terraform with OCI

Terraform lets you create OCI resources using code.

Instead of clicking in the OCI Console, you write files:

```text id="8c9v97"
provider.tf
main.tf
variables.tf
terraform.tfvars
outputs.tf
```

Example flow:

```text id="t7gqnb"
Terraform code → OCI Provider → Oracle Cloud resources
```

Terraform is important for DevOps because it makes infrastructure repeatable and easy to manage.

## OCI Console

The **OCI Console** is the web interface used to manage Oracle Cloud.

From the console, you can create and manage:

```text id="t226ag"
Users
Groups
Policies
Compartments
VCNs
Compute Instances
Storage
Load Balancers
Databases
```

Common console areas:

```text id="s5w8ub"
Identity & Security
Networking
Compute
Storage
Databases
Developer Services
Observability & Management
```

## OCI Basic Architecture Example

A simple application in OCI may look like this:

```text id="xteg7n"
OCI Tenancy
└── Dev Compartment
    └── VCN
        ├── Public Subnet
        │   ├── Load Balancer
        │   └── Compute Instance
        │
        └── Private Subnet
            └── Database
```

Traffic flow:

```text id="4dk64i"
User
 ↓
Internet
 ↓
Load Balancer
 ↓
Compute Instance
 ↓
Database
```

## Important OCI Terms

```text id="dnkjg7"
Tenancy       → Your main OCI account
Region        → Geographic location of OCI data centers
Availability Domain → Isolated data center inside a region
Compartment   → Logical container for resources
VCN           → Private network in OCI
Subnet        → Smaller network inside a VCN
Compute Instance → Virtual server
Block Volume  → Virtual disk
Object Storage → File/object storage service
IAM           → Access control system
Policy        → Permission rule
```

## OCI vs Traditional Data Center

| Traditional Data Center  | OCI                          |
| ------------------------ | ---------------------------- |
| Buy physical servers     | Create virtual servers       |
| Manage hardware yourself | Oracle manages hardware      |
| Scaling is slower        | Scaling is faster            |
| High upfront cost        | Pay for cloud resources      |
| Manual setup             | Console, CLI, API, Terraform |

## Beginner Learning Order

For learning OCI, study in this order:

```text id="4fyznw"
1. OCI overview
2. Tenancy and compartments
3. IAM users, groups, and policies
4. Regions and availability domains
5. VCN networking
6. Compute instances
7. Storage
8. Load balancer
9. Terraform with OCI
```

## Summary

```text id="fa3275"
OCI        → Oracle Cloud Infrastructure
Compute    → Virtual servers
VCN        → Virtual cloud network
Storage    → Save data and files
IAM        → Control access
Compartment → Organize resources
Load Balancer → Distribute traffic
Terraform  → Create OCI resources with code
```

> OCI is Oracle's cloud platform for running applications, networks, storage, databases, and DevOps infrastructure in the cloud.

