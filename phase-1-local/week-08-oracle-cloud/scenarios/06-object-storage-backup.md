# Scenario 06 - Back Up Compute Data to OCI Object Storage

## Goal

In this scenario, we will back up files from a private Compute Instance to Oracle Cloud Infrastructure Object Storage.

The Compute Instance will create a compressed backup file and upload it to a private Object Storage bucket.

The instance will access Object Storage through a Service Gateway instead of sending the backup through the public Internet.

This scenario teaches how Compute, IAM, networking, and Object Storage work together.

---

# Final Architecture

```text
                         OCI Region
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
          │              Customer VCN             │
          │                                       │
          │    Private Compute Instance           │
          │         No Public IP                  │
          │              │                        │
          │              ▼                        │
          │       Private Route Table             │
          │              │                        │
          │              ▼                        │
          │        Service Gateway                │
          │                                       │
          └───────────────────┬───────────────────┘
                              │
                              ▼
                   Oracle Services Network
                              │
                              ▼
                    OCI Object Storage
                              │
                              ▼
                     Private Backup Bucket
```

The backup flow is:

```text
Application Data
      │
      ▼
Compressed Backup File
      │
      ▼
OCI CLI
      │
      ▼
Service Gateway
      │
      ▼
Object Storage Bucket
```

---

# What We Want to Build

We will create:

* One Compartment
* One VCN
* One private subnet
* One private Compute Instance
* One Service Gateway
* One private Route Table
* One Network Security Group
* One private Object Storage bucket
* One Dynamic Group
* One IAM Policy
* One backup directory
* One backup script
* One scheduled backup job
* One restore test

The Compute Instance will:

1. Collect application files
2. Compress them into an archive
3. Upload the archive to Object Storage
4. Verify that the object exists
5. Download it during a restore test
6. Extract the restored files

---

# Why Use Object Storage for Backups?

A backup stored on the same Compute Instance is not enough.

Consider this design:

```text
Compute Instance
      │
      └── Backup File on Local Disk
```

If the instance or disk fails, both the original data and the backup may be lost.

A better design stores the backup in a separate service:

```text
Compute Instance
      │
      ▼
Object Storage
```

Object Storage is independent from the Compute Instance.

This provides better protection against:

* Instance termination
* Local disk failure
* Accidental file deletion
* Application corruption
* Operating system problems
* Infrastructure replacement

---

# What Is Object Storage?

OCI Object Storage is a service for storing data as objects.

An object normally contains:

* The file data
* An object name
* Metadata

Objects are stored inside buckets.

```text
Object Storage Namespace
        │
        ▼
      Bucket
        │
        ├── backup-2026-07-18.tar.gz
        ├── backup-2026-07-19.tar.gz
        └── backup-2026-07-20.tar.gz
```

Object Storage is suitable for:

* Backups
* Logs
* Images
* Videos
* Application files
* Static website files
* Terraform state
* Data archives
* Machine learning datasets

---

# Object Storage Is Not a Normal Disk

Object Storage is different from Block Volume and File Storage.

You do not normally mount it and use it like a local Linux disk.

Instead, applications interact with it using:

* OCI Console
* OCI CLI
* SDKs
* REST APIs
* Automation tools

Example upload command:

```bash
oci os object put \
  --bucket-name webapp-backups \
  --file backup.tar.gz
```

Example download command:

```bash
oci os object get \
  --bucket-name webapp-backups \
  --name backup.tar.gz \
  --file restored-backup.tar.gz
```

---

# Object Storage vs Block Volume vs File Storage

| Service        | Best Use                                                 |
| -------------- | -------------------------------------------------------- |
| Block Volume   | Disk attached to a Compute Instance                      |
| File Storage   | Shared filesystem used by multiple systems               |
| Object Storage | Backups, archives, media, logs, large unstructured files |

## Block Volume

```text
Compute Instance
      │
      ▼
Virtual Disk
```

The operating system sees it as a disk device.

## File Storage

```text
Server 01 ─┐
           ├── Shared Filesystem
Server 02 ─┘
```

Multiple systems can access shared files.

## Object Storage

```text
Application
     │
     ▼
API Request
     │
     ▼
Bucket
     │
     ▼
Object
```

Files are uploaded and downloaded as objects.

---

# Why Use a Service Gateway?

The private Compute Instance has no public IP address.

It needs a secure path to OCI Object Storage.

A Service Gateway allows resources inside a VCN to access supported Oracle services without sending traffic through the public Internet.

```text
Private Compute Instance
          │
          ▼
     Service Gateway
          │
          ▼
Oracle Services Network
          │
          ▼
     Object Storage
```

This traffic remains on Oracle's network.

---

# Service Gateway vs NAT Gateway

Both gateways can provide outbound connectivity, but they serve different purposes.

| Feature                          | Service Gateway            | NAT Gateway                      |
| -------------------------------- | -------------------------- | -------------------------------- |
| Destination                      | Supported OCI services     | General Internet                 |
| Public IP on instance required   | No                         | No                               |
| Used for Object Storage          | Recommended                | Possible in some designs         |
| Sends traffic to public Internet | No                         | Yes                              |
| Main purpose                     | Private OCI service access | Private outbound Internet access |

Use:

```text
Object Storage → Service Gateway
GitHub → NAT Gateway
Ubuntu repositories → NAT Gateway
External API → NAT Gateway
```

A private subnet may use both gateways.

---

# Combined Gateway Architecture

```text
Private Compute Instance
          │
          ▼
       Route Table
          │
          ├── OCI Services → Service Gateway
          │
          └── 0.0.0.0/0 → NAT Gateway
```

The Route Table chooses the correct gateway based on the destination.

---

# OCI Services Used

| Service                | Purpose                                            |
| ---------------------- | -------------------------------------------------- |
| Compartment            | Organize resources                                 |
| VCN                    | Provide the private cloud network                  |
| Private Subnet         | Host the Compute Instance                          |
| Compute Instance       | Create and upload backups                          |
| Object Storage         | Store backup objects                               |
| Bucket                 | Logical container for backups                      |
| Service Gateway        | Provide private access to Object Storage           |
| Route Table            | Send Oracle service traffic to the Service Gateway |
| Network Security Group | Control network traffic                            |
| Dynamic Group          | Identify the Compute Instance as an IAM principal  |
| IAM Policy             | Permit the instance to use Object Storage          |
| OCI CLI                | Upload, list, download, and delete objects         |

---

# Main Concepts

This scenario combines four major areas:

```text
Compute
   +
Networking
   +
IAM
   +
Object Storage
```

All four must be configured correctly.

A networking route alone is not enough.

IAM permissions alone are not enough.

The instance needs:

```text
Network path
     +
Authentication identity
     +
Authorization policy
     +
Correct CLI command
```

---

# Resource Relationships

```text
Compartment
    │
    ├── VCN
    │     │
    │     ├── Private Subnet
    │     │      │
    │     │      ├── Route Table
    │     │      ├── Instance NSG
    │     │      └── Compute Instance
    │     │
    │     └── Service Gateway
    │
    ├── Object Storage Bucket
    │
    ├── Dynamic Group
    │      │
    │      └── Matches Compute Instance
    │
    └── IAM Policy
           │
           └── Allows Dynamic Group to manage objects
```

---

# Main Dependency Chain

```text
Compute Instance
      │
      ├── Matches Dynamic Group
      │
      ├── Receives permissions from IAM Policy
      │
      ├── Uses Route Table
      │
      ├── Reaches Service Gateway
      │
      └── Uploads to Object Storage Bucket
```

If any part is missing, the upload may fail.

---

# Object Storage Namespace

Every OCI tenancy has an Object Storage namespace.

The namespace is used in Object Storage API and CLI operations.

It is not necessarily the same as:

* Tenancy name
* Compartment name
* Bucket name
* Username
* Region name

You can retrieve it with:

```bash
oci os ns get
```

Example output:

```json
{
  "data": "exampletenancynamespace"
}
```

To store it inside a variable:

```bash
NAMESPACE=$(oci os ns get --query 'data' --raw-output)
```

---

# Bucket

A bucket is a logical container for objects.

Example:

```text
Bucket:
webapp-backups
```

Inside the bucket:

```text
webapp-backups
├── daily/webapp-2026-07-18.tar.gz
├── daily/webapp-2026-07-19.tar.gz
├── weekly/webapp-2026-week-29.tar.gz
└── database/database-2026-07-18.sql.gz
```

---

# Bucket Visibility

The backup bucket should be private.

Recommended setting:

```text
Visibility:
Private
```

Do not make backup buckets public.

A public backup bucket could expose:

* Source code
* Configuration files
* Database dumps
* Customer data
* Application secrets
* Internal logs

---

# Storage Tiers

Object Storage provides storage tiers for different access patterns.

Common concepts include:

## Standard Tier

Used for objects that may be accessed frequently.

Examples:

* Recent backups
* Active files
* Application assets
* Frequently downloaded data

## Infrequent Access Tier

Used for data accessed less frequently but still requiring quick retrieval.

Examples:

* Older backups
* Monthly archives
* Compliance data

## Archive Tier

Used for long-term storage that is rarely accessed.

Examples:

* Annual backups
* Legal archives
* Long-term retention
* Historical datasets

Archived objects may require restoration before they can be downloaded.

---

# Recommended Backup Tier Strategy

Example:

```text
0–30 days:
Standard

31–90 days:
Infrequent Access

Older than 90 days:
Archive
```

The exact strategy depends on:

* Recovery requirements
* Cost
* Access frequency
* Compliance rules
* Restore time requirements

---

# Backup Naming Strategy

Do not use one object name repeatedly unless overwriting is intentional.

Bad:

```text
backup.tar.gz
```

Each upload may replace or conflict with the previous backup.

Better:

```text
webapp-2026-07-18-020000.tar.gz
```

Recommended pattern:

```text
APPLICATION-YYYY-MM-DD-HHMMSS.tar.gz
```

Example:

```text
webapp-2026-07-18-020000.tar.gz
```

For organized storage, use object name prefixes:

```text
daily/2026/07/webapp-2026-07-18-020000.tar.gz
```

Object Storage does not use normal folders in the same way as a filesystem.

The `/` characters are part of the object name and are displayed like folders for organization.

---

# Suggested Scenario Values

```text
Compartment:
oci-learning
```

```text
VCN:
backup-vcn
```

```text
Private Subnet:
backup-private-subnet
```

```text
Service Gateway:
object-storage-service-gateway
```

```text
Route Table:
backup-private-route-table
```

```text
Compute Instance:
backup-client
```

```text
Bucket:
webapp-backups
```

```text
Dynamic Group:
backup-instance-dynamic-group
```

---

# Suggested IP Address Plan

## VCN

```text
10.0.0.0/16
```

## Private Subnet

```text
10.0.2.0/24
```

Example instance address:

```text
10.0.2.10
```

The instance should not have a public IP address.

---

# Service Gateway Configuration

Create a Service Gateway inside the VCN.

The Service Gateway target should provide access to Oracle services in the Region.

Conceptually:

```text
Service Gateway
      │
      ▼
All supported Oracle services in the Region
```

The exact service label shown by the OCI Console may vary.

The important goal is to allow access to regional Object Storage through the Oracle Services Network.

---

# Route Table Configuration

The private subnet needs a Route Table rule that sends Oracle service traffic to the Service Gateway.

Conceptually:

```text
Destination:
Regional Oracle Services Network
```

```text
Target:
Service Gateway
```

Architecture:

```text
Private Subnet
      │
      ▼
Route Table
      │
      ▼
Service Gateway
      │
      ▼
Object Storage
```

Do not configure the Object Storage route as:

```text
0.0.0.0/0 → Service Gateway
```

A Service Gateway is not a general Internet gateway.

---

# Route Table with NAT and Service Gateway

A private server may need both OCI service access and public Internet access.

Example Route Table:

```text
Regional Oracle Services → Service Gateway
0.0.0.0/0                → NAT Gateway
```

Routing works using the most specific matching destination.

Object Storage traffic uses the Service Gateway.

General Internet traffic uses the NAT Gateway.

---

# Network Security Group

Create:

```text
backup-instance-nsg
```

For a simple lab, allow the instance to initiate HTTPS connections.

```text
Destination:
0.0.0.0/0

Protocol:
TCP

Destination Port:
443
```

OCI CLI communicates with Object Storage over HTTPS.

For a more controlled design, restrict egress according to the required network architecture.

---

# Authentication Options

The Compute Instance needs an identity before it can access Object Storage.

There are two common approaches.

## Option 1 - User API Key

The OCI CLI uses:

* User OCID
* Tenancy OCID
* API private key
* Fingerprint
* Region

This is common on a developer workstation.

However, placing a personal user's private API key on a server is not ideal.

## Option 2 - Instance Principal

The Compute Instance authenticates as itself.

This uses:

* Dynamic Group
* IAM Policy
* Instance Principal authentication

This is the recommended approach for this scenario.

---

# Why Use Instance Principals?

Without instance principals, you may need to store a personal API private key on the server.

That creates security risks.

With instance principals:

```text
Compute Instance
      │
      ▼
Dynamic Group
      │
      ▼
IAM Policy
      │
      ▼
Object Storage Permission
```

The instance receives temporary credentials automatically.

No personal API private key needs to be copied to the server.

---

# What Is a Dynamic Group?

A Dynamic Group groups OCI resources instead of human users.

A normal IAM Group contains users.

```text
IAM Group
   │
   ├── User 01
   └── User 02
```

A Dynamic Group contains resources that match a rule.

```text
Dynamic Group
      │
      └── Compute Instance
```

The matching rule may identify resources using:

* Instance OCID
* Compartment OCID
* Resource type
* Tags

---

# Dynamic Group Matching Rule

A simple lab can match one Compute Instance by OCID.

Conceptual rule:

```text
instance.id = 'INSTANCE_OCID'
```

A broader rule can match Compute Instances inside a Compartment.

Conceptual rule:

```text
instance.compartment.id = 'COMPARTMENT_OCID'
```

Be careful with broad rules.

A rule matching an entire Compartment may grant permissions to every matching Compute Instance inside that Compartment.

---

# Recommended Dynamic Group Scope

For a small lab:

```text
Match only the backup Compute Instance
```

For a production backup system:

```text
Match instances with a specific defined tag
```

Example concept:

```text
All instances tagged:
Role = BackupClient
```

Tag-based rules make the design easier to scale without granting permissions to unrelated servers.

---

# IAM Policy

The Dynamic Group needs permission to use the backup bucket.

A broad learning policy may look conceptually like:

```text
Allow dynamic-group backup-instance-dynamic-group
to manage objects
in compartment oci-learning
```

This allows object operations in buckets inside the target Compartment.

A more restricted production policy should limit access to the specific bucket when supported by the policy design.

---

# Manage Objects vs Manage Buckets

These permissions are different.

## Object Permissions

Used for:

* Uploading objects
* Downloading objects
* Listing objects
* Deleting objects

## Bucket Permissions

Used for:

* Creating buckets
* Deleting buckets
* Changing bucket configuration

The backup server usually needs to manage objects.

It does not normally need permission to create or delete buckets.

This follows least privilege.

---

# Least-Privilege Design

The backup instance should ideally be allowed to:

* Upload backup objects
* List backup objects
* Download objects for restore
* Delete old objects only when required

It should not automatically be allowed to:

* Delete the bucket
* Change bucket visibility
* Manage all buckets in the tenancy
* Manage IAM
* Create unrelated cloud resources

---

# OCI CLI Authentication with Instance Principal

When using the OCI CLI, add:

```bash
--auth instance_principal
```

Example:

```bash
oci os ns get \
  --auth instance_principal
```

List buckets:

```bash
oci os bucket list \
  --compartment-id "$COMPARTMENT_OCID" \
  --auth instance_principal
```

Upload an object:

```bash
oci os object put \
  --bucket-name "$BUCKET_NAME" \
  --file "$BACKUP_FILE" \
  --name "$OBJECT_NAME" \
  --auth instance_principal
```

---

# Build Order

Create resources in this order:

1. Create the Compartment
2. Create the VCN
3. Create the Service Gateway
4. Create the private Route Table
5. Add the Oracle services route
6. Create the private subnet
7. Create the instance NSG
8. Create the private Compute Instance
9. Create the private Object Storage bucket
10. Copy the Compute Instance OCID
11. Create the Dynamic Group
12. Add the instance matching rule
13. Create the IAM Policy
14. Install or verify OCI CLI
15. Test Instance Principal authentication
16. Test Object Storage access
17. Create sample application data
18. Create the backup script
19. Run the first backup
20. Verify the uploaded object
21. Download the object
22. Test data restoration
23. Configure scheduled backups
24. Configure retention or lifecycle rules
25. Test failure conditions
26. Clean up resources

---

# OCI Console Navigation

Console labels may change, but the resources are generally available through these areas.

## Create the Bucket

```text
Navigation Menu
→ Storage
→ Object Storage & Archive Storage
→ Buckets
→ Create Bucket
```

Recommended settings:

```text
Name:
webapp-backups
```

```text
Default Storage Tier:
Standard
```

```text
Visibility:
Private
```

```text
Object Versioning:
Optional for this lab
```

---

## Create the Service Gateway

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Service Gateways
→ Create Service Gateway
```

Choose the available Oracle services network option for the Region.

---

## Create the Route Table

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Route Tables
→ Create Route Table
```

Add a route rule:

```text
Destination:
Regional Oracle Services Network
```

```text
Target:
object-storage-service-gateway
```

---

## Create the Dynamic Group

```text
Navigation Menu
→ Identity & Security
→ Domains
→ Dynamic Groups
```

Depending on the current OCI Console layout, Dynamic Groups may appear under the identity domain or IAM area.

Suggested name:

```text
backup-instance-dynamic-group
```

---

## Create the IAM Policy

```text
Navigation Menu
→ Identity & Security
→ Policies
→ Create Policy
```

Create the policy in the correct Compartment or tenancy scope.

---

# Prepare the Compute Instance

Connect to the private Compute Instance through:

* OCI Bastion
* VPN
* Jump server
* Another approved private access method

Verify the instance has no public IP.

```text
Public IPv4 Address:
Not Assigned
```

---

# Verify OCI CLI

Check whether the OCI CLI is installed:

```bash
oci --version
```

If it is unavailable, install it using an approved method for the operating system.

After installation, verify again:

```bash
oci --version
```

---

# Test Instance Principal Authentication

Run:

```bash
oci os ns get \
  --auth instance_principal
```

Expected result:

```json
{
  "data": "your-object-storage-namespace"
}
```

If this succeeds, the Compute Instance can authenticate as an Instance Principal.

---

# Test Bucket Access

Set environment variables:

```bash
export COMPARTMENT_OCID="ocid1.compartment.oc1..example"
export BUCKET_NAME="webapp-backups"
```

List buckets:

```bash
oci os bucket list \
  --compartment-id "$COMPARTMENT_OCID" \
  --auth instance_principal
```

List objects:

```bash
oci os object list \
  --bucket-name "$BUCKET_NAME" \
  --auth instance_principal
```

An empty bucket may return an empty list.

That still confirms the request succeeded.

---

# Create Sample Application Data

Create a directory:

```bash
sudo mkdir -p /opt/webapp/data
```

Create sample files:

```bash
echo "Customer record 001" | sudo tee /opt/webapp/data/customers.txt
echo "Order record 001" | sudo tee /opt/webapp/data/orders.txt
echo "Application configuration" | sudo tee /opt/webapp/data/config.txt
```

Verify:

```bash
find /opt/webapp/data -type f -maxdepth 1 -print
```

---

# Create a Manual Backup

Create a backup directory:

```bash
sudo mkdir -p /var/backups/webapp
```

Set the timestamp:

```bash
TIMESTAMP=$(date -u +"%Y-%m-%d-%H%M%S")
```

Create the archive:

```bash
sudo tar \
  -czf "/var/backups/webapp/webapp-${TIMESTAMP}.tar.gz" \
  -C /opt/webapp \
  data
```

List the backup:

```bash
ls -lh /var/backups/webapp
```

Inspect its contents:

```bash
tar -tzf "/var/backups/webapp/webapp-${TIMESTAMP}.tar.gz"
```

---

# Upload the Backup

Set variables:

```bash
BACKUP_FILE="/var/backups/webapp/webapp-${TIMESTAMP}.tar.gz"
OBJECT_NAME="daily/$(date -u +%Y/%m)/webapp-${TIMESTAMP}.tar.gz"
```

Upload:

```bash
oci os object put \
  --bucket-name "$BUCKET_NAME" \
  --file "$BACKUP_FILE" \
  --name "$OBJECT_NAME" \
  --auth instance_principal
```

Expected result should include object upload information.

---

# Verify the Uploaded Object

List all objects:

```bash
oci os object list \
  --bucket-name "$BUCKET_NAME" \
  --auth instance_principal
```

List only objects under the daily prefix:

```bash
oci os object list \
  --bucket-name "$BUCKET_NAME" \
  --prefix "daily/" \
  --auth instance_principal
```

Retrieve object metadata:

```bash
oci os object head \
  --bucket-name "$BUCKET_NAME" \
  --name "$OBJECT_NAME" \
  --auth instance_principal
```

---

# Create an Automated Backup Script

Create the script:

```bash
sudo nano /usr/local/bin/backup-webapp.sh
```

Use:

```bash
#!/usr/bin/env bash

set -Eeuo pipefail

BUCKET_NAME="webapp-backups"
SOURCE_DIRECTORY="/opt/webapp/data"
LOCAL_BACKUP_DIRECTORY="/var/backups/webapp"
LOG_FILE="/var/log/webapp-backup.log"

TIMESTAMP="$(date -u +"%Y-%m-%d-%H%M%S")"
DATE_PREFIX="$(date -u +"%Y/%m")"

BACKUP_FILENAME="webapp-${TIMESTAMP}.tar.gz"
BACKUP_FILE="${LOCAL_BACKUP_DIRECTORY}/${BACKUP_FILENAME}"
OBJECT_NAME="daily/${DATE_PREFIX}/${BACKUP_FILENAME}"

log() {
    printf '%s %s\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$1" |
        tee -a "$LOG_FILE"
}

cleanup() {
    if [[ -f "$BACKUP_FILE" ]]; then
        rm -f "$BACKUP_FILE"
    fi
}

trap cleanup EXIT

if [[ ! -d "$SOURCE_DIRECTORY" ]]; then
    log "ERROR: Source directory does not exist: ${SOURCE_DIRECTORY}"
    exit 1
fi

mkdir -p "$LOCAL_BACKUP_DIRECTORY"
touch "$LOG_FILE"

log "Starting backup from ${SOURCE_DIRECTORY}"

tar \
    -czf "$BACKUP_FILE" \
    -C "$(dirname "$SOURCE_DIRECTORY")" \
    "$(basename "$SOURCE_DIRECTORY")"

if [[ ! -s "$BACKUP_FILE" ]]; then
    log "ERROR: Backup file was not created or is empty"
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

log "Verified object successfully"
log "Backup completed"
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/backup-webapp.sh
```

Run it:

```bash
sudo /usr/local/bin/backup-webapp.sh
```

View logs:

```bash
sudo tail -n 50 /var/log/webapp-backup.log
```

---

# Why Use `set -Eeuo pipefail`?

The line:

```bash
set -Eeuo pipefail
```

makes the script safer.

## `-e`

Stops the script when a command fails.

## `-u`

Stops the script when an undefined variable is used.

## `-o pipefail`

Detects failures inside command pipelines.

## `-E`

Preserves error traps inside functions and subshells.

Without these options, the script may continue and report success even when part of the backup failed.

---

# Schedule the Backup with Cron

Edit root's crontab:

```bash
sudo crontab -e
```

Run the backup every day at 02:00 UTC:

```cron
0 2 * * * /usr/local/bin/backup-webapp.sh >> /var/log/webapp-backup-cron.log 2>&1
```

Verify:

```bash
sudo crontab -l
```

---

# Cron Timezone Warning

Cron uses the server's configured timezone.

Check it:

```bash
timedatectl
```

If the server uses UTC:

```text
0 2 * * *
```

means 02:00 UTC.

Always document the timezone used by scheduled jobs.

---

# Alternative: systemd Timer

A systemd timer provides better service management and logging than cron.

Create the service:

```bash
sudo nano /etc/systemd/system/webapp-backup.service
```

```ini
[Unit]
Description=Back up web application data to OCI Object Storage
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-webapp.sh
```

Create the timer:

```bash
sudo nano /etc/systemd/system/webapp-backup.timer
```

```ini
[Unit]
Description=Run web application backup daily

[Timer]
OnCalendar=*-*-* 02:00:00 UTC
Persistent=true
Unit=webapp-backup.service

[Install]
WantedBy=timers.target
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable and start the timer:

```bash
sudo systemctl enable --now webapp-backup.timer
```

List timers:

```bash
systemctl list-timers --all
```

Run a manual test:

```bash
sudo systemctl start webapp-backup.service
```

Check logs:

```bash
sudo journalctl -u webapp-backup.service
```

---

# Why Use `Persistent=true`?

Suppose the server is stopped at the scheduled backup time.

Without persistent scheduling:

```text
02:00 → Server is stopped → Backup is missed
```

With:

```ini
Persistent=true
```

systemd can run the missed timer after the server starts again.

---

# Restore Process

A backup is not useful until restoration has been tested.

Create a restore directory:

```bash
sudo mkdir -p /opt/webapp-restore
```

Choose an object:

```bash
oci os object list \
  --bucket-name "$BUCKET_NAME" \
  --prefix "daily/" \
  --auth instance_principal
```

Set the object name:

```bash
RESTORE_OBJECT="daily/2026/07/webapp-2026-07-18-020000.tar.gz"
```

Download it:

```bash
oci os object get \
  --bucket-name "$BUCKET_NAME" \
  --name "$RESTORE_OBJECT" \
  --file /tmp/webapp-restore.tar.gz \
  --auth instance_principal
```

Inspect the archive:

```bash
tar -tzf /tmp/webapp-restore.tar.gz
```

Extract it:

```bash
sudo tar \
  -xzf /tmp/webapp-restore.tar.gz \
  -C /opt/webapp-restore
```

Verify:

```bash
find /opt/webapp-restore -type f -print
```

Compare files:

```bash
diff -r /opt/webapp/data /opt/webapp-restore/data
```

No output from `diff` usually means the contents match.

---

# Backup Verification Levels

There are several levels of backup validation.

## Level 1 - Object Exists

```text
The object appears in the bucket.
```

This is the weakest validation.

## Level 2 - Object Metadata Is Readable

```bash
oci os object head
```

This confirms that the object can be located.

## Level 3 - Object Can Be Downloaded

```text
The backup can be retrieved successfully.
```

## Level 4 - Archive Can Be Opened

```bash
tar -tzf backup.tar.gz
```

## Level 5 - Data Can Be Restored

```text
Files are extracted and validated.
```

The strongest validation is a successful restore test.

---

# Recovery Point Objective

Recovery Point Objective defines how much recent data the organization can afford to lose.

If backups run once every 24 hours:

```text
Maximum potential data loss:
Approximately 24 hours
```

If backups run every hour:

```text
Maximum potential data loss:
Approximately 1 hour
```

Example:

```text
Backup completed at 02:00
Failure happened at 17:00
Potential data loss: 15 hours
```

---

# Recovery Time Objective

Recovery Time Objective defines how quickly the service must be restored after failure.

Restore time depends on:

* Backup size
* Storage tier
* Download speed
* Extraction time
* Database import time
* Application configuration
* Testing and validation

Example:

```text
RTO:
Restore the application within 2 hours
```

---

# RPO vs RTO

| Term | Main Question                     |
| ---- | --------------------------------- |
| RPO  | How much recent data can we lose? |
| RTO  | How quickly must we recover?      |

Example:

```text
RPO: 1 hour
RTO: 2 hours
```

This means:

* Backups or replication should limit data loss to approximately one hour
* The service should be restored within two hours

---

# Object Versioning

Object Versioning keeps older versions when an object is replaced or deleted.

Without versioning:

```text
backup.tar.gz
      │
      ▼
New upload replaces old object
```

With versioning:

```text
backup.tar.gz
├── Version 1
├── Version 2
└── Version 3
```

Versioning helps protect against:

* Accidental overwrite
* Accidental deletion
* Automation mistakes
* Corrupted replacement objects

Versioning may increase storage usage and cost.

---

# Lifecycle Rules

Lifecycle rules automatically move or delete objects based on age.

Example strategy:

```text
After 30 days:
Move to Infrequent Access

After 90 days:
Move to Archive

After 365 days:
Delete
```

Lifecycle rules reduce manual work and help control storage costs.

---

# Retention Rules

Retention rules protect objects from deletion or modification for a defined period.

Example:

```text
Retention period:
30 days
```

During that period, protected objects cannot be deleted normally.

This can protect against:

* Accidental deletion
* Malicious deletion
* Script errors
* Ransomware-style attacks

Retention must be configured carefully because it may prevent cleanup.

---

# Backup Retention Strategy

A common retention pattern is:

```text
Daily backups:
Keep 7 days

Weekly backups:
Keep 4 weeks

Monthly backups:
Keep 12 months

Yearly backups:
Keep according to compliance requirements
```

This is sometimes called a grandfather-father-son rotation strategy.

---

# Encryption

OCI Object Storage encrypts stored objects.

For additional control, organizations may use customer-managed encryption keys.

Conceptually:

```text
Backup File
     │
     ▼
Encryption
     │
     ▼
Object Storage
```

A stronger design may include:

* OCI Vault
* Customer-managed keys
* Key rotation
* Restricted key permissions
* Audit logging

---

# Application-Level Encryption

Highly sensitive backups may also be encrypted before upload.

Example:

```bash
gpg \
  --symmetric \
  --cipher-algo AES256 \
  backup.tar.gz
```

This creates:

```text
backup.tar.gz.gpg
```

The encrypted object is then uploaded.

Be careful:

> Losing the encryption key or passphrase may make the backup permanently unusable.

---

# Database Backup Example

For a MySQL database, create a dump:

```bash
mysqldump \
  -h "$DB_HOST" \
  -u "$DB_USER" \
  -p \
  "$DB_NAME" |
gzip \
  > "/var/backups/webapp/database-${TIMESTAMP}.sql.gz"
```

Upload it:

```bash
oci os object put \
  --bucket-name "$BUCKET_NAME" \
  --file "/var/backups/webapp/database-${TIMESTAMP}.sql.gz" \
  --name "database/$(date -u +%Y/%m)/database-${TIMESTAMP}.sql.gz" \
  --auth instance_principal
```

Do not put database passwords directly inside scripts.

Use a secure credential mechanism.

---

# Restore a MySQL Backup

Download the backup:

```bash
oci os object get \
  --bucket-name "$BUCKET_NAME" \
  --name "$DATABASE_OBJECT_NAME" \
  --file /tmp/database-restore.sql.gz \
  --auth instance_principal
```

Restore:

```bash
gunzip -c /tmp/database-restore.sql.gz |
mysql \
  -h "$DB_HOST" \
  -u "$DB_USER" \
  -p \
  "$DB_NAME"
```

Always test database restoration in a safe environment before using it in production.

---

# Monitoring

Monitor the following backup signals:

* Last successful backup time
* Backup file size
* Upload success or failure
* Object verification result
* Restore test status
* Storage usage
* Lifecycle rule behavior
* Failed authentication attempts

---

# Backup Success Is Not Enough

A script exiting successfully does not always mean the backup is valid.

Examples:

```text
Source directory was empty
Archive contained no useful files
Database dump was incomplete
Wrong folder was backed up
Upload used the wrong bucket
Backup cannot be restored
```

Backup monitoring should validate the result, not only the command exit status.

---

# Useful Log Messages

A backup script should log:

```text
Backup started
Source directory
Backup filename
Backup size
Object name
Upload result
Verification result
Backup completed
Error details
```

Example:

```text
2026-07-18T02:00:00Z Starting backup
2026-07-18T02:00:04Z Created backup: 42 MB
2026-07-18T02:00:10Z Uploaded object successfully
2026-07-18T02:00:11Z Verified object successfully
2026-07-18T02:00:11Z Backup completed
```

---

# Validation Checklist

```text
[ ] Object Storage bucket exists
[ ] Bucket is private
[ ] Compute Instance has no public IP
[ ] Service Gateway exists
[ ] Private subnet uses the correct Route Table
[ ] Route Table sends OCI service traffic to the Service Gateway
[ ] Instance NSG allows required HTTPS egress
[ ] Compute Instance matches the Dynamic Group
[ ] IAM Policy allows required object operations
[ ] Instance Principal authentication works
[ ] OCI CLI can retrieve the Object Storage namespace
[ ] OCI CLI can list the target bucket
[ ] Backup archive is created
[ ] Backup archive is not empty
[ ] Backup object uploads successfully
[ ] Uploaded object can be listed
[ ] Object metadata can be retrieved
[ ] Object can be downloaded
[ ] Downloaded archive can be extracted
[ ] Restored files match the original files
[ ] Scheduled backup job is enabled
[ ] Backup logs are reviewed
[ ] Retention strategy is documented
```

---

# Common Beginner Mistakes

## Creating the Bucket but Forgetting IAM Permissions

The bucket exists, but the instance receives an authorization error.

Possible cause:

```text
Dynamic Group or IAM Policy is missing
```

Networking access does not automatically grant Object Storage permissions.

---

## Creating IAM Policy but Forgetting the Service Gateway

Authentication works conceptually, but the private instance has no network path to Object Storage.

Check:

```text
Private Subnet
   │
   ▼
Route Table
   │
   ▼
Service Gateway
```

---

## Creating a Service Gateway Without a Route Rule

The Service Gateway exists but no traffic is sent to it.

The subnet Route Table must include the Oracle services destination.

---

## Subnet Uses the Wrong Route Table

The correct Route Table exists, but the private subnet is still associated with another Route Table.

Open the subnet details and verify the association.

---

## Using Personal API Keys on the Server

Copying a developer's private API key to a Compute Instance creates unnecessary risk.

Use Instance Principals for workload authentication.

---

## Giving the Instance Administrator Permissions

Avoid policies such as:

```text
Manage all-resources in tenancy
```

The backup server only needs Object Storage permissions.

---

## Making the Bucket Public

Backup buckets should remain private.

Never expose backups using anonymous public access.

---

## Using One Fixed Backup Name

This may overwrite previous backups:

```text
backup.tar.gz
```

Use timestamps:

```text
backup-2026-07-18-020000.tar.gz
```

---

## Never Testing Restore

An untested backup may fail during an emergency.

Always perform restore tests.

---

## Keeping Backups Forever

Unlimited retention may cause unnecessary storage usage and cost.

Use lifecycle and retention policies based on business requirements.

---

## Deleting Local Backup Before Verification

Do not remove the local backup until:

1. Upload succeeds
2. Object metadata is verified
3. Ideally, checksum or restore validation succeeds

The example script deletes the local file only after the script completes or exits, so production implementations may need more advanced retry and retention behavior.

---

# Troubleshooting Process

## Step 1 - Verify Instance Principal Authentication

```bash
oci os ns get \
  --auth instance_principal
```

If this fails, investigate:

* Dynamic Group matching rule
* Instance OCID
* IAM Policy
* Policy Compartment
* Instance Principal support

---

## Step 2 - Verify Bucket Listing

```bash
oci os bucket list \
  --compartment-id "$COMPARTMENT_OCID" \
  --auth instance_principal
```

If authentication works but the bucket is missing, verify:

* Compartment OCID
* Region
* Bucket location
* IAM permissions

---

## Step 3 - Verify the Route Table

Confirm the private subnet has a route to the Service Gateway.

---

## Step 4 - Verify Security Rules

Confirm HTTPS egress is permitted.

```text
TCP 443
```

---

## Step 5 - Verify the Region

The CLI command and bucket must use the correct OCI Region.

Check:

```bash
oci iam region-subscription list \
  --auth instance_principal
```

You can also specify a Region explicitly when needed:

```bash
--region REGION_IDENTIFIER
```

---

## Step 6 - Test a Small Object

Create:

```bash
echo "OCI backup test" > /tmp/backup-test.txt
```

Upload:

```bash
oci os object put \
  --bucket-name "$BUCKET_NAME" \
  --file /tmp/backup-test.txt \
  --name tests/backup-test.txt \
  --auth instance_principal
```

Testing a small file separates Object Storage access problems from backup archive problems.

---

## Step 7 - Check Backup Logs

```bash
sudo tail -n 100 /var/log/webapp-backup.log
```

For systemd:

```bash
sudo journalctl \
  -u webapp-backup.service \
  --since today
```

---

# Failure Scenarios

## Service Gateway Is Deleted

```text
Compute Instance: Running
IAM Permissions: Correct
Service Gateway: Missing
Object Storage Upload: Fails
```

The identity is valid, but the network path is unavailable.

---

## IAM Policy Is Removed

```text
Network Path: Working
Instance Authentication: Working
Authorization: Denied
Upload: Fails
```

The instance can reach Object Storage but cannot perform the requested operation.

---

## Dynamic Group Rule Is Incorrect

```text
Compute Instance does not match Dynamic Group
      │
      ▼
No workload identity permissions
      │
      ▼
Instance Principal request fails
```

---

## Bucket Is Deleted

```text
Backup Script: Running
Target Bucket: Missing
Upload: Fails
```

Monitoring should detect this immediately.

---

## Source Directory Is Empty

```text
Upload: Successful
Backup: Technically valid
Useful Data: Missing
```

This is why backup content validation is important.

---

## Restore Test Fails

Possible causes:

* Corrupted object
* Incomplete upload
* Incorrect archive format
* Missing encryption key
* Wrong permissions
* Application version incompatibility
* Database dump problems

A failed restore test means the backup process is not reliable yet.

---

# Security Improvements

A production architecture should consider:

* Instance Principals
* Least-privilege IAM policies
* Private buckets
* Service Gateway
* OCI Vault
* Customer-managed encryption keys
* Object Versioning
* Retention Rules
* Lifecycle Rules
* Audit logs
* Security Zones
* Backup integrity checks
* Automated restore testing
* Cross-Region replication
* Alerts for failed backups
* Protection against object deletion

---

# Cross-Region Backup Concept

Storing all backups in one Region may not protect against a regional disaster.

A stronger disaster recovery design may copy backups to another Region.

```text
Primary Region
     │
     ▼
Primary Backup Bucket
     │
     ▼
Replication or Copy
     │
     ▼
Secondary Region
     │
     ▼
Disaster Recovery Bucket
```

This improves protection against regional failure.

It may also increase:

* Storage cost
* Replication cost
* Operational complexity
* Compliance requirements

---

# Backup Rule to Remember

A useful general principle is the `3-2-1` backup concept:

```text
3 copies of the data

2 different storage types

1 copy stored separately or offsite
```

In a cloud design, this may mean:

```text
Original application data
      +
Local or volume backup
      +
Object Storage backup in another failure boundary
```

The exact implementation depends on system requirements.

---

# Cleanup Order

Delete resources in this order:

1. Disable the scheduled backup timer or cron job
2. Remove temporary local backup files
3. Delete test objects if no longer required
4. Review whether production backup objects must be retained
5. Delete the Object Storage bucket only when it is empty
6. Remove the IAM Policy created for the lab
7. Delete the Dynamic Group
8. Terminate the private Compute Instance
9. Delete the instance NSG
10. Delete the private subnet
11. Delete the private Route Table
12. Delete the Service Gateway
13. Delete the VCN
14. Delete the Compartment if it is empty

Do not delete backup objects until you confirm they are no longer needed.

---

# What You Learned

After completing this scenario, you should understand:

* What OCI Object Storage is
* How buckets and objects relate to each other
* Why Object Storage is useful for backups
* Why backups should not stay only on the original server
* The difference between Object Storage, Block Volume, and File Storage
* How a Service Gateway provides private access to Oracle services
* The difference between a Service Gateway and a NAT Gateway
* Why networking access and IAM permissions are separate requirements
* What Instance Principals are
* How Dynamic Groups identify OCI resources
* How IAM Policies authorize Compute workloads
* How to create and upload a compressed backup
* How to schedule recurring backups
* Why timestamps and object prefixes matter
* How to download and restore backup data
* Why restore testing is necessary
* What RPO and RTO mean
* How lifecycle, versioning, retention, and storage tiers improve backup management
* Why least-privilege access matters

---

# Main Relationship to Remember

```text
Private Compute Instance
          │
          ├── Identity: Dynamic Group
          │
          ├── Permission: IAM Policy
          │
          └── Network: Service Gateway
                         │
                         ▼
                  Object Storage Bucket
```

The backup succeeds only when all three parts work:

```text
Network Access
      +
Authentication
      +
Authorization
```

The backup process is:

```text
Application Data
      │
      ▼
Create Archive
      │
      ▼
Upload Object
      │
      ▼
Verify Object
      │
      ▼
Test Restore
```

---

# Next Scenario

Scenario 07:

```text
Block Volume for Application Data
```

The next scenario will attach persistent Block Volume storage to a Compute Instance.

```text
Compute Instance
      │
      ▼
Attached Block Volume
      │
      ▼
Application Data
```

We will explain:

* How to attach the volume
* How Linux detects the new disk
* How to create a filesystem
* How to mount it
* How to persist the mount after reboot
* How to detach and reattach the volume
* Why application data should not always remain on the boot volume
