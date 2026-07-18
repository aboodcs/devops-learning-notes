# Scenario 09 - Deploy OCI Web Infrastructure with Terraform

## Goal

In this scenario, we will deploy a complete web-server infrastructure on Oracle Cloud Infrastructure using Terraform.

Instead of creating every resource manually from the OCI Console, we will describe the infrastructure using Terraform configuration files.

Terraform will create:

* One VCN
* One public subnet
* One Internet Gateway
* One Route Table
* One Network Security Group
* One Compute Instance
* One public IPv4 address
* One Nginx web server
* Useful Terraform outputs

The main goal is to understand how Terraform resources connect to each other and how Infrastructure as Code manages OCI infrastructure.

---

# Final Architecture

```text
Developer Computer
        │
        ▼
Terraform Configuration
        │
        ▼
Terraform OCI Provider
        │
        ▼
Oracle Cloud Infrastructure
        │
        ▼
      VCN
        │
        ├── Internet Gateway
        │
        ├── Route Table
        │
        ├── Public Subnet
        │       │
        │       ├── NSG
        │       └── Compute Instance
        │               │
        │               ├── Public IP
        │               └── Nginx
        │
        └── Security Rules
```

Traffic flow:

```text
Internet User
      │
      ▼
Public IPv4 Address
      │
      ▼
Internet Gateway
      │
      ▼
Public Subnet
      │
      ▼
Network Security Group
      │
      ▼
Compute Instance
      │
      ▼
Nginx
```

---

# What We Want to Build

We will create a Terraform project with this structure:

```text
oci-web-infrastructure/
├── versions.tf
├── provider.tf
├── variables.tf
├── networking.tf
├── compute.tf
├── outputs.tf
├── terraform.tfvars
├── cloud-init.yaml
└── .gitignore
```

Terraform will:

1. Authenticate with OCI
2. Read information about the selected Availability Domain
3. Create networking resources
4. Create security rules
5. Create a Compute Instance
6. Install Nginx automatically
7. Return the instance public IP
8. Return the application URL
9. Track all managed resources in Terraform state

---

# Why Use Terraform?

Without Terraform, infrastructure is created manually.

```text
Engineer
   │
   ▼
OCI Console
   │
   ├── Create VCN
   ├── Create Subnet
   ├── Create Route Table
   ├── Create Gateway
   ├── Create NSG
   └── Create Compute Instance
```

This works for small labs, but it becomes difficult when infrastructure grows.

Manual deployment can cause:

* Inconsistent environments
* Forgotten configuration steps
* Difficult cleanup
* Configuration drift
* Limited review history
* Repeated work
* Human error

Terraform changes the process:

```text
Terraform Code
      │
      ▼
terraform plan
      │
      ▼
Review Changes
      │
      ▼
terraform apply
      │
      ▼
OCI Resources
```

---

# Infrastructure as Code

Infrastructure as Code means defining infrastructure using files instead of creating it only through a graphical interface.

Example:

```hcl
resource "oci_core_vcn" "web_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks     = [var.vcn_cidr]
  display_name    = "${var.project_name}-vcn"
  dns_label       = "webvcn"
}
```

This Terraform resource declares that a VCN should exist.

Terraform compares the declared configuration with the real OCI environment.

---

# Declarative Infrastructure

Terraform is declarative.

You describe the desired result:

```text
One VCN should exist
One public subnet should exist
One Compute Instance should exist
```

Terraform determines which API operations are needed.

You do not normally write:

```text
Step 1: Open the Console
Step 2: Click Networking
Step 3: Click Create VCN
Step 4: Enter the CIDR
```

You define the target state.

---

# Terraform Workflow

The main Terraform workflow is:

```text
Write
  │
  ▼
Format
  │
  ▼
Initialize
  │
  ▼
Validate
  │
  ▼
Plan
  │
  ▼
Apply
  │
  ▼
Verify
  │
  ▼
Destroy
```

Commands:

```bash
terraform fmt
terraform init
terraform validate
terraform plan
terraform apply
terraform output
terraform destroy
```

---

# OCI Services Used

| Service                | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| IAM                    | Authenticate Terraform and authorize resource creation |
| Compartment            | Contain the deployed resources                         |
| VCN                    | Provide the network                                    |
| Public Subnet          | Host the Compute Instance                              |
| Internet Gateway       | Connect the VCN to the Internet                        |
| Route Table            | Send Internet traffic to the Internet Gateway          |
| Network Security Group | Control inbound and outbound traffic                   |
| Compute Instance       | Run the web server                                     |
| Image                  | Provide the operating-system template                  |
| Availability Domain    | Determine instance placement                           |
| Terraform State        | Track managed infrastructure                           |

---

# Terraform Components

The main Terraform components in this scenario are:

```text
Terraform CLI
      │
      ▼
OCI Provider
      │
      ▼
OCI APIs
      │
      ▼
Cloud Resources
```

---

# Terraform CLI

The Terraform CLI reads the `.tf` files.

It performs actions such as:

* Downloading providers
* Validating configuration
* Creating execution plans
* Applying changes
* Reading outputs
* Destroying infrastructure

---

# OCI Provider

The OCI Provider allows Terraform to communicate with Oracle Cloud.

Example:

```hcl
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}
```

The provider uses OCI credentials and configuration to make API requests.

---

# OCI API

Terraform does not click buttons in the OCI Console.

It sends requests to OCI APIs.

Conceptually:

```text
Terraform Resource
      │
      ▼
OCI Provider
      │
      ▼
OCI API Request
      │
      ▼
OCI Resource Created
```

---

# Terraform State

Terraform State records information about managed resources.

Default state file:

```text
terraform.tfstate
```

The state helps Terraform understand:

* Which OCI resources it created
* Resource OCIDs
* Dependencies
* Current known attributes
* Which changes are required

Example relationship:

```text
Terraform Configuration
        │
        ▼
Terraform State
        │
        ▼
Real OCI Resources
```

---

# State Is Important

Without state, Terraform cannot reliably map configuration resources to existing OCI resources.

The state may contain sensitive values.

Do not commit it to Git.

Add:

```gitignore
terraform.tfstate
terraform.tfstate.*
.terraform/
*.tfplan
crash.log
```

For production environments, use a secure remote backend and state locking strategy.

---

# Authentication Options

Terraform needs authentication before it can manage OCI resources.

Common options include:

* API key authentication
* Instance Principal
* Resource Principal
* Security token authentication
* Workload identity where supported

For this beginner lab, we will use API key authentication.

---

# API Key Authentication

API key authentication commonly requires:

```text
Tenancy OCID
User OCID
API Key Fingerprint
Private Key Path
Region
```

These values allow the provider to authenticate as an OCI User.

---

# Security Warning

The private API key is sensitive.

Never commit it to Git.

Bad:

```text
project/
├── main.tf
├── terraform.tfvars
└── oci_api_key.pem
```

Better:

```text
~/.oci/
├── config
└── oci_api_key.pem
```

The Terraform project references the key path.

---

# Terraform Project Structure

Create the project:

```bash
mkdir -p oci-web-infrastructure
cd oci-web-infrastructure
```

Create the files:

```bash
touch \
versions.tf \
provider.tf \
variables.tf \
networking.tf \
compute.tf \
outputs.tf \
terraform.tfvars \
cloud-init.yaml \
.gitignore
```

Final structure:

```text
oci-web-infrastructure/
├── cloud-init.yaml
├── compute.tf
├── networking.tf
├── outputs.tf
├── provider.tf
├── terraform.tfvars
├── variables.tf
├── versions.tf
└── .gitignore
```

---

# Resource Dependency Architecture

```text
Compartment
    │
    ▼
VCN
    │
    ├── Internet Gateway
    │
    ├── Route Table
    │       │
    │       └── Route Rule → Internet Gateway
    │
    ├── Network Security Group
    │
    └── Public Subnet
            │
            ├── Uses Route Table
            └── Hosts Compute Instance
                    │
                    ├── Uses Image
                    ├── Uses Availability Domain
                    ├── Uses Subnet
                    ├── Uses NSG
                    └── Receives Public IP
```

Terraform determines many dependencies by reading resource references.

---

# Resource References

Example:

```hcl
subnet_id = oci_core_subnet.public_subnet.id
```

This tells Terraform:

```text
Compute Instance
      │
      ▼
Depends on Public Subnet
```

Terraform will create the subnet before creating the instance.

You do not need to write `depends_on` for most direct references.

---

# versions.tf

Create:

```bash
nano versions.tf
```

Add:

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

# What `required_version` Means

```hcl
required_version = ">= 1.6.0"
```

This means the project requires Terraform version `1.6.0` or newer.

Check:

```bash
terraform version
```

---

# What `required_providers` Means

```hcl
required_providers {
  oci = {
    source  = "oracle/oci"
    version = "~> 7.0"
  }
}
```

This tells Terraform:

* Provider name: `oci`
* Provider source: `oracle/oci`
* Accepted provider version range: compatible `7.x`

Terraform downloads the provider during:

```bash
terraform init
```

---

# Version Pinning

Provider versions should not be left completely uncontrolled.

Bad:

```hcl
version = ">= 1.0"
```

This may allow future major releases containing breaking changes.

Better:

```hcl
version = "~> 7.0"
```

This allows compatible updates within the selected major version range.

After initialization, Terraform creates:

```text
.terraform.lock.hcl
```

Commit `.terraform.lock.hcl` to Git.

It helps keep provider installation consistent.

---

# provider.tf

Create:

```bash
nano provider.tf
```

Add:

```hcl
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}
```

---

# Provider Authentication Flow

```text
Terraform
    │
    ├── Tenancy OCID
    ├── User OCID
    ├── Fingerprint
    ├── Private API Key
    └── Region
          │
          ▼
      OCI Provider
          │
          ▼
       OCI APIs
```

The User must also belong to a Group with the required IAM Policies.

Credentials prove identity.

IAM Policies grant permission.

---

# Authentication Is Not Authorization

Provider credentials may be valid, but Terraform can still receive:

```text
NotAuthorizedOrNotFound
```

That means authentication may have succeeded, but the User does not have sufficient permission for the requested resource or scope.

Terraform needs both:

```text
Valid Credentials
        +
IAM Permissions
```

---

# Required IAM Concept

For a broad learning Compartment, Terraform may need permissions for:

* VCN resources
* Compute resources
* Images
* Availability Domains
* Block Volumes
* VNIC operations

Conceptual policies may include:

```text
Allow group terraform-operators
to manage virtual-network-family
in compartment development
```

```text
Allow group terraform-operators
to manage instance-family
in compartment development
```

```text
Allow group terraform-operators
to manage volume-family
in compartment development
```

```text
Allow group terraform-operators
to read app-catalog-listing
in tenancy
```

The exact permissions depend on the resources used.

Do not grant `manage all-resources in tenancy` merely to avoid troubleshooting.

---

# variables.tf

Create:

```bash
nano variables.tf
```

Add:

```hcl
variable "tenancy_ocid" {
  description = "OCID of the OCI tenancy"
  type        = string
  sensitive   = true
}

variable "user_ocid" {
  description = "OCID of the OCI user used by Terraform"
  type        = string
  sensitive   = true
}

variable "fingerprint" {
  description = "Fingerprint of the OCI API public key"
  type        = string
  sensitive   = true
}

variable "private_key_path" {
  description = "Local path to the OCI API private key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "OCI region identifier"
  type        = string
}

variable "compartment_ocid" {
  description = "OCID of the compartment where resources will be created"
  type        = string
}

variable "project_name" {
  description = "Prefix used for OCI resource names"
  type        = string
  default     = "terraform-web"
}

variable "vcn_cidr" {
  description = "CIDR block used by the VCN"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block used by the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "allowed_ssh_cidr" {
  description = "Trusted CIDR allowed to connect using SSH"
  type        = string

  validation {
    condition     = var.allowed_ssh_cidr != "0.0.0.0/0"
    error_message = "SSH access must not be open to the entire Internet."
  }
}

variable "instance_shape" {
  description = "OCI Compute shape"
  type        = string
  default     = "VM.Standard.E2.1.Micro"
}

variable "instance_ocpus" {
  description = "Number of OCPUs used by a flexible shape"
  type        = number
  default     = 1
}

variable "instance_memory_gbs" {
  description = "Memory in GB used by a flexible shape"
  type        = number
  default     = 6
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key"
  type        = string
}

variable "image_ocid" {
  description = "OCID of the operating-system image"
  type        = string
}
```

---

# Why Use Variables?

Without variables:

```hcl
region         = "me-riyadh-1"
compartment_id = "ocid1.compartment.oc1..example"
```

Values are hardcoded inside resources.

With variables:

```hcl
region         = var.region
compartment_id = var.compartment_ocid
```

The configuration becomes reusable.

---

# Variable Types

Examples:

```hcl
type = string
```

```hcl
type = number
```

```hcl
type = bool
```

Other Terraform types include:

* List
* Set
* Map
* Object
* Tuple

Strong variable types help detect incorrect input.

---

# Sensitive Variables

Example:

```hcl
sensitive = true
```

This reduces accidental display in Terraform output.

It does not encrypt the value automatically.

Sensitive values may still appear in:

* Terraform State
* Provider logs
* Local files
* Shell history
* External systems

Protect the state and variable files.

---

# Variable Validation

We added:

```hcl
validation {
  condition     = var.allowed_ssh_cidr != "0.0.0.0/0"
  error_message = "SSH access must not be open to the entire Internet."
}
```

This blocks a dangerous default for SSH.

Terraform will reject:

```hcl
allowed_ssh_cidr = "0.0.0.0/0"
```

Use your trusted public IP with `/32`.

Example:

```hcl
allowed_ssh_cidr = "203.0.113.15/32"
```

---

# terraform.tfvars

Create:

```bash
nano terraform.tfvars
```

Example:

```hcl
tenancy_ocid     = "ocid1.tenancy.oc1..replace-me"
user_ocid        = "ocid1.user.oc1..replace-me"
fingerprint      = "aa:bb:cc:dd:replace-me"
private_key_path = "/home/USER/.oci/oci_api_key.pem"

region           = "me-riyadh-1"
compartment_ocid = "ocid1.compartment.oc1..replace-me"

project_name       = "oci-web-lab"
vcn_cidr           = "10.0.0.0/16"
public_subnet_cidr = "10.0.1.0/24"

allowed_ssh_cidr   = "YOUR_PUBLIC_IP/32"
ssh_public_key_path = "/home/USER/.ssh/id_ed25519.pub"

instance_shape     = "VM.Standard.E2.1.Micro"
image_ocid         = "ocid1.image.oc1.me-riyadh-1.replace-me"
```

Replace every placeholder.

---

# Protect terraform.tfvars

The file may contain:

* Tenancy OCID
* User OCID
* Fingerprint
* Local file paths
* Compartment OCID

Add it to `.gitignore`.

```gitignore
terraform.tfvars
*.auto.tfvars
```

A safer team workflow may use:

* Environment variables
* Secret managers
* CI/CD secrets
* Generated variable files
* Short-lived credentials

---

# Environment Variable Input

Terraform variables can also be provided using environment variables.

Pattern:

```text
TF_VAR_variable_name
```

Example:

```bash
export TF_VAR_tenancy_ocid="ocid1.tenancy.oc1..example"
export TF_VAR_user_ocid="ocid1.user.oc1..example"
export TF_VAR_fingerprint="aa:bb:cc:dd"
```

This avoids writing some values directly into `terraform.tfvars`.

However, environment variables may still appear in process environments or shell history.

---

# Data Source for Availability Domains

Add this near the top of `compute.tf`:

```hcl
data "oci_identity_availability_domains" "available" {
  compartment_id = var.tenancy_ocid
}
```

A data source reads existing information.

It does not create a resource.

---

# Resource vs Data Source

Resource:

```hcl
resource "oci_core_vcn" "web_vcn" {
}
```

Creates or manages something.

Data source:

```hcl
data "oci_identity_availability_domains" "available" {
}
```

Reads information that already exists.

---

# Access the First Availability Domain

Use:

```hcl
data.oci_identity_availability_domains.available.availability_domains[0].name
```

This selects the first Availability Domain returned for the Region.

For a production environment, placement should be designed intentionally rather than selected blindly.

---

# networking.tf

Create:

```bash
nano networking.tf
```

Add the networking resources.

---

# Create the VCN

```hcl
resource "oci_core_vcn" "web_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks     = [var.vcn_cidr]
  display_name    = "${var.project_name}-vcn"
  dns_label       = "webvcn"

  freeform_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}
```

---

# VCN Arguments

## `compartment_id`

Defines where the VCN is created.

## `cidr_blocks`

Defines the private IP range.

Example:

```text
10.0.0.0/16
```

## `display_name`

The name shown in OCI.

## `dns_label`

Allows DNS features inside the VCN.

The DNS label must follow OCI naming restrictions.

---

# Create the Internet Gateway

```hcl
resource "oci_core_internet_gateway" "web_igw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_vcn.id
  display_name   = "${var.project_name}-igw"
  enabled        = true

  freeform_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}
```

Relationship:

```text
Internet Gateway
      │
      ▼
Attached to VCN
```

This reference creates the dependency:

```hcl
vcn_id = oci_core_vcn.web_vcn.id
```

---

# Create the Route Table

```hcl
resource "oci_core_route_table" "public_route_table" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_vcn.id
  display_name   = "${var.project_name}-public-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.web_igw.id
  }

  freeform_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}
```

Main route:

```text
0.0.0.0/0 → Internet Gateway
```

---

# Route Rule Meaning

```text
Destination:
0.0.0.0/0
```

means all IPv4 destinations not matched by a more specific route.

```text
Target:
Internet Gateway
```

means send that traffic toward the Internet Gateway.

---

# Create the Network Security Group

```hcl
resource "oci_core_network_security_group" "web_nsg" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_vcn.id
  display_name   = "${var.project_name}-nsg"

  freeform_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}
```

The NSG exists inside the VCN.

It does not control traffic until rules are added and the NSG is attached to a VNIC.

---

# Allow HTTP Ingress

```hcl
resource "oci_core_network_security_group_security_rule" "allow_http" {
  network_security_group_id = oci_core_network_security_group.web_nsg.id
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

  description = "Allow HTTP traffic from the Internet"
}
```

Protocol number:

```text
6 = TCP
```

---

# Allow Restricted SSH

```hcl
resource "oci_core_network_security_group_security_rule" "allow_ssh" {
  network_security_group_id = oci_core_network_security_group.web_nsg.id
  direction                 = "INGRESS"
  protocol                  = "6"

  source      = var.allowed_ssh_cidr
  source_type = "CIDR_BLOCK"

  tcp_options {
    destination_port_range {
      min = 22
      max = 22
    }
  }

  description = "Allow SSH only from the trusted administrator CIDR"
}
```

Do not use:

```text
0.0.0.0/0 → TCP 22
```

for a normal deployment.

---

# Allow Egress

```hcl
resource "oci_core_network_security_group_security_rule" "allow_all_egress" {
  network_security_group_id = oci_core_network_security_group.web_nsg.id
  direction                 = "EGRESS"
  protocol                  = "all"

  destination      = "0.0.0.0/0"
  destination_type = "CIDR_BLOCK"

  description = "Allow outbound traffic"
}
```

This is acceptable for a learning lab.

Production environments should consider more restrictive egress controls.

---

# Create the Public Subnet

```hcl
resource "oci_core_subnet" "public_subnet" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_vcn.id

  cidr_block                 = var.public_subnet_cidr
  display_name               = "${var.project_name}-public-subnet"
  dns_label                  = "publicsubnet"
  route_table_id             = oci_core_route_table.public_route_table.id
  prohibit_public_ip_on_vnic = false

  freeform_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}
```

---

# Why It Is a Public Subnet

A subnet is considered public when:

1. Its Route Table sends Internet traffic to an Internet Gateway
2. Resources are allowed to receive public IP addresses
3. Security rules allow the required inbound traffic

In this resource:

```hcl
route_table_id = oci_core_route_table.public_route_table.id
```

connects the subnet to the public Route Table.

```hcl
prohibit_public_ip_on_vnic = false
```

allows VNICs in the subnet to receive public IP addresses.

---

# Networking Dependency Chain

```text
VCN
  │
  ├── Internet Gateway
  │
  ├── Route Table
  │      └── Route → Internet Gateway
  │
  ├── NSG
  │      ├── HTTP rule
  │      ├── SSH rule
  │      └── Egress rule
  │
  └── Public Subnet
         └── Uses Route Table
```

---

# cloud-init.yaml

Create:

```bash
nano cloud-init.yaml
```

Add:

```yaml
#cloud-config

package_update: true

packages:
  - nginx
  - curl

write_files:
  - path: /var/www/html/index.html
    permissions: "0644"
    owner: root:root
    content: |
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OCI Terraform Web Server</title>
      </head>
      <body>
        <h1>OCI Web Server Deployed with Terraform</h1>
        <p>This infrastructure was created using Infrastructure as Code.</p>
        <p>Managed by Terraform.</p>
      </body>
      </html>

runcmd:
  - systemctl enable nginx
  - systemctl restart nginx
```

---

# What Is cloud-init?

`cloud-init` runs during the first boot of the Compute Instance.

It can:

* Install packages
* Create files
* Create users
* Run commands
* Configure services
* Start applications

Flow:

```text
Terraform Creates Instance
          │
          ▼
Instance Starts
          │
          ▼
cloud-init Runs
          │
          ├── Installs Nginx
          ├── Creates index.html
          └── Starts Nginx
```

---

# Why Use cloud-init?

Without cloud-init:

1. Terraform creates the server
2. You connect through SSH
3. You install Nginx manually
4. You create the web page manually

With cloud-init:

```text
terraform apply
      │
      ▼
Compute Instance
      │
      ▼
Nginx Installed Automatically
```

This improves repeatability.

---

# compute.tf

Create:

```bash
nano compute.tf
```

Add:

```hcl
data "oci_identity_availability_domains" "available" {
  compartment_id = var.tenancy_ocid
}

resource "oci_core_instance" "web_server" {
  compartment_id      = var.compartment_ocid
  availability_domain = data.oci_identity_availability_domains.available.availability_domains[0].name
  display_name        = "${var.project_name}-server"
  shape               = var.instance_shape

  dynamic "shape_config" {
    for_each = can(regex("Flex$", var.instance_shape)) ? [1] : []

    content {
      ocpus         = var.instance_ocpus
      memory_in_gbs = var.instance_memory_gbs
    }
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.public_subnet.id
    assign_public_ip = true
    hostname_label   = "webserver"
    nsg_ids          = [oci_core_network_security_group.web_nsg.id]
  }

  source_details {
    source_type = "image"
    source_id   = var.image_ocid
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
    user_data = base64encode(
      file("${path.module}/cloud-init.yaml")
    )
  }

  preserve_boot_volume = false

  freeform_tags = {
    Project     = var.project_name
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}
```

---

# Compute Resource Relationships

```text
Compute Instance
      │
      ├── Compartment
      ├── Availability Domain
      ├── Shape
      ├── Image
      ├── Public Subnet
      ├── NSG
      ├── Public IP
      ├── SSH Public Key
      └── cloud-init
```

---

# Instance Shape

```hcl
shape = var.instance_shape
```

The shape controls the instance compute capacity.

Depending on the shape, it may define:

* OCPUs
* Memory
* Network capacity
* Maximum VNICs
* Supported architecture

---

# Fixed vs Flexible Shapes

A fixed shape has predefined CPU and memory.

A flexible shape allows CPU and memory customization.

Example flexible shape:

```text
VM.Standard.E4.Flex
```

For a flexible shape, Terraform may require:

```hcl
shape_config {
  ocpus         = 1
  memory_in_gbs = 6
}
```

The configuration uses a dynamic block so `shape_config` is only added for shape names ending with `Flex`.

---

# Why Use a Dynamic Block?

Some OCI shapes accept `shape_config`.

Others may not.

The dynamic block:

```hcl
dynamic "shape_config" {
  for_each = can(regex("Flex$", var.instance_shape)) ? [1] : []
}
```

means:

```text
If the shape name ends with Flex:
Create shape_config

Otherwise:
Do not create shape_config
```

---

# Image OCID

The image defines the operating system.

Examples may include:

* Oracle Linux
* Ubuntu
* Other supported images

Image OCIDs differ by:

* Region
* Operating-system version
* Architecture
* Release

Do not copy an image OCID from another Region and assume it will work.

---

# Source Details

```hcl
source_details {
  source_type = "image"
  source_id   = var.image_ocid
}
```

This tells OCI to create the Boot Volume from the selected image.

---

# VNIC Configuration

```hcl
create_vnic_details {
  subnet_id        = oci_core_subnet.public_subnet.id
  assign_public_ip = true
  hostname_label   = "webserver"
  nsg_ids          = [oci_core_network_security_group.web_nsg.id]
}
```

This creates the primary VNIC.

It:

* Connects the instance to the public subnet
* Assigns a public IP
* Adds the VNIC to the NSG
* Sets a hostname label

---

# SSH Key Metadata

```hcl
ssh_authorized_keys = file(var.ssh_public_key_path)
```

Terraform reads the public key file.

OCI places the key inside the instance user's authorized keys.

Never provide the private SSH key.

Use:

```text
id_ed25519.pub
```

Not:

```text
id_ed25519
```

---

# User Data Metadata

```hcl
user_data = base64encode(
  file("${path.module}/cloud-init.yaml")
)
```

OCI expects the user data to be Base64 encoded.

`${path.module}` refers to the directory containing the Terraform module.

---

# Preserve Boot Volume

```hcl
preserve_boot_volume = false
```

When the instance is terminated, Terraform allows the Boot Volume to be deleted with it.

For important systems, decide this based on data-retention requirements.

Do not store important persistent application data only on the Boot Volume.

---

# outputs.tf

Create:

```bash
nano outputs.tf
```

Add:

```hcl
output "vcn_id" {
  description = "OCID of the created VCN"
  value       = oci_core_vcn.web_vcn.id
}

output "public_subnet_id" {
  description = "OCID of the public subnet"
  value       = oci_core_subnet.public_subnet.id
}

output "instance_id" {
  description = "OCID of the Compute Instance"
  value       = oci_core_instance.web_server.id
}

output "instance_private_ip" {
  description = "Private IPv4 address of the Compute Instance"
  value       = oci_core_instance.web_server.private_ip
}

output "instance_public_ip" {
  description = "Public IPv4 address of the Compute Instance"
  value       = oci_core_instance.web_server.public_ip
}

output "application_url" {
  description = "Public URL of the Nginx web server"
  value       = "http://${oci_core_instance.web_server.public_ip}"
}

output "ssh_command" {
  description = "Example SSH connection command"
  value       = "ssh ubuntu@${oci_core_instance.web_server.public_ip}"
}
```

---

# Why Use Outputs?

Outputs expose useful information after deployment.

Instead of searching through the Console, run:

```bash
terraform output
```

Example:

```text
application_url = "http://203.0.113.20"
instance_public_ip = "203.0.113.20"
```

---

# Output One Value

Run:

```bash
terraform output instance_public_ip
```

Raw output:

```bash
terraform output -raw instance_public_ip
```

Use it in a command:

```bash
curl "http://$(terraform output -raw instance_public_ip)"
```

---

# SSH Username Warning

The SSH username depends on the selected image.

Common examples:

```text
Ubuntu:
ubuntu
```

```text
Oracle Linux:
opc
```

Update the `ssh_command` output according to the image.

---

# .gitignore

Create:

```bash
nano .gitignore
```

Add:

```gitignore
.terraform/
terraform.tfstate
terraform.tfstate.*
terraform.tfvars
*.auto.tfvars
*.tfplan
crash.log
crash.*.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json
*.pem
```

Do not ignore:

```text
.terraform.lock.hcl
```

Commit the lock file.

---

# Format the Configuration

Run:

```bash
terraform fmt -recursive
```

This automatically formats Terraform files.

Check formatting:

```bash
terraform fmt -check -recursive
```

---

# Initialize Terraform

Run:

```bash
terraform init
```

Terraform will:

* Initialize the working directory
* Download the OCI Provider
* Create `.terraform/`
* Create or update `.terraform.lock.hcl`
* Initialize the backend

Expected concept:

```text
Initializing the backend...
Initializing provider plugins...
Terraform has been successfully initialized!
```

---

# Validate the Configuration

Run:

```bash
terraform validate
```

This checks:

* HCL syntax
* Resource arguments
* Provider configuration structure
* Internal references

Expected:

```text
Success! The configuration is valid.
```

Validation does not prove that OCI credentials and permissions are correct.

---

# Create an Execution Plan

Run:

```bash
terraform plan
```

Terraform will compare:

```text
Configuration
      │
      ▼
Current State
      │
      ▼
OCI Infrastructure
```

It will show the proposed changes.

Example:

```text
Plan: 9 to add, 0 to change, 0 to destroy.
```

The exact number may differ.

---

# Save the Plan

For controlled execution:

```bash
terraform plan -out=tfplan
```

Apply the saved plan:

```bash
terraform apply tfplan
```

This ensures Terraform applies the reviewed plan file.

Do not commit `tfplan`.

---

# Read the Plan Carefully

Symbols:

```text
+ create
~ update in place
-/+ destroy and recreate
- destroy
```

A replacement is important:

```text
-/+
```

It may cause downtime or data loss.

Do not apply blindly.

---

# Apply the Infrastructure

Run:

```bash
terraform apply
```

Review the plan.

Type:

```text
yes
```

Terraform creates the resources according to dependency order.

---

# Terraform Creation Order

Terraform may create independent resources in parallel.

Conceptual order:

```text
VCN
 │
 ├── Internet Gateway
 ├── Route Table
 └── NSG
       │
       ▼
Public Subnet
       │
       ▼
Compute Instance
```

Exact execution may be parallel where dependencies allow it.

---

# Watch the Deployment

During apply, Terraform displays operations such as:

```text
oci_core_vcn.web_vcn: Creating...
oci_core_internet_gateway.web_igw: Creating...
oci_core_subnet.public_subnet: Creating...
oci_core_instance.web_server: Creating...
```

At the end:

```text
Apply complete!
```

Outputs are displayed afterward.

---

# Display Outputs

Run:

```bash
terraform output
```

Example:

```text
application_url = "http://PUBLIC_IP"
instance_public_ip = "PUBLIC_IP"
ssh_command = "ssh ubuntu@PUBLIC_IP"
```

---

# Validate the Web Server

Retrieve the URL:

```bash
terraform output -raw application_url
```

Test it:

```bash
curl "$(terraform output -raw application_url)"
```

Open it in a browser.

Expected content:

```text
OCI Web Server Deployed with Terraform
```

---

# cloud-init May Need Time

Terraform may finish creating the instance before cloud-init completes installing Nginx.

If the first request fails:

1. Wait briefly
2. Retry the request
3. Check instance status
4. Connect using SSH
5. Inspect cloud-init logs

Useful commands:

```bash
cloud-init status
```

```bash
cloud-init status --wait
```

```bash
sudo tail -n 100 /var/log/cloud-init-output.log
```

---

# Connect with SSH

For Ubuntu:

```bash
ssh ubuntu@"$(terraform output -raw instance_public_ip)"
```

For Oracle Linux:

```bash
ssh opc@"$(terraform output -raw instance_public_ip)"
```

Use the private key matching the public key supplied to Terraform.

Example:

```bash
ssh \
  -i ~/.ssh/id_ed25519 \
  ubuntu@"$(terraform output -raw instance_public_ip)"
```

---

# Validate Nginx on the Instance

Check:

```bash
sudo systemctl status nginx
```

Verify the port:

```bash
sudo ss -tulpn | grep :80
```

Test locally:

```bash
curl http://localhost
```

Check the page:

```bash
cat /var/www/html/index.html
```

---

# Validate OCI Resources

Check in the OCI Console:

```text
VCN:
Created
```

```text
Internet Gateway:
Enabled
```

```text
Route Table:
0.0.0.0/0 → Internet Gateway
```

```text
Public Subnet:
Created
```

```text
NSG:
Attached to instance VNIC
```

```text
Compute Instance:
Running
```

```text
Public IP:
Assigned
```

---

# Change Infrastructure

Terraform is not only for initial creation.

Suppose you change the project name tag or web page.

Edit:

```text
cloud-init.yaml
```

Important:

> Changing cloud-init user data does not always rerun the initialization script on an existing instance.

Cloud-init usually runs during first boot.

Terraform may update metadata without reinstalling the application.

For repeatable application deployment, use:

* Configuration management
* Image building
* Containers
* Deployment pipelines
* Instance replacement
* OCI Instance Configuration

---

# Add an HTTPS Rule

You can add:

```hcl
resource "oci_core_network_security_group_security_rule" "allow_https" {
  network_security_group_id = oci_core_network_security_group.web_nsg.id
  direction                 = "INGRESS"
  protocol                  = "6"

  source      = "0.0.0.0/0"
  source_type = "CIDR_BLOCK"

  tcp_options {
    destination_port_range {
      min = 443
      max = 443
    }
  }

  description = "Allow HTTPS traffic"
}
```

Run:

```bash
terraform fmt
terraform validate
terraform plan
terraform apply
```

Terraform should create only the new rule.

---

# Idempotency

Run:

```bash
terraform plan
```

after a successful apply without changing the configuration.

Expected:

```text
No changes.
Your infrastructure matches the configuration.
```

This demonstrates idempotent behavior.

Terraform does not recreate resources unnecessarily when the desired state already exists.

---

# Configuration Drift

Configuration drift happens when someone changes a Terraform-managed resource outside Terraform.

Example:

```text
Terraform Configuration:
HTTP port 80 allowed
```

Someone changes the NSG manually in OCI:

```text
OCI Console:
HTTP rule deleted
```

Now the real infrastructure differs from the code.

Run:

```bash
terraform plan
```

Terraform may detect the missing rule and propose recreating it.

---

# Why Manual Changes Are Dangerous

Manual changes can cause:

* Unexpected Terraform plans
* Reverted Console changes
* Conflicting ownership
* Unclear configuration history
* Accidental resource replacement

Use Terraform as the primary source of truth for Terraform-managed resources.

---

# Import Existing Infrastructure

Terraform does not automatically manage resources that were created manually.

To bring an existing resource under Terraform, you may use import.

Conceptually:

```bash
terraform import RESOURCE_ADDRESS RESOURCE_OCID
```

Example pattern:

```bash
terraform import \
  oci_core_vcn.web_vcn \
  ocid1.vcn.oc1.region.example
```

Import adds the resource to state.

You must still create matching Terraform configuration.

Import does not automatically produce a complete, correct configuration.

---

# Terraform State Commands

List resources:

```bash
terraform state list
```

Example:

```text
oci_core_instance.web_server
oci_core_internet_gateway.web_igw
oci_core_network_security_group.web_nsg
oci_core_subnet.public_subnet
oci_core_vcn.web_vcn
```

Show one resource:

```bash
terraform state show oci_core_instance.web_server
```

Do not edit `terraform.tfstate` manually.

---

# Refresh and Planning

Modern Terraform planning normally refreshes resource information automatically.

Run:

```bash
terraform plan
```

to compare the state with real OCI resources.

A refresh-only plan can be used carefully:

```bash
terraform plan -refresh-only
```

Apply refresh-only changes:

```bash
terraform apply -refresh-only
```

Understand the effect before updating state.

---

# Terraform Dependency Graph

Generate a dependency graph:

```bash
terraform graph
```

Save it:

```bash
terraform graph > graph.dot
```

If Graphviz is installed:

```bash
dot -Tpng graph.dot -o terraform-graph.png
```

The graph can help visualize resource relationships.

---

# Explicit `depends_on`

Terraform usually detects dependencies through references.

Example:

```hcl
vcn_id = oci_core_vcn.web_vcn.id
```

Use `depends_on` only when a dependency exists but is not visible through a normal reference.

Example pattern:

```hcl
depends_on = [
  oci_core_network_security_group_security_rule.allow_http
]
```

Do not add `depends_on` everywhere.

Excessive explicit dependencies reduce parallelism and can make the configuration harder to understand.

---

# Local Values

Local values reduce repetition.

Example:

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}
```

Then use:

```hcl
freeform_tags = local.common_tags
```

This avoids repeating the same tags.

---

# Improved locals.tf

You may create:

```bash
touch locals.tf
```

Add:

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = "development"
    ManagedBy   = "Terraform"
  }
}
```

Replace repeated tags with:

```hcl
freeform_tags = local.common_tags
```

---

# Naming Strategy

A consistent naming strategy makes resources easier to identify.

Example:

```text
oci-web-lab-vcn
oci-web-lab-public-subnet
oci-web-lab-igw
oci-web-lab-public-rt
oci-web-lab-nsg
oci-web-lab-server
```

Use:

```hcl
"${var.project_name}-resource-name"
```

---

# Tagging Strategy

Recommended tags:

```text
Project
Environment
Owner
ManagedBy
CostCenter
AutoDestroy
```

Example:

```hcl
freeform_tags = {
  Project     = var.project_name
  Environment = "development"
  Owner       = "Abdulrahman"
  ManagedBy   = "Terraform"
}
```

Tags help with:

* Cost tracking
* Ownership
* Automation
* Resource discovery
* Cleanup
* Governance

---

# Destroy the Infrastructure

When the lab is complete:

```bash
terraform plan -destroy
```

Review the destruction plan.

Then:

```bash
terraform destroy
```

Type:

```text
yes
```

Terraform deletes managed resources in dependency-aware order.

---

# Destroy Order

Conceptually:

```text
Compute Instance
      │
      ▼
Public Subnet
      │
      ▼
NSG and Route Table
      │
      ▼
Internet Gateway
      │
      ▼
VCN
```

Terraform deletes dependent resources before the resources they depend on.

---

# Destroy Warning

`terraform destroy` may permanently delete:

* Compute Instances
* Boot Volumes
* Network resources
* Public IP addresses
* Application data

Before destroying:

```text
[ ] Verify the correct workspace
[ ] Verify the correct Compartment
[ ] Review the plan
[ ] Back up required data
[ ] Confirm no production resources are managed
[ ] Confirm the state file is correct
```

---

# Targeted Operations Warning

Terraform supports:

```bash
terraform apply -target=RESOURCE_ADDRESS
```

and:

```bash
terraform destroy -target=RESOURCE_ADDRESS
```

Targeted operations should not be the normal workflow.

They can leave infrastructure partially updated or create confusing dependency states.

Use them only for recovery or exceptional troubleshooting.

---

# Common Beginner Mistakes

## Committing Secrets to Git

Do not commit:

* API private keys
* `terraform.tfvars`
* State files
* Tokens
* Passwords

Check:

```bash
git status
```

before every commit.

---

## Using the Wrong Region

The provider Region and image OCID must be compatible.

Possible error:

```text
Image not found
```

Verify:

```hcl
region = "me-riyadh-1"
```

and ensure the image belongs to the same Region.

---

## Using an Invalid Shape

The selected shape may:

* Be unavailable
* Require flexible shape settings
* Not be included in the account limits
* Use a different CPU architecture
* Require more quota

Review the shape available in your tenancy and Availability Domain.

---

## Missing IAM Permissions

Terraform may authenticate but fail to create resources.

Check:

* User Group membership
* Policy verbs
* Resource families
* Compartment scope
* Dependent resource permissions

---

## Public Subnet Has No Internet Route

The instance has a public IP but cannot reach the Internet.

Check:

```text
Public Subnet
      │
      ▼
Route Table
      │
      ▼
0.0.0.0/0 → Internet Gateway
```

---

## HTTP Port Is Not Allowed

Nginx is running, but the website is unreachable.

Check:

* NSG attachment
* NSG ingress port 80
* Operating-system firewall
* Nginx service
* Route Table
* Public IP

---

## NSG Exists but Is Not Attached

Creating an NSG does not apply it automatically.

The Compute VNIC must include:

```hcl
nsg_ids = [
  oci_core_network_security_group.web_nsg.id
]
```

---

## SSH Open to Everyone

Avoid:

```hcl
source = "0.0.0.0/0"
```

for port `22`.

Use a trusted `/32` CIDR.

---

## Wrong SSH Username

Ubuntu typically uses:

```text
ubuntu
```

Oracle Linux commonly uses:

```text
opc
```

---

## cloud-init Failed

Check:

```bash
cloud-init status
sudo tail -n 100 /var/log/cloud-init-output.log
```

Possible causes:

* Package repository failure
* YAML syntax error
* Network not ready
* Incorrect command
* Unsupported package name

---

## Terraform State Deleted

If the local state is deleted while resources still exist, Terraform may no longer know it manages them.

Do not simply rerun `terraform apply`.

You may create duplicate infrastructure.

Recover the state backup or import existing resources.

---

## Changing Resource Names

Terraform resource block labels are state addresses.

Changing:

```hcl
resource "oci_core_vcn" "web_vcn"
```

to:

```hcl
resource "oci_core_vcn" "main_vcn"
```

may make Terraform think:

```text
Old resource removed
New resource added
```

Use a moved block when refactoring:

```hcl
moved {
  from = oci_core_vcn.web_vcn
  to   = oci_core_vcn.main_vcn
}
```

---

# Troubleshooting Process

## Step 1 - Format

```bash
terraform fmt -recursive
```

## Step 2 - Validate

```bash
terraform validate
```

## Step 3 - Review Variables

Check:

* OCIDs
* Region
* Image
* Shape
* SSH key path
* CIDR ranges

## Step 4 - Review the Plan

```bash
terraform plan
```

## Step 5 - Check Authentication

Verify:

* Private key exists
* Fingerprint is correct
* User OCID is correct
* Tenancy OCID is correct

## Step 6 - Check Authorization

Review the User's Groups and Policies.

## Step 7 - Check Terraform State

```bash
terraform state list
```

## Step 8 - Check OCI Resource Status

Open the OCI Console and inspect the resource lifecycle state.

## Step 9 - Check Instance Initialization

```bash
cloud-init status
sudo tail -n 100 /var/log/cloud-init-output.log
```

## Step 10 - Check Networking

Verify:

```text
Public IP
Internet Gateway
Route Table
NSG
Nginx
Operating-system firewall
```

---

# Validation Checklist

```text
[ ] Terraform is installed
[ ] OCI Provider is initialized
[ ] API private key is outside the repository
[ ] terraform.tfvars is ignored by Git
[ ] State files are ignored by Git
[ ] .terraform.lock.hcl is committed
[ ] Terraform credentials are valid
[ ] Terraform User has least-privilege IAM access
[ ] Region is correct
[ ] Image OCID belongs to the selected Region
[ ] VCN is created
[ ] Internet Gateway is enabled
[ ] Route Table contains 0.0.0.0/0 → Internet Gateway
[ ] Public subnet uses the correct Route Table
[ ] Public IPs are permitted in the subnet
[ ] NSG exists
[ ] HTTP port 80 is allowed
[ ] SSH port 22 is restricted
[ ] NSG is attached to the instance VNIC
[ ] Compute Instance is running
[ ] Public IP is assigned
[ ] cloud-init completed
[ ] Nginx is running
[ ] Website is reachable
[ ] terraform plan shows no changes after deployment
[ ] terraform output returns the application URL
[ ] terraform destroy was reviewed before cleanup
```

---

# Failure Scenarios

## Credentials Are Invalid

```text
Terraform Configuration:
Valid

OCI Authentication:
Failed

Deployment:
Fails
```

Check the private key, fingerprint, User OCID, and Tenancy OCID.

---

## IAM Permission Is Missing

```text
Authentication:
Successful

Authorization:
Denied

Resource Creation:
Fails
```

Review the exact resource type and Compartment.

---

## Internet Gateway Is Missing

```text
Compute Instance:
Running

Public IP:
Assigned

Internet Route:
Missing

Website:
Unreachable
```

---

## Route Rule Is Missing

```text
Internet Gateway:
Created

Public Subnet:
Created

0.0.0.0/0 Route:
Missing

Internet Connectivity:
Fails
```

---

## NSG Rule Is Missing

```text
Nginx:
Running

Public IP:
Working

TCP Port 80:
Blocked

Website:
Unreachable
```

---

## cloud-init Fails

```text
Infrastructure:
Created

Nginx:
Not Installed

Website:
Unavailable
```

Terraform successfully created infrastructure, but the operating-system configuration failed.

This is an important separation:

```text
Infrastructure Deployment
          ≠
Application Configuration Success
```

---

## State and Real Infrastructure Differ

```text
Terraform State:
Resource exists

OCI:
Resource manually deleted
```

Terraform may propose recreating it.

Or:

```text
OCI Resource:
Exists

Terraform State:
Missing
```

Terraform may try to create another resource.

---

# Security Improvements

A stronger production design should consider:

* Private Compute Instances
* Public Load Balancer
* OCI Bastion
* HTTPS
* OCI Certificates
* Web Application Firewall
* Vault-managed secrets
* Instance Principals
* Remote Terraform state
* State encryption
* State access controls
* CI/CD with short-lived credentials
* Policy-as-code
* Security scanning
* Private subnets
* NAT Gateway
* Service Gateway
* Restricted egress
* Central logging
* Monitoring and alarms

---

# Better Production Architecture

```text
Internet
    │
    ▼
Web Application Firewall
    │
    ▼
Public Load Balancer
    │
    ▼
Private Application Subnet
    │
    ├── Compute Instance 01
    └── Compute Instance 02
            │
            ▼
      Private Database
```

Terraform can manage the complete architecture.

The simple public-instance scenario is only the first Infrastructure as Code lab.

---

# Remote State Concept

Local state:

```text
Developer Laptop
      │
      └── terraform.tfstate
```

Problems:

* State is available to only one machine
* Easy to lose
* Difficult team collaboration
* No centralized locking
* Sensitive data on a laptop

Remote state:

```text
Terraform Clients
       │
       ▼
Central State Storage
       │
       ├── Access Control
       ├── Encryption
       ├── Versioning
       └── Team Collaboration
```

Use a supported secure state backend for production workflows.

---

# State Locking

State locking prevents two Terraform operations from modifying the same state simultaneously.

Without locking:

```text
Engineer 01 → terraform apply
Engineer 02 → terraform apply
                    │
                    ▼
            Conflicting Changes
```

With locking:

```text
Engineer 01 acquires lock
Engineer 02 must wait or stop
```

This reduces state corruption and race conditions.

---

# CI/CD Workflow Concept

```text
Developer Pushes Terraform Code
             │
             ▼
        Pull Request
             │
             ▼
      terraform fmt
             │
             ▼
      terraform validate
             │
             ▼
        Security Scan
             │
             ▼
      terraform plan
             │
             ▼
       Human Approval
             │
             ▼
      terraform apply
```

Production infrastructure should not normally be changed directly from an engineer's laptop without review.

---

# Terraform Security Scanning

Possible tools include:

* TFLint
* Checkov
* Trivy configuration scanning
* Terrascan
* OPA and Conftest

They may detect:

* Open SSH rules
* Public exposure
* Missing encryption
* Unsafe defaults
* Policy violations
* Misconfigurations

Scanning does not replace code review or testing.

---

# Think Like an Infrastructure Engineer

Do not only ask:

```text
Did terraform apply succeed?
```

Also ask:

```text
Is the design secure?
```

```text
Is the state protected?
```

```text
Can another engineer reproduce it?
```

```text
Can the environment be destroyed safely?
```

```text
What happens if a resource is changed manually?
```

```text
Can we recover if the state is lost?
```

```text
Does the plan contain a destructive replacement?
```

---

# Complete Command Sequence

```bash
terraform version

terraform fmt -recursive

terraform init

terraform validate

terraform plan -out=tfplan

terraform apply tfplan

terraform output

curl "$(terraform output -raw application_url)"

terraform state list

terraform plan

terraform plan -destroy

terraform destroy
```

---

# Cleanup Order

Terraform should normally perform cleanup.

Run:

```bash
terraform plan -destroy
```

Review carefully.

Then:

```bash
terraform destroy
```

After destruction:

1. Confirm OCI resources were deleted
2. Review any remaining Boot Volumes
3. Review retained public IPs
4. Review state files
5. Remove temporary plans
6. Keep the Terraform configuration in Git
7. Keep `.terraform.lock.hcl`
8. Never commit secrets

---

# What You Learned

After completing this scenario, you should understand:

* What Infrastructure as Code means
* Why Terraform is declarative
* How the Terraform workflow works
* What the OCI Provider does
* How Terraform authenticates with OCI
* Why authentication and authorization are different
* How variables make configurations reusable
* How data sources read existing OCI information
* How Terraform resources reference each other
* How dependencies determine creation order
* How to create a VCN using Terraform
* How to create an Internet Gateway
* How to create a Route Table
* How to create a public subnet
* How to create an NSG and security rules
* How to create a Compute Instance
* How to assign a public IP
* How to install Nginx with cloud-init
* How Terraform outputs expose useful values
* What Terraform State is
* Why state must be protected
* How to detect configuration drift
* Why manual changes can conflict with Terraform
* How to inspect an execution plan
* Why resource replacement must be reviewed
* How to destroy infrastructure safely
* Why production Terraform requires remote state, locking, review, and automation

---

# Main Relationship to Remember

```text
Terraform Configuration
        │
        ▼
Terraform Provider
        │
        ▼
OCI APIs
        │
        ▼
OCI Resources
        │
        ▼
Terraform State
```

Resource relationship:

```text
VCN
  │
  ├── Internet Gateway
  ├── Route Table
  │      └── 0.0.0.0/0 → Internet Gateway
  ├── Network Security Group
  │      ├── HTTP 80
  │      └── Restricted SSH 22
  └── Public Subnet
          │
          ▼
     Compute Instance
          │
          ├── Public IP
          └── Nginx
```

The safest Terraform workflow is:

```text
Write
  ↓
Format
  ↓
Validate
  ↓
Plan
  ↓
Review
  ↓
Apply
  ↓
Verify
  ↓
Plan Again
```

Never treat:

```bash
terraform apply -auto-approve
```

as the default production workflow.

---

# Next Scenario

Scenario 10:

```text
Full OCI DevOps Project
```

The next scenario will combine the previous lessons into one complete project.

```text
GitHub
   │
   ▼
CI/CD Pipeline
   │
   ▼
Terraform
   │
   ▼
OCI Infrastructure
   │
   ├── VCN
   ├── Public Load Balancer
   ├── Private Compute Instances
   ├── Block Volume
   ├── Object Storage
   ├── IAM
   └── Monitoring
```

It will include:

* Terraform modules
* Development and production environments
* Public Load Balancer
* Private application servers
* Application deployment
* Object Storage backup
* Block Volume persistence
* IAM access
* Monitoring
* Failure testing
* CI/CD
* Security controls
* Cleanup and disaster recovery
