# 14 - Terraform User Data

When Terraform creates a virtual machine, the operating system starts empty.

You usually need to perform some initial setup, such as:

```text
Install packages
Update the operating system
Install Docker
Create users
Configure SSH
Clone a Git repository
Start services
```

Instead of logging in manually every time, you can automate these tasks using **User Data**.

```text
Terraform
      │
      ▼
Create Compute Instance
      │
      ▼
Boot Instance
      │
      ▼
Execute User Data Script
      │
      ▼
Ready-to-use Server
```

## What Is User Data?

**User Data** is a script that runs automatically the first time a virtual machine boots.

It allows you to configure the instance without manually connecting through SSH.

Benefits:

```text
Automation
Consistent server setup
Faster deployments
Less manual work
Repeatable infrastructure
```

---

# Why Use User Data?

Imagine launching ten servers.

Without User Data:

```text
Create server
SSH into server
Install Docker
Install Git
Install updates
Repeat 10 times
```

With User Data:

```text
Create server
Boot server
User Data runs automatically
Server is ready
```

Everything happens automatically.

---

# User Data Workflow

```text
Terraform Apply
       │
       ▼
OCI Creates Compute Instance
       │
       ▼
Instance Boots
       │
       ▼
cloud-init Reads User Data
       │
       ▼
Shell Script Executes
       │
       ▼
Server Configuration Complete
```

---

# User Data in OCI

OCI uses **cloud-init** to execute User Data during the first boot.

Terraform sends the script to OCI, and cloud-init runs it automatically.

---

# Simple User Data Script

Example:

```bash
#!/bin/bash

echo "Hello from User Data"

sudo apt update

sudo apt install -y nginx

sudo systemctl enable nginx

sudo systemctl start nginx
```

This script:

```text
Updates packages
Installs Nginx
Enables the service
Starts the service
```

---

# Saving the Script

Create a directory:

```text
project/
├── terraform/
└── scripts/
    └── bootstrap.sh
```

Example:

```bash
#!/bin/bash

sudo apt update

sudo apt install -y docker.io git curl

sudo systemctl enable docker

sudo systemctl start docker
```

This script becomes your User Data.

---

# Reading the Script in Terraform

Terraform can read the file using the `file()` function.

Example:

```hcl
locals {
  user_data = file("${path.module}/../scripts/bootstrap.sh")
}
```

Explanation:

```text
file()         → Reads file contents
path.module    → Current Terraform directory
bootstrap.sh   → User Data script
```

---

# Passing User Data to OCI

Example:

```hcl
resource "oci_core_instance" "web_server" {

  metadata = {
    user_data = base64encode(local.user_data)
  }

}
```

Terraform:

```text
Reads script
Encodes script
Sends it to OCI
OCI executes it on first boot
```

---

# Why base64encode()?

OCI expects User Data to be Base64 encoded.

Terraform provides:

```hcl
base64encode(local.user_data)
```

Example:

```text
Shell Script
      │
      ▼
Base64
      │
      ▼
OCI Metadata
```

Terraform handles the encoding automatically.

---

# Example Project Structure

```text
terraform-project/
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── scripts/
    └── bootstrap.sh
```

Terraform reads:

```text
scripts/bootstrap.sh
```

and sends it as User Data.

---

# Example OCI Resource

```hcl
locals {
  user_data = file("${path.module}/../scripts/bootstrap.sh")
}

resource "oci_core_instance" "web_server" {

  metadata = {
    user_data = base64encode(local.user_data)
  }

}
```

---

# Example Bootstrap Script

```bash
#!/bin/bash

sudo apt update

sudo apt install -y \
    docker.io \
    git \
    curl

sudo systemctl enable docker

sudo systemctl start docker

docker --version
```

This prepares the server immediately after boot.

---

# Using Variables Inside Scripts

Instead of hardcoding values, you can pass variables from Terraform.

Example:

```hcl
metadata = {
  user_data = base64encode(templatefile(
    "${path.module}/../scripts/bootstrap.sh.tpl",
    {
      project = var.project_name
    }
  ))
}
```

Template file:

```bash
#!/bin/bash

echo "Project: ${project}"
```

Terraform replaces the variable before sending the script.

---

# Typical Tasks Performed by User Data

```text
Install Docker
Install Git
Install Kubernetes tools
Install Terraform
Configure firewall
Create users
Download application code
Run Docker containers
Configure monitoring
```

---

# Checking If User Data Ran Successfully

Connect to the instance:

```bash
ssh ubuntu@PUBLIC_IP
```

View cloud-init logs:

```bash
sudo cat /var/log/cloud-init.log
```

Or:

```bash
sudo cat /var/log/cloud-init-output.log
```

These logs show the commands executed during boot.

---

# Verify Installed Software

Example:

```bash
docker --version
```

```bash
git --version
```

```bash
curl --version
```

If the commands work, the User Data script likely executed successfully.

---

# When Does User Data Run?

User Data runs:

```text
First boot
```

Normally it does **not** run again after every reboot.

```text
Create VM
      │
      ▼
Run User Data
      │
      ▼
Reboot VM
      │
      ▼
User Data does NOT run again
```

---

# Updating User Data

Changing the script does not automatically rerun it on an existing instance.

If you need the updated script:

```text
Recreate the instance
```

Terraform example:

```bash
terraform destroy
terraform apply
```

This creates a new VM that executes the latest User Data.

---

# Advantages

```text
Automatic server setup
No manual SSH configuration
Consistent deployments
Infrastructure as Code
Repeatable provisioning
```

---

# Limitations

```text
Runs only during initial boot
Long scripts increase boot time
Errors may be difficult to debug
Requires cloud-init support
```

---

# Common Beginner Mistakes

### Forgetting Base64 Encoding

Bad:

```hcl
metadata = {
  user_data = local.user_data
}
```

Better:

```hcl
metadata = {
  user_data = base64encode(local.user_data)
}
```

---

### Hardcoding Everything

Bad:

```bash
echo "Development Server"
```

Better:

Use variables with `templatefile()`.

---

### Putting Everything Inside User Data

Bad:

```text
500-line bootstrap script
```

Better:

Keep User Data focused on initial server setup.

---

### Forgetting File Paths

Bad:

```hcl
file("bootstrap.sh")
```

Better:

```hcl
file("${path.module}/../scripts/bootstrap.sh")
```

Using `path.module` makes the configuration more portable.

---

### Ignoring Logs

If something fails, check:

```bash
sudo cat /var/log/cloud-init.log
```

before changing Terraform.

---

# Best Practices

```text
Keep scripts simple
Store scripts in a separate scripts/ directory
Use file() to read scripts
Use base64encode() for OCI metadata
Use templatefile() for dynamic values
Check cloud-init logs for debugging
Keep scripts under version control
```

---

# Useful Commands

Connect to the instance:

```bash
ssh ubuntu@PUBLIC_IP
```

View cloud-init log:

```bash
sudo cat /var/log/cloud-init.log
```

View cloud-init output:

```bash
sudo cat /var/log/cloud-init-output.log
```

Check Docker:

```bash
docker --version
```

Check Git:

```bash
git --version
```

Recreate infrastructure:

```bash
terraform destroy
terraform apply
```

---

# Summary

```text
User Data      → Script executed during first boot
cloud-init     → Runs the User Data
file()         → Reads the script
base64encode() → Encodes the script for OCI
templatefile() → Generates dynamic scripts
bootstrap.sh   → Common User Data script
```

> User Data automates the initial configuration of compute instances, allowing Terraform to provision servers that are ready to use immediately after they are created.

