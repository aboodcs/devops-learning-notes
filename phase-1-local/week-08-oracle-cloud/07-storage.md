# 07 - Storage

In OCI, **Storage** is used to save data.

Cloud applications need storage for different reasons:

```text id="wklf82"
Operating systems
Application files
Databases
Backups
Images
Videos
Logs
Shared files
Docker data
```

OCI provides different storage services because not all data is used the same way.

The main storage services are:

```text id="50hv6d"
Block Volume
Object Storage
File Storage
```

## Simple Explanation

```text id="a7gwg4"
Block Volume  → Virtual hard disk
Object Storage → Storage for files and objects
File Storage   → Shared file system
```

Think about it like this:

```text id="rf68y0"
Block Volume  → Like an SSD attached to one server
Object Storage → Like Google Drive / S3-style storage
File Storage   → Like a shared network folder
```

## 1. Block Volume

**Block Volume** is a virtual hard disk.

It can be attached to a Compute Instance.

```text id="6cktag"
Compute Instance
├── Boot Volume
└── Block Volume
```

The instance sees the Block Volume like an extra disk.

## What Is It Used For?

Use Block Volume for:

```text id="fwhe05"
Operating system disk
Database storage
Application data
Docker volumes
Persistent server data
```

Example:

```text id="x7soz3"
Ubuntu Compute Instance
└── Block Volume mounted at /data
```

The application can save files inside `/data`.

## Boot Volume vs Block Volume

When you create a Compute Instance, OCI automatically creates a **Boot Volume**.

The Boot Volume contains the operating system.

Example:

```text id="d7altv"
Boot Volume
└── Ubuntu OS
```

A normal Block Volume is extra storage that you attach later.

```text id="j5z9mc"
Compute Instance
├── Boot Volume  → OS disk
└── Block Volume → Extra data disk
```

## Block Volume Features

Block Volume is useful because it is:

```text id="kvf7td"
Persistent
Resizable
High performance
Attachable to Compute Instances
Backup supported
Good for databases and applications
```

Persistent means the data can remain even if the instance is stopped.

## Block Volume Example

```text id="spyw3e"
Compute Instance
   │
   ▼
Block Volume
   │
   ▼
Application data
```

Example use case:

```text id="f7ss3n"
A database server stores database files on a Block Volume.
```

If the Compute Instance has a problem, the Block Volume can still be protected using backups.

## 2. Object Storage

**Object Storage** is used to store files as objects.

Objects are stored inside containers called **buckets**.

```text id="m7gr78"
Object Storage
└── Bucket
    ├── image.png
    ├── backup.zip
    ├── logs.txt
    └── video.mp4
```

## What Is a Bucket?

A **bucket** is like a folder or container in Object Storage.

Example bucket names:

```text id="klx5c3"
app-backups
website-images
logs-bucket
terraform-state
```

Inside a bucket, you store objects.

## What Is It Used For?

Use Object Storage for:

```text id="ws3q97"
Backups
Images
Videos
Logs
Static files
Archives
Terraform state
Application uploads
```

Example:

```text id="d0abqw"
Web Application
   │
   ▼
Upload image
   │
   ▼
Object Storage Bucket
```

## Object Storage Features

Object Storage is useful because it is:

```text id="gavqvu"
Durable
Scalable
Good for large files
Good for backups
Accessible through API
Good for static files
```

Object Storage is not attached like a disk.

You usually access it using:

```text id="y7wxka"
OCI Console
OCI CLI
SDK
API
Application code
```

## Object Storage Example

A website allows users to upload profile images.

Instead of saving images directly on the server, the app stores them in Object Storage.

```text id="h9tv97"
User uploads image
        ↓
Application
        ↓
Object Storage Bucket
```

This is better because images are separated from the server.

## 3. File Storage

**File Storage** provides a shared file system.

Multiple Compute Instances can access the same shared files.

```text id="fl8wfk"
File Storage
├── Compute Instance 1
├── Compute Instance 2
└── Compute Instance 3
```

This is similar to a shared network folder.

## What Is It Used For?

Use File Storage when many servers need access to the same files.

Examples:

```text id="p6c2ev"
Shared application files
Shared uploads
Content management systems
Logs shared between servers
Multi-server applications
```

## File Storage Example

```text id="zoceg4"
Load Balancer
├── Web Server 1
├── Web Server 2
└── Web Server 3

All web servers use the same File Storage.
```

If a user uploads a file from Web Server 1, Web Server 2 can also access it.

## Block vs Object vs File Storage

| Storage Type   | Simple Meaning           | Best For                        |
| -------------- | ------------------------ | ------------------------------- |
| Block Volume   | Virtual hard disk        | Databases, OS disks, app data   |
| Object Storage | Bucket for files/objects | Backups, images, logs, archives |
| File Storage   | Shared file system       | Shared files between servers    |

## Simple Comparison

```text id="c9hn59"
Need a disk for one server?
Use Block Volume.

Need to store backups or uploaded files?
Use Object Storage.

Need many servers to share the same files?
Use File Storage.
```

## Real DevOps Examples

### Docker Data

If you run Docker on an OCI Compute Instance, you may use Block Volume for Docker data.

```text id="nij3b0"
Compute Instance
└── Block Volume
    └── Docker volumes
```

### Application Backups

Use Object Storage to save backups.

```text id="i6cf95"
Database backup
      ↓
Object Storage Bucket
```

### Multiple Web Servers

Use File Storage when multiple servers need the same uploaded files.

```text id="8r9z4r"
Web Server 1
Web Server 2
Web Server 3
      ↓
File Storage
```

## Storage and Security

Storage can contain sensitive data.

Protect it carefully.

Important rules:

```text id="meq060"
Do not make buckets public unless needed
Use IAM policies
Use encryption
Use backups
Limit access by groups
Do not store secrets in plain text
```

## Object Storage Public vs Private

A bucket should usually be private.

Private means only allowed users or applications can access it.

```text id="w1ywv6"
Private bucket → safer
Public bucket  → accessible from internet
```

Use public buckets only for public files, such as website images or static assets.

## Backups

Backups are important because storage can be deleted by mistake.

Use backups for:

```text id="r8ldgd"
Block Volumes
Databases
Important application files
Configuration files
```

Example:

```text id="q3x4i5"
Block Volume
   ↓
Backup
   ↓
Restore when needed
```

## Storage in a Simple OCI Architecture

```text id="yzfwai"
OCI Compartment
└── VCN
    ├── Public Subnet
    │   └── Compute Instance
    │       └── Block Volume
    │
    ├── Object Storage Bucket
    │   └── Backups and uploaded files
    │
    └── File Storage
        └── Shared files for multiple servers
```

## Common Beginner Mistakes

### Using Block Volume for Backups Only

Block Volume is a disk.

For backup files, Object Storage is usually better.

### Making Object Storage Public by Mistake

Bad:

```text id="z5ctoa"
Public bucket with private files
```

Better:

```text id="e5g6ut"
Private bucket with IAM access
```

### Saving Important Data Only Inside the Instance

If you save everything only inside the server and delete the server, you may lose data.

Better:

```text id="jbpccg"
Use Block Volume
Use Object Storage backups
Use proper backup policy
```

### Using File Storage for One Server Only

If only one server needs the data, Block Volume may be simpler.

File Storage is more useful when multiple servers share the same files.

## Console Path

To manage storage in OCI:

```text id="62onpi"
OCI Console
→ Storage
```

Common storage pages:

```text id="ggw1qh"
Block Storage
Object Storage
File Storage
```

For Compute boot volumes:

```text id="js6fok"
OCI Console
→ Compute
→ Instances
→ Instance details
→ Boot volume
```

## Simple Decision Guide

```text id="gaxr1r"
Question:
Do I need a disk attached to a server?

Answer:
Use Block Volume.
```

```text id="iick9o"
Question:
Do I need to store files, backups, images, or logs?

Answer:
Use Object Storage.
```

```text id="5anadv"
Question:
Do multiple servers need the same shared folder?

Answer:
Use File Storage.
```

## Summary

```text id="8s09p8"
Block Volume  → Virtual disk attached to Compute Instance
Boot Volume   → Disk that contains the operating system
Object Storage → Bucket-based storage for files and backups
Bucket        → Container for objects
File Storage  → Shared file system for multiple servers
Backup        → Copy of data used for recovery
```

> In OCI, use Block Volume for disks, Object Storage for files and backups, and File Storage for shared file systems.

