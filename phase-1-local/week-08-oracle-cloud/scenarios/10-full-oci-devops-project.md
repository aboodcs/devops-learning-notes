# Scenario 10 - Full OCI DevOps Project

## Goal

In this final scenario, we will build a complete production-style DevOps project on Oracle Cloud Infrastructure.

This project combines everything learned in the previous scenarios:

* OCI networking
* Public and private subnets
* Internet Gateway
* NAT Gateway
* Service Gateway
* Network Security Groups
* Compute Instances
* Load Balancer
* Block Volume
* Object Storage
* IAM
* Dynamic Groups
* Instance Principals
* Terraform
* Docker
* GitHub Actions
* Monitoring
* Logging
* Backups
* Failure testing
* Disaster recovery
* Security controls

The objective is not only to make the application work.

The objective is to build an environment that is:

* Repeatable
* Secure
* Highly available
* Observable
* Recoverable
* Automated
* Easy to maintain
* Safe to destroy and recreate

---

# Project Overview

We will deploy a containerized web application on two private OCI Compute Instances.

Internet users will access the application through a public Load Balancer.

The application servers will not have public IP addresses.

Each application server will run:

* Linux
* Docker
* A Flask application
* Nginx
* A health-check endpoint
* OCI Monitoring Agent
* Backup automation

Application data will be stored on Block Volume storage.

Backups will be uploaded to Object Storage through a Service Gateway.

Infrastructure will be created using Terraform.

GitHub Actions will validate, plan, and deploy the Terraform configuration.

---

# Final Architecture

```text
                              Developers
                                  │
                                  ▼
                           GitHub Repository
                                  │
                                  ▼
                         GitHub Actions CI/CD
                                  │
                                  ▼
                              Terraform
                                  │
                                  ▼
                     Oracle Cloud Infrastructure
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
       IAM                    Networking               Observability
        │                         │                         │
        │                         ▼                         ├── Monitoring
        │                        VCN                        ├── Logging
        │                         │                         ├── Alarms
        │          ┌──────────────┴──────────────┐          └── Audit
        │          │                             │
        │          ▼                             ▼
        │   Public Subnet                 Private App Subnet
        │          │                             │
        │          ▼                 ┌───────────┴───────────┐
        │   Public Load Balancer     │                       │
        │          │                 ▼                       ▼
        │          └──────────► App Server 01         App Server 02
        │                            │                       │
        │                            ├── Docker              ├── Docker
        │                            ├── Nginx               ├── Nginx
        │                            ├── Flask               ├── Flask
        │                            └── Block Volume        └── Block Volume
        │                                    │                       │
        │                                    └───────────┬───────────┘
        │                                                │
        │                                                ▼
        │                                          Backup Script
        │                                                │
        │                                                ▼
        │                                         Service Gateway
        │                                                │
        │                                                ▼
        └──────────────────────────────────────► Object Storage
```

---

# User Traffic Flow

```text
Internet User
      │
      ▼
Public Load Balancer IP
      │
      ▼
Load Balancer Listener
      │
      ▼
Backend Set
      │
      ├── App Server 01
      └── App Server 02
              │
              ▼
            Nginx
              │
              ▼
       Flask Container
              │
              ▼
        Application Response
```

The Load Balancer sends traffic only to healthy application servers.

---

# Administrative Flow

```text
DevOps Engineer
      │
      ▼
OCI Bastion
      │
      ▼
Private Compute Instance
```

The Compute Instances do not have public IP addresses.

SSH is not exposed directly to the Internet.

---

# Outbound Internet Flow

The private Compute Instances may need to:

* Download packages
* Pull Docker images
* Access GitHub
* Reach external APIs

Traffic flow:

```text
Private Compute Instance
          │
          ▼
    Private Route Table
          │
          ▼
       NAT Gateway
          │
          ▼
        Internet
```

---

# Object Storage Flow

Backups should not use the public Internet.

```text
Private Compute Instance
          │
          ▼
    Private Route Table
          │
          ▼
     Service Gateway
          │
          ▼
Oracle Services Network
          │
          ▼
    Object Storage Bucket
```

---

# Main Architecture Layers

The project is divided into several layers.

```text
Identity Layer
Network Layer
Compute Layer
Application Layer
Storage Layer
Automation Layer
Observability Layer
Recovery Layer
```

Each layer has a separate responsibility.

---

# Identity Layer

The identity layer controls:

* Who can access OCI
* What Terraform can create
* What GitHub Actions can manage
* What Compute Instances can access
* Who can view production resources
* Who can modify networking
* Who can delete infrastructure

Main services:

* IAM Users
* IAM Groups
* IAM Policies
* Dynamic Groups
* Instance Principals
* Identity Domains
* MFA

---

# Network Layer

The network layer controls communication between resources.

It contains:

* VCN
* Public subnet
* Private subnet
* Internet Gateway
* NAT Gateway
* Service Gateway
* Route Tables
* Network Security Groups
* DNS
* Public Load Balancer

---

# Compute Layer

The Compute layer runs the application.

It contains:

* Two private Compute Instances
* Boot Volumes
* Block Volumes
* VNICs
* cloud-init
* Docker
* System services

---

# Application Layer

The application layer contains:

* Flask application
* Nginx reverse proxy
* Docker image
* Docker container
* Health endpoint
* Environment variables
* Application logs

---

# Storage Layer

The storage layer contains:

* Boot Volumes
* Block Volumes
* Object Storage bucket
* Backup objects
* Retention policies
* Lifecycle policies

---

# Automation Layer

The automation layer contains:

* Terraform
* GitHub Actions
* cloud-init
* Backup scripts
* Deployment scripts
* Validation scripts

---

# Observability Layer

The observability layer contains:

* OCI Monitoring
* OCI Logging
* OCI Audit
* Load Balancer metrics
* Compute metrics
* Application logs
* Alarms
* Notifications

---

# Recovery Layer

The recovery layer contains:

* Block Volume backups
* Object Storage backups
* Restore procedures
* Failure tests
* Recovery Point Objective
* Recovery Time Objective
* Disaster recovery documentation

---

# OCI Services Used

| OCI Service      | Purpose                                |
| ---------------- | -------------------------------------- |
| Compartment      | Isolate and organize project resources |
| IAM              | Control access                         |
| Identity Domain  | Manage users and groups                |
| Dynamic Group    | Identify Compute Instances             |
| VCN              | Provide the cloud network              |
| Public Subnet    | Host the Load Balancer                 |
| Private Subnet   | Host application servers               |
| Internet Gateway | Provide public Load Balancer access    |
| NAT Gateway      | Provide outbound Internet access       |
| Service Gateway  | Provide private OCI service access     |
| Route Table      | Direct network traffic                 |
| NSG              | Control resource traffic               |
| Load Balancer    | Distribute user traffic                |
| Compute          | Run application workloads              |
| Block Volume     | Store persistent application data      |
| Object Storage   | Store backups                          |
| Monitoring       | Collect metrics                        |
| Logging          | Centralize logs                        |
| Audit            | Track OCI API activity                 |
| Notifications    | Deliver alerts                         |
| Terraform        | Create infrastructure                  |
| Vault            | Protect secrets and encryption keys    |

---

# Project Repository Structure

```text
oci-full-devops-project/
├── README.md
├── Makefile
├── .gitignore
├── .github/
│   └── workflows/
│       ├── terraform-check.yml
│       ├── terraform-plan.yml
│       ├── terraform-apply.yml
│       └── application-build.yml
│
├── application/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   └── templates/
│       └── index.html
│
├── nginx/
│   └── default.conf
│
├── terraform/
│   ├── versions.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── locals.tf
│   ├── data.tf
│   ├── networking.tf
│   ├── security.tf
│   ├── compute.tf
│   ├── storage.tf
│   ├── load-balancer.tf
│   ├── iam.tf
│   ├── monitoring.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   ├── cloud-init/
│   │   ├── app-server-01.yaml
│   │   └── app-server-02.yaml
│   └── modules/
│       ├── network/
│       ├── compute/
│       ├── storage/
│       └── load-balancer/
│
├── scripts/
│   ├── deploy-application.sh
│   ├── backup-application.sh
│   ├── restore-application.sh
│   ├── validate-environment.sh
│   └── test-failover.sh
│
├── docs/
│   ├── architecture.md
│   ├── security.md
│   ├── deployment.md
│   ├── monitoring.md
│   ├── backup-and-restore.md
│   ├── disaster-recovery.md
│   ├── troubleshooting.md
│   └── runbook.md
│
└── screenshots/
```

---

# Resource Naming Strategy

Use a consistent prefix.

Example project prefix:

```text
oci-devops
```

Resources:

```text
oci-devops-vcn
oci-devops-public-subnet
oci-devops-private-app-subnet
oci-devops-internet-gateway
oci-devops-nat-gateway
oci-devops-service-gateway
oci-devops-public-route-table
oci-devops-private-route-table
oci-devops-load-balancer-nsg
oci-devops-application-nsg
oci-devops-load-balancer
oci-devops-app-server-01
oci-devops-app-server-02
oci-devops-app-data-01
oci-devops-app-data-02
oci-devops-backups
```

A consistent naming strategy makes troubleshooting easier.

---

# Tagging Strategy

Every resource should have tags.

Example:

```text
Project:
OCI-Full-DevOps-Project

Environment:
Development

Owner:
Abdulrahman

ManagedBy:
Terraform

CostCenter:
Learning

AutoDestroy:
true
```

Terraform example:

```hcl
locals {
  common_tags = {
    Project     = "OCI-Full-DevOps-Project"
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "Terraform"
    CostCenter  = "Learning"
  }
}
```

Then:

```hcl
freeform_tags = local.common_tags
```

---

# Compartment Design

Create a project Compartment.

```text
Tenancy
└── OCI-DevOps-Project
```

A stronger environment structure:

```text
Tenancy
└── OCI-DevOps
    ├── Development
    ├── Staging
    └── Production
```

For this lab, start with:

```text
OCI-DevOps-Development
```

---

# IAM Groups

Recommended groups:

```text
terraform-operators
devops-engineers
network-admins
security-auditors
production-readonly
```

---

# Terraform Operators

The `terraform-operators` Group manages the infrastructure used by Terraform.

Conceptual policies:

```text
Allow group terraform-operators
to manage virtual-network-family
in compartment OCI-DevOps-Development
```

```text
Allow group terraform-operators
to manage instance-family
in compartment OCI-DevOps-Development
```

```text
Allow group terraform-operators
to manage volume-family
in compartment OCI-DevOps-Development
```

```text
Allow group terraform-operators
to manage load-balancers
in compartment OCI-DevOps-Development
```

```text
Allow group terraform-operators
to manage object-family
in compartment OCI-DevOps-Development
```

Avoid granting:

```text
manage all-resources in tenancy
```

unless the identity truly requires tenancy-wide administration.

---

# DevOps Engineers

The `devops-engineers` Group may manage application and Compute resources.

Example:

```text
Allow group devops-engineers
to manage instance-family
in compartment OCI-DevOps-Development
```

```text
Allow group devops-engineers
to manage volume-family
in compartment OCI-DevOps-Development
```

```text
Allow group devops-engineers
to manage load-balancers
in compartment OCI-DevOps-Development
```

```text
Allow group devops-engineers
to use virtual-network-family
in compartment OCI-DevOps-Development
```

---

# Network Administrators

```text
Allow group network-admins
to manage virtual-network-family
in compartment OCI-DevOps-Development
```

This separates network administration from normal application deployment.

---

# Security Auditors

```text
Allow group security-auditors
to read all-resources
in compartment OCI-DevOps-Development
```

Auditors should not be able to change resources.

---

# Dynamic Group for Compute Instances

The application servers need access to Object Storage.

Create a Dynamic Group:

```text
oci-devops-app-instances
```

A simple matching rule may use the Compartment:

```text
instance.compartment.id = 'COMPARTMENT_OCID'
```

A stronger production design uses tags so only approved application servers match.

Conceptually:

```text
All Compute Instances with:
Role = ApplicationServer
```

---

# Instance Principal Policy

Allow the Compute Instances to manage backup objects.

Conceptual policy:

```text
Allow dynamic-group oci-devops-app-instances
to manage objects
in compartment OCI-DevOps-Development
```

The instances normally do not need permission to delete or manage the bucket itself.

---

# Networking Design

## VCN CIDR

```text
10.0.0.0/16
```

## Public Subnet

```text
10.0.1.0/24
```

Used for:

* Public Load Balancer

## Private Application Subnet

```text
10.0.2.0/24
```

Used for:

* Application Server 01
* Application Server 02

Optional future database subnet:

```text
10.0.3.0/24
```

---

# Network Architecture

```text
VCN: 10.0.0.0/16
│
├── Public Subnet: 10.0.1.0/24
│   └── Public Load Balancer
│
└── Private Application Subnet: 10.0.2.0/24
    ├── App Server 01
    └── App Server 02
```

---

# Internet Gateway

The Internet Gateway allows the public Load Balancer to communicate with Internet users.

```text
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Subnet
   │
   ▼
Load Balancer
```

---

# NAT Gateway

The private application servers use the NAT Gateway for outbound Internet access.

```text
Private App Server
        │
        ▼
Private Route Table
        │
        ▼
NAT Gateway
        │
        ▼
Internet
```

The NAT Gateway supports:

* Package downloads
* Docker image pulls
* External API calls
* GitHub access

It does not allow Internet users to connect directly to the instances.

---

# Service Gateway

The Service Gateway provides private access to Object Storage.

```text
Private App Server
        │
        ▼
Service Gateway
        │
        ▼
Object Storage
```

This keeps backup traffic on Oracle's network.

---

# Public Route Table

Route:

```text
0.0.0.0/0 → Internet Gateway
```

Attached to:

```text
Public Subnet
```

---

# Private Route Table

Routes:

```text
0.0.0.0/0 → NAT Gateway
```

```text
Regional Oracle Services → Service Gateway
```

Attached to:

```text
Private Application Subnet
```

---

# Network Security Groups

Create separate NSGs.

```text
load-balancer-nsg
application-nsg
```

Do not use one large NSG for every resource.

---

# Load Balancer NSG

## Ingress HTTP

```text
Source:
0.0.0.0/0

Protocol:
TCP

Port:
80
```

## Ingress HTTPS

```text
Source:
0.0.0.0/0

Protocol:
TCP

Port:
443
```

## Egress to Application Servers

```text
Destination:
application-nsg

Protocol:
TCP

Port:
8080
```

---

# Application NSG

## Ingress from Load Balancer

```text
Source:
load-balancer-nsg

Protocol:
TCP

Port:
8080
```

## SSH from Bastion

```text
Source:
Approved Bastion source

Protocol:
TCP

Port:
22
```

## Egress HTTPS

```text
Destination:
0.0.0.0/0

Protocol:
TCP

Port:
443
```

## Egress HTTP

```text
Destination:
0.0.0.0/0

Protocol:
TCP

Port:
80
```

---

# Security Relationship

```text
Internet
   │
   ▼
Load Balancer NSG
   │
   ▼
Load Balancer
   │
   ▼
Application NSG
   │
   ▼
Private App Servers
```

The application servers do not accept port `8080` from the entire Internet.

They accept it only from the Load Balancer NSG.

---

# Load Balancer Design

Create one public Load Balancer.

```text
Public Load Balancer
├── Listener: HTTP 80
├── Optional Listener: HTTPS 443
├── Backend Set
├── Health Check
├── Backend 01
└── Backend 02
```

---

# Listener

For the first version:

```text
Protocol:
HTTP

Port:
80
```

Production improvement:

```text
Protocol:
HTTPS

Port:
443
```

HTTP traffic should then redirect to HTTPS.

---

# Backend Set

Use:

```text
Policy:
Round Robin
```

Backends:

```text
App Server 01:8080
App Server 02:8080
```

---

# Health Check

Configure:

```text
Protocol:
HTTP
```

```text
Port:
8080
```

```text
Path:
/health
```

Expected response:

```text
HTTP 200
```

The Load Balancer should stop sending traffic to unhealthy servers.

---

# Compute Design

Create two private Compute Instances.

```text
oci-devops-app-server-01
oci-devops-app-server-02
```

Each instance should have:

* No public IP
* Private subnet
* Application NSG
* Boot Volume
* Block Volume
* cloud-init
* Docker
* Nginx
* Flask container
* Monitoring configuration

---

# Fault Domain Placement

Place the two instances in different Fault Domains when possible.

```text
Availability Domain
├── Fault Domain 1
│   └── App Server 01
│
└── Fault Domain 2
    └── App Server 02
```

This reduces the chance that one hardware failure affects both servers.

---

# Application Design

The application will be a simple Flask service.

Endpoints:

```text
/
```

```text
/health
```

```text
/info
```

---

# application/app.py

```python
import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
HOSTNAME = socket.gethostname()


@app.get("/")
def home():
    return render_template(
        "index.html",
        hostname=HOSTNAME,
        version=APP_VERSION,
        environment=ENVIRONMENT,
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "hostname": HOSTNAME,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ), 200


@app.get("/info")
def info():
    return jsonify(
        {
            "application": "OCI DevOps Demo",
            "version": APP_VERSION,
            "environment": ENVIRONMENT,
            "hostname": HOSTNAME,
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

---

# application/requirements.txt

```text
Flask==3.1.1
gunicorn==23.0.0
```

---

# Application Template

Create:

```text
application/templates/index.html
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >
    <title>OCI DevOps Project</title>
</head>
<body>
    <h1>OCI Full DevOps Project</h1>

    <p>
        This application is running on Oracle Cloud Infrastructure.
    </p>

    <ul>
        <li>Hostname: {{ hostname }}</li>
        <li>Environment: {{ environment }}</li>
        <li>Version: {{ version }}</li>
    </ul>
</body>
</html>
```

The hostname helps prove that the Load Balancer distributes traffic between servers.

---

# Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system appgroup \
    && useradd --system --gid appgroup appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')"

CMD [
    "gunicorn",
    "--bind",
    "0.0.0.0:8080",
    "--workers",
    "2",
    "--threads",
    "4",
    "--access-logfile",
    "-",
    "--error-logfile",
    "-",
    "app:app"
]
```

---

# Why Use Gunicorn?

The Flask development server is not designed for production workloads.

Gunicorn provides:

* Multiple workers
* Better concurrency
* Process management
* Better failure isolation
* Production-style serving

---

# Docker Ignore File

Create:

```text
application/.dockerignore
```

```text
__pycache__/
*.pyc
*.pyo
.env
.git/
.gitignore
tests/
README.md
```

---

# Build the Application Image

From the application directory:

```bash
docker build -t oci-devops-app:1.0.0 .
```

Run locally:

```bash
docker run -d \
  --name oci-devops-app \
  -p 8080:8080 \
  -e APP_VERSION=1.0.0 \
  -e ENVIRONMENT=development \
  oci-devops-app:1.0.0
```

Test:

```bash
curl http://localhost:8080
```

```bash
curl http://localhost:8080/health
```

---

# Nginx Reverse Proxy

Nginx may listen on port `80` locally and forward requests to the container on port `8080`.

```text
Load Balancer
      │
      ▼
Nginx :80
      │
      ▼
Flask Container :8080
```

However, to simplify the first project version, the Load Balancer can connect directly to port `8080`.

Nginx can later be used for:

* TLS termination inside the server
* Request buffering
* Static files
* Rate limiting
* Local routing
* Custom access logs

---

# Block Volume Design

Each application server receives one Block Volume.

```text
App Server 01
      │
      ▼
Block Volume 01
      │
      ▼
/data
```

```text
App Server 02
      │
      ▼
Block Volume 02
      │
      ▼
/data
```

Suggested directories:

```text
/data/application
/data/uploads
/data/backups
/data/logs
```

---

# Important Storage Warning

Two separate Block Volumes do not automatically provide shared data.

```text
App Server 01 → Block Volume 01
App Server 02 → Block Volume 02
```

If users upload a file to Server 01, Server 02 will not automatically have that file.

For truly shared application files, use:

* Object Storage
* File Storage
* Database storage
* Application-level synchronization

Block Volume is best for dedicated instance storage.

---

# Recommended Stateless Application Design

Application servers should be stateless where possible.

Do not store:

* User sessions in memory
* Important uploads only on one server
* Critical configuration only on local disk

Use external systems for shared state.

Examples:

```text
Sessions → Redis
Uploads → Object Storage
Database → Managed database
Secrets → Vault
Logs → Logging service
```

---

# Boot Volume vs Block Volume

```text
Boot Volume
└── Operating system and application runtime

Block Volume
└── Persistent local application data
```

The application should continue to work if the instance is replaced and the volume is reattached.

---

# Object Storage Backup Bucket

Create a private bucket:

```text
oci-devops-application-backups
```

Recommended settings:

```text
Visibility:
Private
```

```text
Versioning:
Enabled
```

```text
Default Tier:
Standard
```

Possible prefixes:

```text
daily/
weekly/
monthly/
database/
logs/
```

---

# Backup Flow

```text
Application Data
      │
      ▼
Create Compressed Archive
      │
      ▼
Upload with Instance Principal
      │
      ▼
Service Gateway
      │
      ▼
Object Storage
      │
      ▼
Verify Object
```

---

# Backup Script

Create:

```text
scripts/backup-application.sh
```

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

BUCKET_NAME="${BUCKET_NAME:-oci-devops-application-backups}"
SOURCE_DIRECTORY="${SOURCE_DIRECTORY:-/data/application}"
LOCAL_BACKUP_DIRECTORY="${LOCAL_BACKUP_DIRECTORY:-/data/backups}"
LOG_FILE="${LOG_FILE:-/var/log/oci-devops-backup.log}"

TIMESTAMP="$(date -u +"%Y-%m-%d-%H%M%S")"
YEAR_MONTH="$(date -u +"%Y/%m")"

BACKUP_FILENAME="application-${TIMESTAMP}.tar.gz"
BACKUP_FILE="${LOCAL_BACKUP_DIRECTORY}/${BACKUP_FILENAME}"
OBJECT_NAME="daily/${YEAR_MONTH}/${BACKUP_FILENAME}"

log() {
    printf '%s %s\n' \
        "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        "$1" |
        tee -a "$LOG_FILE"
}

cleanup() {
    if [[ -f "$BACKUP_FILE" ]]; then
        rm -f "$BACKUP_FILE"
    fi
}

trap cleanup EXIT

if [[ ! -d "$SOURCE_DIRECTORY" ]]; then
    log "ERROR: Source directory not found: ${SOURCE_DIRECTORY}"
    exit 1
fi

mkdir -p "$LOCAL_BACKUP_DIRECTORY"
touch "$LOG_FILE"

log "Starting application backup"

tar \
    -czf "$BACKUP_FILE" \
    -C "$(dirname "$SOURCE_DIRECTORY")" \
    "$(basename "$SOURCE_DIRECTORY")"

if [[ ! -s "$BACKUP_FILE" ]]; then
    log "ERROR: Backup file is missing or empty"
    exit 1
fi

log "Created backup: ${BACKUP_FILE}"

oci os object put \
    --bucket-name "$BUCKET_NAME" \
    --file "$BACKUP_FILE" \
    --name "$OBJECT_NAME" \
    --force \
    --auth instance_principal

log "Uploaded object: ${OBJECT_NAME}"

oci os object head \
    --bucket-name "$BUCKET_NAME" \
    --name "$OBJECT_NAME" \
    --auth instance_principal \
    >/dev/null

log "Object verification successful"
log "Backup completed"
```

Make it executable:

```bash
chmod +x scripts/backup-application.sh
```

---

# Backup Scheduling

Use a systemd timer.

Service:

```ini
[Unit]
Description=Back up OCI DevOps application data
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-application.sh
```

Timer:

```ini
[Unit]
Description=Run OCI DevOps application backup daily

[Timer]
OnCalendar=*-*-* 02:00:00 UTC
Persistent=true
Unit=oci-devops-backup.service

[Install]
WantedBy=timers.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now oci-devops-backup.timer
```

Verify:

```bash
systemctl list-timers --all
```

---

# Terraform Project

Terraform is responsible for creating the infrastructure.

It should not contain application secrets.

Suggested Terraform structure:

```text
terraform/
├── versions.tf
├── provider.tf
├── variables.tf
├── locals.tf
├── data.tf
├── networking.tf
├── security.tf
├── compute.tf
├── storage.tf
├── load-balancer.tf
├── iam.tf
├── monitoring.tf
└── outputs.tf
```

---

# versions.tf

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 7.0"
    }
  }
}
```

---

# provider.tf

```hcl
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}
```

A stronger CI/CD design should use short-lived authentication rather than storing long-lived API credentials.

---

# variables.tf

```hcl
variable "tenancy_ocid" {
  description = "OCI tenancy OCID"
  type        = string
  sensitive   = true
}

variable "user_ocid" {
  description = "OCI user OCID used by Terraform"
  type        = string
  sensitive   = true
}

variable "fingerprint" {
  description = "OCI API key fingerprint"
  type        = string
  sensitive   = true
}

variable "private_key_path" {
  description = "Path to the OCI API private key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "OCI region"
  type        = string
}

variable "compartment_ocid" {
  description = "Project Compartment OCID"
  type        = string
}

variable "project_name" {
  description = "Resource name prefix"
  type        = string
  default     = "oci-devops"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
}

variable "owner" {
  description = "Resource owner"
  type        = string
  default     = "Abdulrahman"
}

variable "vcn_cidr" {
  description = "VCN CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet CIDR block"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_app_subnet_cidr" {
  description = "Private application subnet CIDR block"
  type        = string
  default     = "10.0.2.0/24"
}

variable "instance_shape" {
  description = "Compute instance shape"
  type        = string
  default     = "VM.Standard.E4.Flex"
}

variable "instance_ocpus" {
  description = "OCPUs per application server"
  type        = number
  default     = 1
}

variable "instance_memory_gbs" {
  description = "Memory in GB per application server"
  type        = number
  default     = 6
}

variable "image_ocid" {
  description = "Operating system image OCID"
  type        = string
}

variable "ssh_public_key_path" {
  description = "SSH public key path"
  type        = string
}

variable "application_port" {
  description = "Application backend port"
  type        = number
  default     = 8080
}

variable "block_volume_size_gbs" {
  description = "Application Block Volume size"
  type        = number
  default     = 50
}
```

---

# locals.tf

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "Terraform"
  }
}
```

---

# data.tf

```hcl
data "oci_identity_availability_domains" "available" {
  compartment_id = var.tenancy_ocid
}
```

---

# networking.tf

```hcl
resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_ocid
  cidr_blocks     = [var.vcn_cidr]
  display_name    = "${var.project_name}-vcn"
  dns_label       = "ocidevops"

  freeform_tags = local.common_tags
}
```

---

# Internet Gateway

```hcl
resource "oci_core_internet_gateway" "main" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-igw"
  enabled        = true

  freeform_tags = local.common_tags
}
```

---

# NAT Gateway

```hcl
resource "oci_core_nat_gateway" "main" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-nat-gateway"

  freeform_tags = local.common_tags
}
```

---

# Service Gateway

```hcl
data "oci_core_services" "all_services" {
  filter {
    name   = "name"
    values = [".*All.*Services.*"]
    regex  = true
  }
}

resource "oci_core_service_gateway" "main" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-service-gateway"

  services {
    service_id = data.oci_core_services.all_services.services[0].id
  }

  freeform_tags = local.common_tags
}
```

---

# Public Route Table

```hcl
resource "oci_core_route_table" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-public-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.main.id
  }

  freeform_tags = local.common_tags
}
```

---

# Private Route Table

```hcl
resource "oci_core_route_table" "private" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-private-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_nat_gateway.main.id
  }

  route_rules {
    destination       = data.oci_core_services.all_services.services[0].cidr_block
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.main.id
  }

  freeform_tags = local.common_tags
}
```

---

# Public Subnet

```hcl
resource "oci_core_subnet" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id

  cidr_block                 = var.public_subnet_cidr
  display_name               = "${var.project_name}-public-subnet"
  dns_label                  = "public"
  route_table_id             = oci_core_route_table.public.id
  prohibit_public_ip_on_vnic = false

  freeform_tags = local.common_tags
}
```

---

# Private Application Subnet

```hcl
resource "oci_core_subnet" "private_app" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id

  cidr_block                 = var.private_app_subnet_cidr
  display_name               = "${var.project_name}-private-app-subnet"
  dns_label                  = "privateapp"
  route_table_id             = oci_core_route_table.private.id
  prohibit_public_ip_on_vnic = true

  freeform_tags = local.common_tags
}
```

---

# security.tf

Create the Load Balancer NSG:

```hcl
resource "oci_core_network_security_group" "load_balancer" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-load-balancer-nsg"

  freeform_tags = local.common_tags
}
```

Create the application NSG:

```hcl
resource "oci_core_network_security_group" "application" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${var.project_name}-application-nsg"

  freeform_tags = local.common_tags
}
```

---

# Allow Public HTTP

```hcl
resource "oci_core_network_security_group_security_rule" "lb_http" {
  network_security_group_id = oci_core_network_security_group.load_balancer.id
  direction                 = "INGRESS"
  protocol                  = "6"

  source      = "0.0.0.0/0"
  source_type = "CIDR_BLOCK"

  tcp_options {
    destination_port_range {
      min = 80
      max = 80
    }
  }

  description = "Allow public HTTP traffic"
}
```

---

# Allow Load Balancer to Application

```hcl
resource "oci_core_network_security_group_security_rule" "app_from_lb" {
  network_security_group_id = oci_core_network_security_group.application.id
  direction                 = "INGRESS"
  protocol                  = "6"

  source      = oci_core_network_security_group.load_balancer.id
  source_type = "NETWORK_SECURITY_GROUP"

  tcp_options {
    destination_port_range {
      min = var.application_port
      max = var.application_port
    }
  }

  description = "Allow application traffic from the Load Balancer"
}
```

---

# Application Egress

```hcl
resource "oci_core_network_security_group_security_rule" "app_egress" {
  network_security_group_id = oci_core_network_security_group.application.id
  direction                 = "EGRESS"
  protocol                  = "all"

  destination      = "0.0.0.0/0"
  destination_type = "CIDR_BLOCK"

  description = "Allow application servers outbound access"
}
```

---

# compute.tf

Create two instances using `count`.

```hcl
resource "oci_core_instance" "application" {
  count = 2

  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.available.availability_domains[0].name
  display_name        = "${var.project_name}-app-server-${count.index + 1}"
  shape               = var.instance_shape

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_memory_gbs
  }

  fault_domain = "FAULT-DOMAIN-${count.index + 1}"

  create_vnic_details {
    subnet_id        = oci_core_subnet.private_app.id
    assign_public_ip = false
    hostname_label   = "appserver${count.index + 1}"

    nsg_ids = [
      oci_core_network_security_group.application.id
    ]
  }

  source_details {
    source_type = "image"
    source_id   = var.image_ocid
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)

    user_data = base64encode(
      templatefile(
        "${path.module}/cloud-init/app-server.yaml",
        {
          server_number = count.index + 1
          environment   = var.environment
        }
      )
    )
  }

  freeform_tags = merge(
    local.common_tags,
    {
      Role   = "ApplicationServer"
      Server = tostring(count.index + 1)
    }
  )
}
```

---

# Important Fault Domain Warning

Do not assume every Availability Domain always exposes the same Fault Domain names.

Verify available placement options in the selected Region and shape.

For a more flexible configuration, read Fault Domains using an OCI data source instead of hardcoding them.

---

# cloud-init

Create:

```text
terraform/cloud-init/app-server.yaml
```

```yaml
#cloud-config

package_update: true

packages:
  - docker.io
  - curl
  - unzip
  - jq

write_files:
  - path: /opt/oci-devops/docker-compose.yml
    owner: root:root
    permissions: "0644"
    content: |
      services:
        application:
          image: oci-devops-app:latest
          container_name: oci-devops-app
          restart: unless-stopped
          ports:
            - "8080:8080"
          environment:
            APP_VERSION: "1.0.0"
            ENVIRONMENT: "${environment}"
            SERVER_NUMBER: "${server_number}"
          volumes:
            - /data/application:/app/data

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - mkdir -p /data/application
  - mkdir -p /opt/oci-devops
```

In a complete deployment, the image must come from a registry accessible by the instance.

---

# Container Registry Design

A production-style project should store the image in a registry.

Possible flow:

```text
GitHub Actions
      │
      ▼
Build Docker Image
      │
      ▼
Container Registry
      │
      ▼
Private Compute Instances
      │
      ▼
Pull Image
```

The registry may be:

* OCI Container Registry
* Another approved private registry

Avoid building production images directly on application servers.

---

# storage.tf

Create one Block Volume per instance.

```hcl
resource "oci_core_volume" "application_data" {
  count = 2

  compartment_id      = var.compartment_ocid
  availability_domain = oci_core_instance.application[count.index].availability_domain
  display_name        = "${var.project_name}-app-data-${count.index + 1}"
  size_in_gbs         = var.block_volume_size_gbs

  freeform_tags = merge(
    local.common_tags,
    {
      Role   = "ApplicationData"
      Server = tostring(count.index + 1)
    }
  )
}
```

---

# Attach Block Volumes

```hcl
resource "oci_core_volume_attachment" "application_data" {
  count = 2

  attachment_type = "paravirtualized"
  instance_id     = oci_core_instance.application[count.index].id
  volume_id       = oci_core_volume.application_data[count.index].id
  display_name    = "${var.project_name}-app-data-attachment-${count.index + 1}"
}
```

Remember:

```text
Terraform attachment
does not automatically mean
Linux filesystem mounted
```

The operating system must still:

* Detect the device
* Format it if new
* Mount it
* Add it to `/etc/fstab`

---

# Object Storage Bucket

```hcl
resource "oci_objectstorage_bucket" "application_backups" {
  compartment_id = var.compartment_ocid
  namespace      = data.oci_objectstorage_namespace.current.namespace
  name           = "${var.project_name}-application-backups"
  access_type    = "NoPublicAccess"
  storage_tier   = "Standard"
  versioning     = "Enabled"

  freeform_tags = local.common_tags
}
```

Namespace data source:

```hcl
data "oci_objectstorage_namespace" "current" {
  compartment_id = var.compartment_ocid
}
```

---

# Load Balancer

```hcl
resource "oci_load_balancer_load_balancer" "main" {
  compartment_id = var.compartment_ocid
  display_name   = "${var.project_name}-load-balancer"
  shape          = "flexible"

  shape_details {
    minimum_bandwidth_in_mbps = 10
    maximum_bandwidth_in_mbps = 100
  }

  subnet_ids = [
    oci_core_subnet.public.id
  ]

  network_security_group_ids = [
    oci_core_network_security_group.load_balancer.id
  ]

  is_private = false

  freeform_tags = local.common_tags
}
```

---

# Backend Set

```hcl
resource "oci_load_balancer_backend_set" "application" {
  name             = "application-backend-set"
  load_balancer_id = oci_load_balancer_load_balancer.main.id
  policy           = "ROUND_ROBIN"

  health_checker {
    protocol          = "HTTP"
    port              = var.application_port
    url_path          = "/health"
    return_code       = 200
    interval_ms       = 10000
    timeout_in_millis = 3000
    retries           = 3
  }
}
```

---

# Backends

```hcl
resource "oci_load_balancer_backend" "application" {
  count = 2

  load_balancer_id = oci_load_balancer_load_balancer.main.id
  backendset_name  = oci_load_balancer_backend_set.application.name

  ip_address = oci_core_instance.application[count.index].private_ip
  port       = var.application_port
  weight     = 1
}
```

---

# Listener

```hcl
resource "oci_load_balancer_listener" "http" {
  load_balancer_id         = oci_load_balancer_load_balancer.main.id
  name                     = "http-listener"
  default_backend_set_name = oci_load_balancer_backend_set.application.name
  port                     = 80
  protocol                 = "HTTP"
}
```

---

# outputs.tf

```hcl
output "load_balancer_ip" {
  description = "Public Load Balancer IP address"
  value       = oci_load_balancer_load_balancer.main.ip_address_details[0].ip_address
}

output "application_url" {
  description = "Public application URL"
  value = "http://${
    oci_load_balancer_load_balancer.main.ip_address_details[0].ip_address
  }"
}

output "application_instance_ids" {
  description = "Application Compute Instance OCIDs"
  value       = oci_core_instance.application[*].id
}

output "application_private_ips" {
  description = "Private IP addresses of the application servers"
  value       = oci_core_instance.application[*].private_ip
}

output "backup_bucket_name" {
  description = "Object Storage backup bucket"
  value       = oci_objectstorage_bucket.application_backups.name
}
```

---

# GitHub Actions Workflow

The CI/CD pipeline should have separate stages.

```text
Push or Pull Request
        │
        ▼
Terraform Format Check
        │
        ▼
Terraform Init
        │
        ▼
Terraform Validate
        │
        ▼
Security Scan
        │
        ▼
Terraform Plan
        │
        ▼
Manual Approval
        │
        ▼
Terraform Apply
        │
        ▼
Application Validation
```

---

# Terraform Check Workflow

Create:

```text
.github/workflows/terraform-check.yml
```

```yaml
name: Terraform Check

on:
  pull_request:
    paths:
      - "terraform/**"
      - ".github/workflows/terraform-check.yml"

jobs:
  terraform-check:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: terraform

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init -backend=false

      - name: Terraform Validate
        run: terraform validate
```

---

# Terraform Plan Workflow

```yaml
name: Terraform Plan

on:
  pull_request:
    paths:
      - "terraform/**"

jobs:
  terraform-plan:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: terraform

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Write OCI private key
        run: |
          printf '%s' "${{ secrets.OCI_PRIVATE_KEY }}" \
            > "${RUNNER_TEMP}/oci_api_key.pem"

          chmod 600 "${RUNNER_TEMP}/oci_api_key.pem"

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        env:
          TF_VAR_tenancy_ocid: ${{ secrets.OCI_TENANCY_OCID }}
          TF_VAR_user_ocid: ${{ secrets.OCI_USER_OCID }}
          TF_VAR_fingerprint: ${{ secrets.OCI_FINGERPRINT }}
          TF_VAR_private_key_path: ${{ runner.temp }}/oci_api_key.pem
          TF_VAR_region: ${{ vars.OCI_REGION }}
          TF_VAR_compartment_ocid: ${{ secrets.OCI_COMPARTMENT_OCID }}
          TF_VAR_image_ocid: ${{ vars.OCI_IMAGE_OCID }}
          TF_VAR_ssh_public_key_path: ${{ runner.temp }}/id_ed25519.pub
        run: terraform plan -no-color
```

A real workflow must also create the public SSH key file or use another deployment mechanism.

---

# Long-Lived Credential Warning

Storing a long-lived OCI API private key in GitHub Secrets works technically, but it is not the strongest design.

A stronger design uses:

* Short-lived credentials
* Workload identity
* OIDC federation when supported
* Dedicated automation identity
* Restricted IAM policy
* Credential rotation

Never store a tenancy administrator key in GitHub.

---

# Terraform Apply Workflow

Production apply should require approval.

Example trigger:

```yaml
on:
  workflow_dispatch:
```

Use a protected GitHub Environment:

```text
production
```

Require reviewers before running the apply job.

Conceptual workflow:

```yaml
name: Terraform Apply

on:
  workflow_dispatch:

jobs:
  apply:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        working-directory: terraform
        run: terraform init

      - name: Terraform Apply
        working-directory: terraform
        run: terraform apply -auto-approve
```

`-auto-approve` is acceptable only after the workflow itself is protected by review and approval controls.

---

# Application Build Workflow

```yaml
name: Build Application

on:
  push:
    branches:
      - main
    paths:
      - "application/**"

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build \
            -t oci-devops-app:${{ github.sha }} \
            application

      - name: Test container
        run: |
          docker run -d \
            --name test-app \
            -p 8080:8080 \
            oci-devops-app:${{ github.sha }}

          sleep 10

          curl --fail http://localhost:8080/health

      - name: Stop test container
        if: always()
        run: docker rm -f test-app || true
```

The next stage should authenticate to the container registry and push the image.

---

# Application Deployment Strategy

Avoid manually SSHing to both servers and changing containers independently.

Use a controlled deployment process.

Example:

```text
Build image
   │
   ▼
Push image
   │
   ▼
Update Server 01
   │
   ▼
Wait for healthy status
   │
   ▼
Update Server 02
   │
   ▼
Wait for healthy status
```

This is a rolling deployment.

---

# Rolling Deployment

1. Remove Server 01 from traffic or wait for connection draining
2. Pull the new image
3. Replace the container
4. Verify `/health`
5. Return Server 01 to service
6. Repeat for Server 02

This reduces downtime.

---

# Deployment Script

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

IMAGE="${1:?Usage: deploy-application.sh IMAGE}"

docker pull "$IMAGE"

docker rm -f oci-devops-app 2>/dev/null || true

docker run -d \
  --name oci-devops-app \
  --restart unless-stopped \
  -p 8080:8080 \
  -e APP_VERSION="${APP_VERSION:-unknown}" \
  -e ENVIRONMENT="${ENVIRONMENT:-development}" \
  -v /data/application:/app/data \
  "$IMAGE"

for attempt in $(seq 1 30); do
    if curl --fail --silent http://127.0.0.1:8080/health >/dev/null; then
        echo "Application is healthy"
        exit 0
    fi

    sleep 5
done

echo "Application health check failed"
docker logs oci-devops-app
exit 1
```

---

# Monitoring Design

Monitor the following.

## Compute

* CPU utilization
* Memory usage
* Network traffic
* Disk activity
* Instance availability
* Load average

## Block Volume

* Read operations
* Write operations
* Throughput
* Latency
* Capacity usage inside Linux

## Load Balancer

* Healthy backend count
* Unhealthy backend count
* HTTP requests
* HTTP 4xx
* HTTP 5xx
* Response time
* Backend connection errors

## Application

* Health endpoint
* Request count
* Error count
* Response latency
* Container restart count

## Backup

* Last successful backup
* Backup object size
* Backup upload failure
* Restore test result

---

# Important Monitoring Difference

OCI can report infrastructure metrics such as CPU usage.

It may not automatically know:

```text
/data is 95% full
```

Filesystem usage must be collected from the operating system or custom monitoring.

Cloud metrics and operating-system metrics are separate.

---

# Recommended Alarms

Create alarms for:

```text
Application backend unhealthy
```

```text
Healthy backend count below 2
```

```text
Compute CPU above 80%
```

```text
Memory usage above 85%
```

```text
Filesystem usage above 85%
```

```text
Load Balancer 5xx errors increasing
```

```text
Backup has not succeeded in 24 hours
```

```text
Compute Instance unavailable
```

---

# Notification Flow

```text
Monitoring Metric
      │
      ▼
Alarm Condition
      │
      ▼
OCI Notifications Topic
      │
      ▼
Email or Approved Alert Channel
```

An alarm without a notification destination may go unnoticed.

---

# Logging Design

Collect logs from:

* Flask
* Gunicorn
* Docker
* Nginx
* cloud-init
* Backup scripts
* systemd
* OCI Load Balancer
* OCI Audit
* GitHub Actions

---

# Useful Instance Logs

Application container:

```bash
docker logs oci-devops-app
```

Follow logs:

```bash
docker logs -f oci-devops-app
```

cloud-init:

```bash
sudo tail -n 100 /var/log/cloud-init-output.log
```

System logs:

```bash
sudo journalctl -xe
```

Backup service:

```bash
sudo journalctl -u oci-devops-backup.service
```

---

# Audit Logging

OCI Audit helps answer:

```text
Who created the Compute Instance?
```

```text
Who changed the NSG?
```

```text
Who deleted the Load Balancer?
```

```text
Which Terraform identity created the VCN?
```

```text
When was the IAM Policy changed?
```

Audit logs are essential for security and troubleshooting.

---

# Security Design

The project should follow these principles:

* No public IP on application servers
* Public access only through Load Balancer
* SSH through Bastion
* NSG-to-NSG rules
* Least-privilege IAM
* Individual user accounts
* MFA
* Private Object Storage bucket
* Instance Principals
* No API keys on application servers
* No secrets committed to Git
* Restricted production deployment
* Protected Terraform state
* Encrypted storage
* Regular access reviews
* Audit logging
* Backup restore tests

---

# Secrets Management

Do not store secrets inside:

* Git repository
* Docker image
* Terraform source
* cloud-init files
* Bash scripts
* Public environment files

Bad:

```python
DB_PASSWORD = "secret123"
```

Better:

```text
OCI Vault
   │
   ▼
Authorized Workload
   │
   ▼
Retrieve Secret at Runtime
```

---

# Terraform State Security

Terraform state may contain:

* OCIDs
* Public IPs
* Private IPs
* Resource metadata
* Sensitive variable values
* Generated secrets
* Provider data

Do not commit:

```text
terraform.tfstate
```

Use:

* Remote state
* Encryption
* Access controls
* Versioning
* Locking
* Backup

---

# Remote State Architecture

```text
GitHub Actions
      │
      ▼
Remote Terraform State
      │
      ├── Encryption
      ├── Access Control
      ├── Versioning
      └── State Locking
```

Without locking, two pipelines may modify the same state simultaneously.

---

# CI/CD Concurrency

Prevent multiple infrastructure applies at the same time.

GitHub Actions example:

```yaml
concurrency:
  group: oci-production-terraform
  cancel-in-progress: false
```

This prevents two runs from modifying the same environment concurrently.

---

# Environment Separation

Use separate state for each environment.

```text
Development State
Staging State
Production State
```

Do not use one state file for every environment.

Possible directory structure:

```text
terraform/
├── modules/
└── environments/
    ├── development/
    ├── staging/
    └── production/
```

---

# Production Architecture Improvement

A stronger architecture may include:

```text
Internet
   │
   ▼
Web Application Firewall
   │
   ▼
HTTPS Load Balancer
   │
   ▼
Private Application Servers
   │
   ▼
Managed Database
```

Add:

* WAF
* TLS certificates
* Managed database
* Redis
* File Storage
* Vault
* Container Registry
* Autoscaling
* Multiple Availability Domains
* DNS
* CDN

---

# High Availability

This project improves availability by using:

* Two application servers
* Separate Fault Domains
* Load Balancer health checks
* Automatic backend removal
* Stateless application design
* Repeatable Terraform deployment

However, this does not make every component highly available.

Potential single points of failure may remain:

* One Availability Domain
* One application data design
* One Region
* One backup Region
* Shared external dependencies

---

# Availability vs Disaster Recovery

High Availability handles local failures.

Example:

```text
App Server 01 fails
App Server 02 continues serving traffic
```

Disaster Recovery handles larger failures.

Example:

```text
Primary Region unavailable
Secondary Region must restore or run the service
```

They are related but not the same.

---

# Disaster Recovery Design

A stronger DR architecture:

```text
Primary Region
├── Terraform Infrastructure
├── Application Servers
├── Load Balancer
├── Block Volumes
└── Object Storage Backups
         │
         ▼
Secondary Region
├── Backup Bucket
├── Terraform Configuration
└── Recovery Environment
```

---

# Recovery Point Objective

Example:

```text
RPO:
24 hours
```

This means the business can tolerate losing up to 24 hours of recent data.

If daily backups run at 02:00 and failure occurs at 20:00, up to 18 hours of data may be lost.

---

# Recovery Time Objective

Example:

```text
RTO:
4 hours
```

This means the service should be restored within four hours.

The recovery process must include:

* Infrastructure deployment
* Volume restoration
* Object download
* Application deployment
* Health checks
* DNS or endpoint update
* Validation

---

# Restore Script

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

BUCKET_NAME="${BUCKET_NAME:-oci-devops-application-backups}"
OBJECT_NAME="${1:?Usage: restore-application.sh OBJECT_NAME}"
RESTORE_DIRECTORY="${RESTORE_DIRECTORY:-/data/restore}"
DOWNLOAD_FILE="/tmp/application-restore.tar.gz"

mkdir -p "$RESTORE_DIRECTORY"

oci os object get \
    --bucket-name "$BUCKET_NAME" \
    --name "$OBJECT_NAME" \
    --file "$DOWNLOAD_FILE" \
    --auth instance_principal

tar -tzf "$DOWNLOAD_FILE"

tar \
    -xzf "$DOWNLOAD_FILE" \
    -C "$RESTORE_DIRECTORY"

echo "Restore completed in ${RESTORE_DIRECTORY}"
```

---

# Backup Validation

A backup process is not complete when upload succeeds.

Validation levels:

```text
Object exists
      │
      ▼
Metadata readable
      │
      ▼
Object downloadable
      │
      ▼
Archive readable
      │
      ▼
Files restorable
      │
      ▼
Application starts with restored data
```

The final level is the most important.

---

# Failure Testing

The project must include deliberate failure tests.

Do not test failures on production systems without proper approval.

---

# Test 1 - Stop the Application on Server 01

On Server 01:

```bash
docker stop oci-devops-app
```

Expected result:

```text
Server 01 becomes unhealthy
Load Balancer stops sending traffic to it
Server 02 continues responding
```

Validate:

```bash
for i in $(seq 1 10); do
  curl -s http://LOAD_BALANCER_IP/info
  echo
done
```

---

# Test 2 - Terminate Server 01

Expected result:

```text
Server 01 unavailable
Server 02 continues serving traffic
Load Balancer reports one healthy backend
```

Terraform may propose recreating the missing instance during the next plan.

---

# Test 3 - Block Application Port

Remove or modify the NSG rule allowing port `8080`.

Expected result:

```text
Load Balancer cannot reach backends
Health checks fail
Application becomes unavailable
```

This proves that security rules are part of application availability.

---

# Test 4 - Delete the NAT Route

Expected result:

* Existing inbound traffic may still work
* Package downloads fail
* Docker image pulls fail
* External API calls fail

The Load Balancer route is separate from outbound server Internet access.

---

# Test 5 - Delete the Service Gateway Route

Expected result:

* General Internet may still work through NAT
* Object Storage backup uploads fail

This proves that NAT Gateway and Service Gateway serve different destinations.

---

# Test 6 - Remove IAM Object Permission

Expected result:

```text
Network path works
Instance Principal authentication may work
Object upload receives authorization failure
```

This proves:

```text
Network access ≠ IAM authorization
```

---

# Test 7 - Fill the Block Volume

Create test data carefully in a lab:

```bash
df -h /data
```

Expected application symptoms may include:

* Upload failures
* Log failures
* Backup failures
* Write errors

Monitoring should alert before the disk becomes completely full.

---

# Test 8 - Break the Health Endpoint

Change `/health` to return HTTP `500`.

Expected result:

```text
Application process running
Load Balancer marks backend unhealthy
Traffic stops reaching that backend
```

A running process is not always a healthy application.

---

# Test 9 - Corrupt a Terraform Variable

Example:

```text
Wrong image OCID
Wrong subnet CIDR
Wrong Compartment OCID
```

Expected result:

* Validation may still pass
* Plan or apply may fail
* Error should be investigated without granting broad IAM permissions

---

# Test 10 - Manual Configuration Drift

Delete an NSG rule manually from the OCI Console.

Run:

```bash
terraform plan
```

Terraform should detect the missing resource and propose restoring it.

---

# Validation Script

Create:

```text
scripts/validate-environment.sh
```

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

APPLICATION_URL="${1:?Usage: validate-environment.sh APPLICATION_URL}"

echo "Testing application root endpoint"
curl \
  --fail \
  --silent \
  --show-error \
  "$APPLICATION_URL" \
  >/dev/null

echo "Testing health endpoint"
curl \
  --fail \
  --silent \
  --show-error \
  "${APPLICATION_URL}/health"

echo
echo "Testing load distribution"

for request in $(seq 1 10); do
    curl \
      --fail \
      --silent \
      "${APPLICATION_URL}/info"

    echo
done

echo "Environment validation completed"
```

---

# Complete Deployment Order

Deploy the project in this order:

1. Define the architecture
2. Create the project repository
3. Create the Compartment
4. Create IAM Groups
5. Create IAM Policies
6. Configure Terraform authentication
7. Create the VCN
8. Create gateways
9. Create Route Tables
10. Create public and private subnets
11. Create NSGs
12. Build the application locally
13. Test the Docker image
14. Configure the container registry
15. Create Compute Instances
16. Attach Block Volumes
17. Prepare Linux filesystems
18. Install Docker
19. Deploy the application containers
20. Create the Load Balancer
21. Create the Backend Set
22. Register backends
23. Configure health checks
24. Create the Object Storage bucket
25. Create the Dynamic Group
26. Create the Instance Principal policy
27. Install the OCI CLI on application servers
28. Configure backup automation
29. Configure Monitoring
30. Configure Logging
31. Configure alarms
32. Configure GitHub Actions
33. Run Terraform plan
34. Review the plan
35. Apply the infrastructure
36. Validate the application
37. Test traffic distribution
38. Test application failure
39. Test instance failure
40. Test backup
41. Test restore
42. Test Terraform drift detection
43. Document the runbook
44. Document the disaster recovery procedure
45. Review security
46. Review cost
47. Clean up the lab safely

---

# Terraform Command Workflow

```bash
cd terraform

terraform fmt -recursive

terraform init

terraform validate

terraform plan -out=tfplan

terraform show tfplan

terraform apply tfplan

terraform output

terraform state list

terraform plan
```

Expected after a clean deployment:

```text
No changes.
Your infrastructure matches the configuration.
```

---

# Application Validation

Get the URL:

```bash
terraform output -raw application_url
```

Test:

```bash
curl "$(terraform output -raw application_url)"
```

Health:

```bash
curl "$(terraform output -raw application_url)/health"
```

Distribution:

```bash
for request in $(seq 1 20); do
  curl -s "$(terraform output -raw application_url)/info"
  echo
done
```

Responses should show both application server hostnames over multiple requests.

---

# Troubleshooting Workflow

Use this order:

```text
User Request
   │
   ▼
DNS or Public IP
   │
   ▼
Load Balancer Listener
   │
   ▼
Backend Set
   │
   ▼
Health Check
   │
   ▼
NSG
   │
   ▼
Private Compute Instance
   │
   ▼
Docker Container
   │
   ▼
Application Process
   │
   ▼
Storage and Dependencies
```

Do not begin troubleshooting randomly.

---

# Website Is Unreachable

Check:

1. Load Balancer lifecycle state
2. Public IP
3. Listener port
4. Load Balancer NSG
5. Backend Set health
6. Backend IP addresses
7. Application NSG
8. Container status
9. Application port
10. Health endpoint

---

# Backends Are Unhealthy

Check:

```bash
docker ps
```

```bash
docker logs oci-devops-app
```

```bash
curl http://localhost:8080/health
```

```bash
sudo ss -tulpn | grep 8080
```

Then verify:

* Correct backend port
* Correct health path
* Correct expected status
* NSG rule from Load Balancer
* Application process

---

# Instance Cannot Pull Image

Check:

```text
Private Route Table
      │
      ▼
0.0.0.0/0 → NAT Gateway
```

Also verify:

* DNS
* Egress rules
* Registry authentication
* Docker daemon
* Image name
* Registry availability

---

# Backup Upload Fails

Check:

```text
Instance matches Dynamic Group
```

```text
IAM Policy allows object operations
```

```text
Service Gateway exists
```

```text
Private Route Table has service route
```

```text
OCI CLI uses --auth instance_principal
```

```text
Bucket exists in the expected Region
```

---

# Terraform Apply Fails

Check:

1. Terraform syntax
2. Variable values
3. Provider authentication
4. IAM authorization
5. Resource availability
6. Shape availability
7. Image Region
8. Quotas
9. CIDR conflicts
10. Terraform state

Never solve every Terraform authorization problem by granting administrator access.

---

# Cost Considerations

Potential billable resources include:

* Load Balancer
* Compute Instances
* Block Volumes
* Object Storage
* Backup storage
* Network traffic
* NAT Gateway traffic
* Monitoring and logging usage
* Public IPv4 resources
* Cross-Region replication

For a learning environment:

* Use small shapes
* Destroy unused resources
* Reduce Load Balancer bandwidth
* Delete unused Block Volumes
* Remove old backups
* Use lifecycle policies
* Monitor costs
* Use tags
* Review current OCI pricing before deployment

---

# Cleanup Preparation

Before destroying:

```text
[ ] Confirm this is the learning environment
[ ] Confirm the correct Terraform state
[ ] Download important logs
[ ] Preserve required backups
[ ] Export required application data
[ ] Review Block Volumes
[ ] Review Object Storage retention
[ ] Review the destroy plan
[ ] Confirm no shared resources are managed
```

---

# Destroy the Environment

```bash
terraform plan -destroy
```

Review every resource.

Then:

```bash
terraform destroy
```

Terraform should delete infrastructure in dependency-aware order.

---

# Cleanup Challenges

Terraform may fail to delete resources when:

* Object Storage bucket is not empty
* Block Volume is still attached
* Load Balancer resources still exist
* Subnet contains active VNICs
* NSG is still attached
* Retention rule prevents object deletion
* External resources depend on the VCN

Do not force-delete without understanding the dependency.

---

# Manual Cleanup Order

When required:

1. Disable application deployments
2. Disable backup timers
3. Preserve required backup objects
4. Empty the lab bucket if safe
5. Delete Load Balancer listeners
6. Delete backends
7. Delete Backend Sets
8. Delete the Load Balancer
9. Stop application services
10. Unmount Block Volumes
11. Detach Block Volumes
12. Terminate Compute Instances
13. Delete Block Volumes
14. Delete NSGs
15. Delete private subnet
16. Delete public subnet
17. Delete Route Tables
18. Delete Service Gateway
19. Delete NAT Gateway
20. Delete Internet Gateway
21. Delete the VCN
22. Delete IAM lab policies
23. Delete Dynamic Groups
24. Delete the Compartment when empty

---

# Documentation Requirements

The project is not complete without documentation.

Create:

```text
docs/architecture.md
```

Include:

* Architecture diagram
* Traffic flow
* Resource relationships
* CIDR plan
* Security boundaries

Create:

```text
docs/runbook.md
```

Include:

* How to deploy
* How to validate
* How to restart services
* How to inspect logs
* How to respond to alerts

Create:

```text
docs/disaster-recovery.md
```

Include:

* RPO
* RTO
* Backup location
* Restore commands
* Region recovery plan
* Validation steps

Create:

```text
docs/security.md
```

Include:

* IAM model
* NSG rules
* Secret handling
* Public exposure
* Encryption
* Access review

---

# Portfolio Screenshots

Capture:

* Terraform plan
* Terraform apply
* OCI VCN
* Subnets
* Route Tables
* NAT Gateway
* Service Gateway
* NSGs
* Compute Instances
* Block Volumes
* Load Balancer
* Healthy backends
* Object Storage bucket
* Backup objects
* Monitoring metrics
* Alarm configuration
* GitHub Actions workflow
* Application page
* Load balancing test
* Failure test
* Restore test

Do not expose:

* Private API keys
* Secret values
* Full sensitive OCIDs when unnecessary
* Personal email addresses
* Private network details that should remain confidential

---

# Interview Explanation

A strong project explanation:

> I built a complete OCI DevOps environment using Terraform. The architecture uses a public Load Balancer and two private application servers distributed across separate Fault Domains. The servers run a containerized Flask application and do not have public IP addresses. They use a NAT Gateway for outbound Internet access and a Service Gateway for private access to Object Storage. Persistent local data is stored on Block Volumes, while scheduled backups are uploaded to a private Object Storage bucket using Instance Principals. GitHub Actions validates and plans infrastructure changes, and production applies require approval. I also configured health checks, monitoring, logging, failure tests, and documented backup and disaster recovery procedures.

---

# What Makes This Project Strong?

This project is stronger than a basic deployment because it demonstrates:

* Architecture design
* Infrastructure as Code
* Network isolation
* Least-privilege IAM
* High availability
* Containerization
* CI/CD
* Persistent storage
* Backup automation
* Observability
* Failure testing
* Disaster recovery
* Security awareness
* Documentation
* Operational thinking

---

# What This Project Does Not Yet Include

The first version does not need to include everything.

Possible future improvements:

* OCI Kubernetes Engine
* OCI Container Registry
* Managed database
* Redis
* Autoscaling
* Web Application Firewall
* HTTPS certificates
* DNS
* Vault secrets
* Multi-Region deployment
* Canary deployment
* Blue-green deployment
* Policy as code
* Cost dashboards
* Automated restore tests

Build the first version correctly before adding every advanced service.

---

# Validation Checklist

```text
[ ] Project Compartment exists
[ ] IAM Groups exist
[ ] IAM Policies use least privilege
[ ] MFA is enabled for privileged users
[ ] VCN exists
[ ] Public subnet exists
[ ] Private application subnet exists
[ ] Internet Gateway exists
[ ] NAT Gateway exists
[ ] Service Gateway exists
[ ] Public Route Table is correct
[ ] Private Route Table is correct
[ ] Load Balancer NSG exists
[ ] Application NSG exists
[ ] Application servers have no public IP
[ ] Application servers are in separate Fault Domains
[ ] Docker is installed
[ ] Application containers are running
[ ] Health endpoints return HTTP 200
[ ] Load Balancer is public
[ ] Backend Set exists
[ ] Both backends are healthy
[ ] Traffic is distributed
[ ] Block Volumes are attached
[ ] Block Volumes are mounted
[ ] Mounts survive reboot
[ ] Object Storage bucket is private
[ ] Versioning is enabled
[ ] Dynamic Group matches application servers
[ ] Instance Principal policy exists
[ ] Backup upload succeeds
[ ] Backup object can be downloaded
[ ] Restore test succeeds
[ ] Monitoring metrics are visible
[ ] Alarms are configured
[ ] Notifications are configured
[ ] GitHub Actions checks Terraform
[ ] Terraform plan is reviewed
[ ] Apply requires approval
[ ] Terraform state is protected
[ ] No secrets are committed to Git
[ ] Failure tests are documented
[ ] Runbook exists
[ ] Disaster recovery document exists
[ ] terraform plan shows no unexpected changes
```

---

# What You Learned

After completing this scenario, you should understand:

* How to design a complete OCI architecture
* How to separate public and private resources
* How Internet Gateway, NAT Gateway, and Service Gateway differ
* How Route Tables control traffic paths
* How NSGs enforce network boundaries
* How to run private application servers
* How a public Load Balancer reaches private backends
* How health checks support high availability
* How Fault Domains reduce infrastructure risk
* How Docker packages an application
* Why application servers should be stateless
* How Block Volumes store persistent local data
* Why Object Storage is suitable for backups
* How Instance Principals avoid human API keys on servers
* How Dynamic Groups and IAM Policies work together
* How Terraform creates related OCI resources
* How Terraform State tracks infrastructure
* Why remote state and locking matter
* How GitHub Actions validates infrastructure
* Why production apply requires approval
* How to monitor Compute, storage, and Load Balancers
* How to create useful alarms
* How to collect logs
* How OCI Audit supports accountability
* How to test application and infrastructure failures
* How to define RPO and RTO
* How to restore application data
* How to detect configuration drift
* How to destroy infrastructure safely
* How to explain a complete DevOps project in an interview

---

# Main Relationship to Remember

```text
GitHub Repository
        │
        ▼
GitHub Actions
        │
        ▼
Terraform
        │
        ▼
OCI IAM
        │
        ▼
OCI Infrastructure
        │
        ├── VCN
        ├── Public Load Balancer
        ├── Private Compute Instances
        ├── Block Volumes
        ├── Object Storage
        ├── Monitoring
        └── Logging
```

---

# Main Traffic Relationship

```text
Internet
   │
   ▼
Public Load Balancer
   │
   ▼
Private Application Servers
   │
   ▼
Dockerized Application
```

---

# Main Backup Relationship

```text
Application Data
      │
      ▼
Block Volume
      │
      ▼
Backup Script
      │
      ▼
Service Gateway
      │
      ▼
Object Storage
```

---

# Main Security Relationship

```text
Human User
    │
    ▼
IAM Group
    │
    ▼
IAM Policy
    │
    ▼
Allowed OCI Resources
```

For workloads:

```text
Compute Instance
      │
      ▼
Dynamic Group
      │
      ▼
Instance Principal Policy
      │
      ▼
Object Storage Permission
```

---

# Final Engineering Principle

Do not judge the project only by asking:

```text
Does the website open?
```

A DevOps engineer must also ask:

```text
Can the infrastructure be reproduced?
```

```text
Are private servers protected?
```

```text
Can one server fail without stopping the service?
```

```text
Are backups restorable?
```

```text
Are changes reviewed?
```

```text
Can we detect failures?
```

```text
Can we recover safely?
```

```text
Can we destroy the environment without deleting the wrong resources?
```

The final goal is not simply:

```text
Deploy an application.
```

The final goal is:

```text
Build a system that is
repeatable,
secure,
available,
observable,
recoverable,
and maintainable.
```
