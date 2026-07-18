# Scenario 07 - Use Block Volume for Persistent Application Data

## Goal

In this scenario, we will attach an OCI Block Volume to a Compute Instance and use it to store persistent application data.

The Compute Instance already has a Boot Volume that contains:

* The operating system
* Installed packages
* System files
* Basic application files

We will add a separate Block Volume for:

* Uploaded files
* Application data
* Database files
* Logs
* Persistent Docker data
* Backup staging files

The main goal is to separate application data from the operating system disk.

---

# Final Architecture

```text
                         OCI Region
                              │
                              ▼
                    Availability Domain
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
         Compute Instance           Block Volume
                 │                         │
                 └──────── Attached ──────┘
                              │
                              ▼
                      Linux Block Device
                              │
                              ▼
                         Filesystem
                              │
                              ▼
                         Mount Point
                              │
                              ▼
                      Application Data
```

Example Linux view:

```text
Compute Instance
├── /dev/sda
│   └── Boot Volume
│       └── /
│
└── /dev/sdb
    └── Block Volume
        └── /data
```

---

# What We Want to Build

We will create:

* One Compartment
* One VCN
* One subnet
* One Compute Instance
* One additional Block Volume
* One volume attachment
* One Linux filesystem
* One mount point
* One persistent `/etc/fstab` entry
* One application data directory
* One backup of the Block Volume
* One detach and reattach test

After configuration, the Block Volume will be mounted at:

```text
/data
```

Application files will be stored under:

```text
/data/application
```

---

# What Is a Block Volume?

A Block Volume is a virtual disk provided by OCI.

It behaves similarly to:

* An SSD installed in a physical server
* An external disk attached to a computer
* An AWS EBS volume
* An Azure Managed Disk

The operating system sees the Block Volume as a block device.

Example:

```text
/dev/sdb
```

The disk must normally be:

1. Attached
2. Detected by the operating system
3. Partitioned when required
4. Formatted with a filesystem
5. Mounted to a directory

---

# Boot Volume vs Block Volume

Every Compute Instance normally has a Boot Volume.

The Boot Volume contains the operating system.

A Block Volume is an additional disk attached to the instance.

```text
Compute Instance
    │
    ├── Boot Volume
    │      └── Operating system
    │
    └── Block Volume
           └── Application data
```

---

# Boot Volume

The Boot Volume usually contains:

* Linux operating system
* Kernel
* System packages
* Configuration files
* User accounts
* Application binaries
* Root filesystem

Typical mount point:

```text
/
```

---

# Block Volume

The additional Block Volume can contain:

* Uploaded files
* Databases
* Docker volumes
* Application logs
* Shared project data
* Backup files
* Large datasets

Possible mount points:

```text
/data
```

```text
/var/lib/mysql
```

```text
/var/lib/docker
```

```text
/opt/application/data
```

---

# Why Separate Application Data?

Suppose the application stores everything on the Boot Volume:

```text
Boot Volume
├── Operating System
├── Application
├── Logs
├── Uploads
└── Database
```

This creates several problems.

## Operating System and Data Share Capacity

Large application files may fill the Boot Volume.

If the root filesystem becomes full:

* Applications may stop
* Logging may fail
* Package installation may fail
* The operating system may become unstable

## Harder Instance Replacement

Replacing or recreating the instance may affect application data.

## Harder Backup Management

Operating system files and application data are mixed together.

## Limited Storage Design

You may want different performance or capacity for data than for the operating system.

A better design is:

```text
Boot Volume
└── Operating System

Block Volume
└── Persistent Application Data
```

---

# Block Storage Concept

A Block Volume provides raw storage blocks.

When first attached, it may not contain:

* A partition
* A filesystem
* A mount point
* Application directories

Linux may detect it as:

```text
/dev/sdb
```

But this does not mean it is ready for storing files.

The preparation process is:

```text
Block Volume
      │
      ▼
Linux Block Device
      │
      ▼
Partition
      │
      ▼
Filesystem
      │
      ▼
Mount Point
      │
      ▼
Files and Directories
```

---

# OCI Services Used

| Service             | Purpose                                   |
| ------------------- | ----------------------------------------- |
| Compartment         | Organize resources                        |
| Compute Instance    | Run the application                       |
| Boot Volume         | Store the operating system                |
| Block Volume        | Store persistent application data         |
| Volume Attachment   | Connect the volume to the instance        |
| Block Volume Backup | Protect the volume data                   |
| IAM                 | Control who can create and manage volumes |
| Monitoring          | Track volume performance and usage        |

---

# Resource Relationships

```text
Compartment
    │
    ├── Compute Instance
    │      │
    │      ├── Boot Volume
    │      └── Volume Attachment
    │               │
    │               ▼
    └────────── Block Volume
```

The Block Volume exists independently from the Compute Instance.

The attachment connects them.

```text
Compute Instance
      │
      ▼
Volume Attachment
      │
      ▼
Block Volume
```

---

# Important Relationship

Creating a Block Volume does not automatically make it available inside Linux.

There are two separate layers.

## OCI Layer

```text
Create Block Volume
      │
      ▼
Attach Block Volume
```

## Linux Layer

```text
Detect Device
      │
      ▼
Create Partition
      │
      ▼
Create Filesystem
      │
      ▼
Mount Filesystem
```

Both layers must be completed.

---

# Block Volume Lifecycle

A Block Volume can continue to exist even when the Compute Instance is terminated.

```text
Compute Instance
      │
      ▼
Terminated

Block Volume
      │
      ▼
Still Exists
```

This depends on the deletion choices made during termination.

The volume can later be attached to another compatible Compute Instance.

```text
Old Compute Instance
      │
      ▼
Detach Volume
      │
      ▼
Attach Volume
      │
      ▼
New Compute Instance
```

This is one of the major benefits of separating persistent data from the instance.

---

# Block Volume Attachment Types

OCI may support different attachment methods depending on the instance shape and configuration.

Common concepts include:

* Paravirtualized attachment
* iSCSI attachment

---

# Paravirtualized Attachment

Paravirtualized attachment is generally simpler for many standard workloads.

The operating system may detect the volume automatically after attachment.

```text
OCI Block Volume
      │
      ▼
Paravirtualized Attachment
      │
      ▼
Linux Device
```

---

# iSCSI Attachment

With iSCSI, the instance connects to the Block Volume through the iSCSI protocol.

The OCI Console may provide commands that must be run inside the instance to connect or disconnect the volume.

Conceptually:

```text
Block Volume
      │
      ▼
iSCSI Target
      │
      ▼
Compute Instance
```

When using iSCSI, save and follow the attach and detach commands provided by OCI.

Do not detach the volume from the Console before safely disconnecting it from the operating system.

---

# Availability Domain Relationship

A Block Volume and its attached Compute Instance generally need to be compatible with the same placement scope.

When creating the volume, verify that its Availability Domain is compatible with the Compute Instance.

Conceptually:

```text
Availability Domain 1
├── Compute Instance
└── Block Volume
```

A volume created in an incompatible placement may not be attachable to the target instance.

---

# Suggested Scenario Values

```text
Compute Instance:
application-server-01
```

```text
Block Volume:
application-data-volume
```

```text
Volume Size:
50 GB
```

```text
Mount Point:
/data
```

```text
Application Directory:
/data/application
```

```text
Filesystem:
XFS or ext4
```

For a beginner lab, `ext4` is a simple choice.

---

# Recommended Build Order

Create and configure resources in this order:

1. Create the Compartment
2. Create the VCN and subnet
3. Create the Compute Instance
4. Record the instance Availability Domain
5. Create the Block Volume
6. Select a compatible Availability Domain
7. Attach the Block Volume
8. Connect to the Compute Instance
9. Detect the new Linux block device
10. Confirm that the disk is empty
11. Create a partition if required
12. Create a filesystem
13. Create the mount point
14. Mount the filesystem
15. Verify available capacity
16. Record the filesystem UUID
17. Add the filesystem to `/etc/fstab`
18. Test the persistent mount
19. Create application directories
20. Write sample application data
21. Reboot the instance
22. Confirm that the volume mounts automatically
23. Create a Block Volume backup
24. Test safe detach and reattach
25. Clean up the resources

---

# OCI Console Navigation

Console labels may change, but the resources are generally available in the following areas.

## Create the Block Volume

```text
Navigation Menu
→ Storage
→ Block Storage
→ Block Volumes
→ Create Block Volume
```

Configure:

```text
Name:
application-data-volume
```

```text
Compartment:
Your learning compartment
```

```text
Availability Domain:
Same compatible domain as the Compute Instance
```

```text
Size:
50 GB
```

---

## Find the Compute Instance Availability Domain

```text
Navigation Menu
→ Compute
→ Instances
→ Select the instance
```

Check:

```text
Availability Domain
```

Use this information when creating the Block Volume.

---

## Attach the Block Volume

From the Compute Instance:

```text
Compute
→ Instances
→ Select the instance
→ Attached Block Volumes
→ Attach Block Volume
```

Or from the volume:

```text
Storage
→ Block Storage
→ Block Volumes
→ Select the volume
→ Attached Instances
→ Attach to Instance
```

Select:

* The target Compute Instance
* The attachment type
* Read/write access
* Device path preferences when available

---

# Connect to the Compute Instance

Connect using the appropriate access method:

* Public SSH for a controlled learning instance
* OCI Bastion
* VPN
* Jump server
* Instance Console Connection

Example:

```bash
ssh ubuntu@PUBLIC_IP
```

For Oracle Linux:

```bash
ssh opc@PUBLIC_IP
```

---

# Detect the New Disk

Before attachment, run:

```bash
lsblk
```

Example:

```text
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0   47G  0 disk
├─sda1    8:1    0 46.9G  0 part /
└─sda15   8:15   0  100M  0 part /boot/efi
```

After attaching the volume, run:

```bash
lsblk
```

Example:

```text
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda       8:0    0   47G  0 disk
├─sda1    8:1    0 46.9G  0 part /
└─sda15   8:15   0  100M  0 part /boot/efi
sdb       8:16   0   50G  0 disk
```

The new disk in this example is:

```text
/dev/sdb
```

The exact device name may be different.

Do not assume the new volume is always `/dev/sdb`.

---

# Identify the Correct Device Safely

Use:

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

Also use:

```bash
sudo fdisk -l
```

You can compare:

* Disk size
* Existing partitions
* Filesystem
* Mount point

Never format a disk until you are certain it is the new Block Volume.

Formatting the wrong disk may destroy the operating system or existing data.

---

# Check Whether the Volume Already Has Data

Before creating a filesystem, inspect it:

```bash
sudo blkid /dev/sdb
```

Check for existing filesystem signatures:

```bash
sudo wipefs /dev/sdb
```

The command may display existing signatures without deleting them.

Also inspect:

```bash
sudo file -s /dev/sdb
```

Possible new empty disk result:

```text
/dev/sdb: data
```

Possible existing filesystem:

```text
/dev/sdb: Linux rev 1.0 ext4 filesystem data
```

If the volume already contains a filesystem or data, do not format it.

Mount it carefully or investigate its history first.

---

# Partitioned vs Unpartitioned Volume

There are two common approaches.

## Option 1 - Create a Partition

```text
/dev/sdb
└── /dev/sdb1
```

The filesystem is created on:

```text
/dev/sdb1
```

## Option 2 - Use the Whole Disk

```text
/dev/sdb
```

The filesystem is created directly on the device.

Both approaches can work.

For this learning scenario, we will create one partition.

---

# Create a Partition

Open `fdisk`:

```bash
sudo fdisk /dev/sdb
```

Inside `fdisk`, use:

```text
n
```

Create a new partition.

Accept the default values to use the full disk.

Then use:

```text
w
```

Write the changes.

Verify:

```bash
lsblk
```

Expected result:

```text
sdb      8:16   0  50G  0 disk
└─sdb1   8:17   0  50G  0 part
```

The new partition is:

```text
/dev/sdb1
```

---

# Create an ext4 Filesystem

Create the filesystem:

```bash
sudo mkfs.ext4 /dev/sdb1
```

Example output may show:

* Filesystem UUID
* Block count
* Inode count
* Journal creation

Verify:

```bash
sudo blkid /dev/sdb1
```

Example:

```text
/dev/sdb1: UUID="7b6a3b72-example" TYPE="ext4"
```

---

# Alternative: Create an XFS Filesystem

Install XFS tools when required:

```bash
sudo apt update
sudo apt install xfsprogs -y
```

For Oracle Linux:

```bash
sudo dnf install xfsprogs -y
```

Create XFS:

```bash
sudo mkfs.xfs /dev/sdb1
```

Use either `ext4` or `XFS`.

Do not create both on the same partition.

---

# Create the Mount Point

Create:

```bash
sudo mkdir -p /data
```

A mount point is a normal directory that becomes the entry point for the filesystem.

Before mounting:

```text
/data
└── Normal directory on the Boot Volume
```

After mounting:

```text
/data
└── Files stored on the Block Volume
```

---

# Mount the Filesystem

Mount the partition:

```bash
sudo mount /dev/sdb1 /data
```

Verify:

```bash
findmnt /data
```

Or:

```bash
df -hT /data
```

Example:

```text
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/sdb1      ext4   49G   24K   47G   1% /data
```

---

# Verify with `lsblk`

Run:

```bash
lsblk -f
```

Expected structure:

```text
NAME   FSTYPE FSVER LABEL UUID                                 MOUNTPOINTS
sda
└─sda1 ext4   1.0         BOOT-VOLUME-UUID                     /
sdb
└─sdb1 ext4   1.0         BLOCK-VOLUME-UUID                    /data
```

---

# Create the Application Directory

Create:

```bash
sudo mkdir -p /data/application
```

Set ownership:

```bash
sudo chown -R ubuntu:ubuntu /data/application
```

For Oracle Linux:

```bash
sudo chown -R opc:opc /data/application
```

Create sample data:

```bash
echo "Persistent application data" > /data/application/data.txt
```

Verify:

```bash
cat /data/application/data.txt
```

---

# Why Ownership Matters

The filesystem may initially be owned by `root`.

Example:

```text
drwxr-xr-x root root /data
```

A normal application user may not be able to write files.

Possible error:

```text
Permission denied
```

Set permissions according to the application account.

Example:

```bash
sudo chown -R appuser:appuser /data/application
```

Avoid using:

```bash
sudo chmod -R 777 /data
```

This gives excessive permissions to every user.

---

# Temporary Mount Problem

The command:

```bash
sudo mount /dev/sdb1 /data
```

mounts the volume only for the current running system.

After reboot, the volume may not mount automatically.

To make the mount persistent, configure:

```text
/etc/fstab
```

---

# Why Use UUID Instead of Device Name?

Linux device names may change.

Today:

```text
/dev/sdb1
```

After a restart or new disk attachment:

```text
/dev/sdc1
```

The filesystem UUID is designed to identify the filesystem consistently.

Example:

```text
UUID=7b6a3b72-example
```

Use the UUID inside `/etc/fstab`.

---

# Get the Filesystem UUID

Run:

```bash
sudo blkid /dev/sdb1
```

Example:

```text
/dev/sdb1: UUID="7b6a3b72-4ad7-4b86-a08b-example" TYPE="ext4"
```

Or:

```bash
lsblk -f
```

Copy the correct UUID.

---

# Configure Persistent Mount

Back up the existing file:

```bash
sudo cp /etc/fstab /etc/fstab.backup
```

Edit:

```bash
sudo nano /etc/fstab
```

Add:

```fstab
UUID=7b6a3b72-4ad7-4b86-a08b-example /data ext4 defaults,nofail 0 2
```

Replace the example UUID with the actual filesystem UUID.

---

# Understand the `/etc/fstab` Entry

```text
UUID=... /data ext4 defaults,nofail 0 2
```

## Field 1 - Device

```text
UUID=7b6a3b72-example
```

Identifies the filesystem.

## Field 2 - Mount Point

```text
/data
```

Defines where the filesystem appears.

## Field 3 - Filesystem Type

```text
ext4
```

Must match the actual filesystem.

## Field 4 - Mount Options

```text
defaults,nofail
```

`defaults` applies standard mount options.

`nofail` allows the system to continue booting if the volume is temporarily unavailable.

## Field 5 - Dump

```text
0
```

Disables the legacy dump backup flag.

## Field 6 - Filesystem Check Order

```text
2
```

Allows filesystem checking after the root filesystem.

---

# Test `/etc/fstab` Before Reboot

Never reboot immediately after editing `/etc/fstab`.

First run:

```bash
sudo mount -a
```

If there is no output, the configuration may be valid.

Check:

```bash
findmnt /data
```

You can test more carefully:

```bash
sudo umount /data
sudo mount -a
findmnt /data
```

Verify the sample file:

```bash
cat /data/application/data.txt
```

---

# Reboot Test

Reboot:

```bash
sudo reboot
```

Reconnect after the server starts.

Verify:

```bash
findmnt /data
```

Check capacity:

```bash
df -hT /data
```

Verify data:

```bash
cat /data/application/data.txt
```

If the data exists and `/data` is mounted, the persistent mount works.

---

# Important Mount Point Warning

Suppose `/data` contains files before mounting the Block Volume:

```text
/data
└── old-file.txt
```

After mounting:

```text
/data
└── Block Volume contents
```

The original file is hidden while the filesystem is mounted.

It is not necessarily deleted.

It becomes visible again after unmounting.

This can confuse beginners.

Always verify whether a mount point contains existing data before mounting a new filesystem.

---

# Store Application Uploads

Example application directory:

```text
/data/application/uploads
```

Create it:

```bash
sudo mkdir -p /data/application/uploads
```

Set ownership:

```bash
sudo chown -R appuser:appuser /data/application/uploads
```

Application configuration:

```bash
UPLOAD_DIRECTORY=/data/application/uploads
```

Now uploaded files remain on the Block Volume.

---

# Use with Docker

Docker named volumes are normally stored under:

```text
/var/lib/docker/volumes
```

For a simple application, you can bind-mount a Block Volume directory into a container.

Create:

```bash
sudo mkdir -p /data/docker/uploads
```

Example:

```bash
docker run -d \
  --name uploader \
  -p 8080:8080 \
  -v /data/docker/uploads:/app/uploads \
  uploader-image
```

Container path:

```text
/app/uploads
```

Host Block Volume path:

```text
/data/docker/uploads
```

If the container is deleted, the uploaded files remain on the Block Volume.

---

# Docker Compose Example

```yaml
services:
  uploader:
    image: uploader-image
    ports:
      - "8080:8080"
    volumes:
      - /data/docker/uploads:/app/uploads
```

This is a bind mount.

The data is stored outside the container lifecycle.

---

# Use with a Database

A self-managed database may store data on the Block Volume.

Example MySQL path:

```text
/data/mysql
```

Example PostgreSQL path:

```text
/data/postgresql
```

Before changing a database data directory:

1. Stop the database safely
2. Back up the existing database
3. Copy files while preserving permissions
4. Update database configuration
5. Update ownership
6. Validate security controls
7. Start the database
8. Test application connectivity

Never move active database files while the database is writing to them.

---

# Example Database Relationship

```text
Compute Instance
      │
      ▼
Database Process
      │
      ▼
/data/mysql
      │
      ▼
Block Volume
```

The database process runs on the Compute Instance.

The database files remain on the attached Block Volume.

---

# Block Volume Performance

Block Volume performance affects:

* Read latency
* Write latency
* IOPS
* Throughput
* Database performance
* Application response time

Different workloads have different needs.

## General Files

Moderate storage performance may be enough.

## Databases

May require higher IOPS and lower latency.

## Large Sequential Backups

May require high throughput.

## Log Workloads

May involve frequent writes.

Choose volume size and performance according to workload requirements.

---

# Capacity Monitoring

Check filesystem capacity:

```bash
df -h /data
```

Check inode usage:

```bash
df -i /data
```

Find large directories:

```bash
sudo du -h --max-depth=1 /data | sort -h
```

Find large files:

```bash
sudo find /data -type f -printf '%s %p\n' |
sort -nr |
head -20
```

A filesystem can fail because of:

* No free disk space
* No free inodes
* Read-only filesystem state
* Permission problems
* Mount failure

---

# Expanding a Block Volume

A Block Volume can often be increased in size.

However, increasing the OCI volume size does not automatically expand:

* The partition
* The filesystem

There are multiple layers:

```text
OCI Block Volume Size
      │
      ▼
Linux Disk Size
      │
      ▼
Partition Size
      │
      ▼
Filesystem Size
```

All necessary layers must be expanded.

---

# Example Expansion Flow

Suppose the volume changes from:

```text
50 GB
```

to:

```text
100 GB
```

After resizing in OCI, verify:

```bash
lsblk
```

You may need to rescan the device or restart, depending on the environment.

If using a partition, expand it with an appropriate tool.

Example concept:

```bash
sudo growpart /dev/sdb 1
```

For ext4:

```bash
sudo resize2fs /dev/sdb1
```

For XFS:

```bash
sudo xfs_growfs /data
```

Always confirm the actual device and filesystem type before running expansion commands.

Back up important data first.

---

# Block Volume Backup

A Block Volume backup creates a point-in-time copy of the volume data.

```text
Block Volume
      │
      ▼
Block Volume Backup
```

Backups can help with:

* Accidental deletion
* Data corruption
* Volume replacement
* Environment cloning
* Disaster recovery planning

---

# Crash-Consistent vs Application-Consistent Backup

## Crash-Consistent Backup

Similar to the state of a disk after an unexpected power failure.

The filesystem may recover, but active application transactions may be incomplete.

## Application-Consistent Backup

The application is prepared before the backup.

For example:

* Stop writes
* Flush buffers
* Lock database tables
* Use database-native backup tools
* Pause the application

This improves data consistency.

---

# Database Backup Warning

A Block Volume backup of an actively writing database may not be enough by itself.

A stronger database backup process may combine:

* Database-native dump
* Transaction log backup
* Application quiescing
* Block Volume backup
* Restore testing

Do not assume that a successful volume backup guarantees a usable database restore.

---

# Create a Block Volume Backup

In the OCI Console:

```text
Storage
→ Block Storage
→ Block Volumes
→ Select application-data-volume
→ Create Backup
```

Suggested name:

```text
application-data-backup-2026-07-18
```

Document:

* Backup time
* Application state
* Volume size
* Backup type
* Retention requirement
* Restore test result

---

# Backup Policy

OCI Block Volumes can use backup policies for scheduled protection.

A policy may define:

* Backup frequency
* Backup timing
* Retention period
* Backup type

Choose a policy based on:

* RPO
* RTO
* Data importance
* Cost
* Compliance
* Restore frequency

---

# Detach the Block Volume Safely

Never detach an actively mounted volume without preparing the operating system.

Safe order:

1. Stop applications writing to the volume
2. Confirm no important process is using it
3. Flush pending writes
4. Unmount the filesystem
5. Disconnect iSCSI when applicable
6. Detach from OCI

---

# Find Processes Using the Volume

Run:

```bash
sudo lsof +f -- /data
```

Or:

```bash
sudo fuser -vm /data
```

Stop the relevant application services.

Example:

```bash
sudo systemctl stop application.service
```

---

# Flush Pending Writes

Run:

```bash
sync
```

This requests pending filesystem writes to be flushed.

---

# Unmount

Run:

```bash
sudo umount /data
```

Verify:

```bash
findmnt /data
```

There should be no mounted filesystem at `/data`.

If you receive:

```text
target is busy
```

find and stop the processes using the mount.

Do not use forceful unmounting unless you understand the risk.

---

# Prevent Automatic Remount During Detach

If you plan to keep the volume detached, comment out or remove its `/etc/fstab` entry.

Example:

```fstab
# UUID=7b6a3b72-example /data ext4 defaults,nofail 0 2
```

Keep a backup of the original configuration.

---

# Detach in OCI

After unmounting:

```text
Compute
→ Instances
→ Select the instance
→ Attached Block Volumes
→ Detach
```

For iSCSI attachments, use the provided disconnect commands before completing detachment.

---

# Attach to Another Instance

The Block Volume can be attached to another compatible Compute Instance.

```text
Original Instance
      │
      ▼
Detach Volume
      │
      ▼
New Instance
      │
      ▼
Attach Volume
```

On the new instance:

```bash
lsblk
```

Detect the existing filesystem:

```bash
sudo blkid
```

Do not run `mkfs` on an existing data volume.

Create the mount point:

```bash
sudo mkdir -p /data
```

Mount using the existing UUID:

```bash
sudo mount UUID=BLOCK_VOLUME_UUID /data
```

Verify:

```bash
ls -la /data/application
```

The original data should still exist.

---

# Critical Reattachment Warning

When attaching an existing volume, never run:

```bash
sudo mkfs.ext4 /dev/sdb1
```

`mkfs` creates a new filesystem and can destroy the existing data.

For an existing volume:

```text
Detect
→ Inspect
→ Mount
```

Not:

```text
Detect
→ Format
```

---

# Validate Data Persistence

Create a file:

```bash
echo "This file must survive instance replacement" |
sudo tee /data/application/persistence-test.txt
```

Detach the volume safely.

Attach it to another instance.

Mount it.

Then verify:

```bash
cat /data/application/persistence-test.txt
```

Expected result:

```text
This file must survive instance replacement
```

This proves that the data belongs to the volume, not the original Compute Instance.

---

# Failure Scenarios

## Compute Instance Is Terminated

```text
Compute Instance:
Terminated

Block Volume:
Still Available
```

If the Block Volume was preserved, it can be attached to another instance.

---

## Block Volume Is Detached While Mounted

Possible results include:

* Application errors
* Filesystem corruption
* Lost writes
* I/O errors
* Database corruption

Always unmount safely first.

---

## `/etc/fstab` Contains the Wrong UUID

Possible result:

* Mount fails
* Server enters emergency mode
* Application data is unavailable

Use:

```text
nofail
```

when appropriate, and test with:

```bash
sudo mount -a
```

before rebooting.

---

## Wrong Device Is Formatted

Possible result:

* Operating system destroyed
* Existing application data lost
* Instance becomes unbootable

Always verify with:

```bash
lsblk
sudo blkid
sudo fdisk -l
```

---

## Volume Mounts but Application Cannot Write

Possible cause:

* Wrong ownership
* Wrong permissions
* Read-only mount
* Application security restrictions

Check:

```bash
ls -ld /data /data/application
```

Test:

```bash
sudo -u appuser touch /data/application/write-test.txt
```

---

## Volume Is Full

Possible symptoms:

* Uploads fail
* Database writes fail
* Logs stop
* Application returns errors

Check:

```bash
df -h /data
```

---

## Volume Is Attached but Not Visible

Possible causes:

* Attachment is incomplete
* iSCSI connection commands were not run
* Operating system has not rescanned the device
* Wrong attachment type
* Device name differs from expectation

Check OCI attachment status and operating-system logs.

---

# Troubleshooting Process

## Step 1 - Check OCI Attachment

Confirm:

```text
Volume state:
Attached
```

Check the attachment type and target instance.

---

## Step 2 - Check Linux Devices

```bash
lsblk
```

```bash
sudo fdisk -l
```

---

## Step 3 - Check Filesystem Signatures

```bash
sudo blkid
```

```bash
sudo file -s /dev/sdb1
```

---

## Step 4 - Check Mount State

```bash
findmnt
```

```bash
mount | grep /data
```

---

## Step 5 - Check `/etc/fstab`

```bash
cat /etc/fstab
```

Validate:

```bash
sudo mount -a
```

---

## Step 6 - Check Permissions

```bash
ls -ld /data
ls -ld /data/application
```

---

## Step 7 - Check Capacity

```bash
df -hT /data
df -i /data
```

---

## Step 8 - Check Kernel Messages

```bash
sudo dmesg | tail -50
```

Look for:

* I/O errors
* Device connection messages
* Filesystem errors
* Mount errors

---

# Security Considerations

Block Volumes may contain sensitive data.

Protect them using:

* Least-privilege IAM
* Encryption
* Restricted instance access
* Backup controls
* Secure deletion processes
* Monitoring
* Audit logs
* Controlled volume attachments

Do not attach sensitive volumes to untrusted Compute Instances.

---

# Encryption

OCI Block Volumes are encrypted.

Organizations may also use customer-managed keys for additional control.

Conceptually:

```text
Application Data
      │
      ▼
Encrypted Block Volume
      │
      ▼
OCI Storage Infrastructure
```

When using customer-managed keys, consider:

* Key availability
* Key permissions
* Key rotation
* Recovery procedures
* Risk of disabling or deleting the key

A volume may become unusable if its required encryption key is unavailable.

---

# Monitoring

Monitor:

* Read operations
* Write operations
* IOPS
* Throughput
* Latency
* Volume attachment state
* Backup status
* Filesystem capacity
* Filesystem errors
* Application write failures

Operating-system monitoring is still necessary because OCI volume metrics do not replace filesystem monitoring.

---

# Useful Linux Monitoring Commands

Filesystem usage:

```bash
df -hT /data
```

Disk devices:

```bash
lsblk
```

Disk activity:

```bash
iostat
```

Install when required:

```bash
sudo apt install sysstat -y
```

Check open files:

```bash
sudo lsof +f -- /data
```

Check recent kernel messages:

```bash
sudo dmesg | tail
```

---

# Production Improvements

A production design may include:

* Multiple Block Volumes for separate workloads
* Logical Volume Manager
* RAID where appropriate
* Automated backup policies
* Customer-managed encryption keys
* Filesystem monitoring
* Capacity alerts
* Performance alerts
* Automated mount validation
* Infrastructure as Code
* Automated restore testing
* Cross-region backup strategy
* Database-native backup tools
* Documented recovery procedures

---

# Separate Workloads Across Volumes

Example:

```text
Compute Instance
├── Boot Volume
│   └── Operating System
│
├── Block Volume 01
│   └── Application Data
│
├── Block Volume 02
│   └── Database Data
│
└── Block Volume 03
    └── Logs and Backups
```

This provides clearer capacity and performance management.

However, it also increases operational complexity.

---

# Block Volume vs Object Storage

| Feature                 | Block Volume            | Object Storage            |
| ----------------------- | ----------------------- | ------------------------- |
| Interface               | Disk device             | API and object operations |
| Mounted filesystem      | Yes                     | Not normally              |
| Best for                | Active application data | Backups and archives      |
| Attached to instance    | Yes                     | No                        |
| Random reads and writes | Yes                     | Not like a normal disk    |
| Data organization       | Filesystem              | Buckets and objects       |

A common design uses both:

```text
Application
     │
     ▼
Block Volume
     │
     ▼
Active Data
     │
     ▼
Backup Process
     │
     ▼
Object Storage
```

Block Volume stores active data.

Object Storage stores backups.

---

# Block Volume vs File Storage

| Feature               | Block Volume                           | File Storage                  |
| --------------------- | -------------------------------------- | ----------------------------- |
| Typical attachment    | One instance or controlled attachments | Multiple clients              |
| Interface             | Block device                           | Shared filesystem             |
| Filesystem management | Managed by the instance                | Provided through file service |
| Best for              | Databases and dedicated disks          | Shared files                  |
| Common protocol       | Block attachment                       | NFS                           |

Use Block Volume when one server needs a dedicated disk.

Use File Storage when multiple servers need a shared filesystem.

---

# Validation Checklist

```text
[ ] Compute Instance exists
[ ] Block Volume exists
[ ] Volume and instance have compatible placement
[ ] Volume is attached
[ ] Correct device was identified
[ ] Existing filesystem signatures were checked
[ ] Partition was created only on a new empty disk
[ ] Filesystem was created successfully
[ ] Mount point exists
[ ] Volume is mounted at /data
[ ] Application directory exists
[ ] Ownership is correct
[ ] Application user can write data
[ ] Filesystem UUID was recorded
[ ] /etc/fstab uses the correct UUID
[ ] mount -a succeeds
[ ] Volume mounts automatically after reboot
[ ] Sample data survives reboot
[ ] Block Volume backup exists
[ ] Detach process was tested safely
[ ] Data remains available after reattachment
[ ] Capacity monitoring is configured
```

---

# Cleanup Order

Delete resources carefully in this order:

1. Stop applications using `/data`
2. Confirm no processes are using the volume
3. Run `sync`
4. Unmount `/data`
5. Remove or comment out the `/etc/fstab` entry
6. Disconnect iSCSI when applicable
7. Detach the Block Volume
8. Confirm whether backups must be retained
9. Delete the Block Volume only if its data is no longer required
10. Terminate the Compute Instance
11. Delete networking resources
12. Delete the Compartment if it is empty

Deleting a Block Volume permanently removes its data unless a usable backup exists.

---

# What You Learned

After completing this scenario, you should understand:

* What an OCI Block Volume is
* The difference between a Boot Volume and a Block Volume
* Why application data should be separated from the operating system
* How Block Volumes relate to Compute Instances
* What a volume attachment does
* Why OCI attachment and Linux mounting are separate steps
* How Linux detects a new disk
* How to identify the correct block device
* Why checking existing filesystem signatures is important
* How to create a partition and filesystem
* How to mount a filesystem
* How to persist a mount using `/etc/fstab`
* Why UUIDs are safer than device names
* How to configure permissions for application users
* How to use a Block Volume with Docker
* How volume data can survive instance replacement
* How to detach and reattach a volume safely
* Why formatting an existing volume destroys data
* How Block Volume backups protect persistent data
* The difference between Block Volume, File Storage, and Object Storage
* How to troubleshoot storage attachment and mount problems

---

# Main Relationship to Remember

```text
Compute Instance
      │
      ▼
Volume Attachment
      │
      ▼
Block Volume
      │
      ▼
Linux Block Device
      │
      ▼
Filesystem
      │
      ▼
Mount Point
      │
      ▼
Application Data
```

The most important operational rule is:

```text
Attach does not mean mounted.
```

OCI handles:

```text
Block Volume → Compute Instance attachment
```

Linux handles:

```text
Device → Filesystem → Mount Point
```

The safest workflow for a new empty volume is:

```text
Detect
  ↓
Verify
  ↓
Partition
  ↓
Format
  ↓
Mount
  ↓
Persist
  ↓
Test
```

For an existing data volume:

```text
Detect
  ↓
Inspect
  ↓
Mount
```

Never format an existing volume unless you intentionally want to erase it.

---

# Next Scenario

Scenario 08:

```text
IAM Access for a DevOps Team
```

The next scenario will create users, groups, and policies for a DevOps team.

```text
DevOps Users
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

We will explain:

* Users
* Groups
* Policies
* Compartments
* Least privilege
* `inspect`, `read`, `use`, and `manage`
* How DevOps engineers receive controlled access
* Why users should not receive full tenancy administrator permissions
