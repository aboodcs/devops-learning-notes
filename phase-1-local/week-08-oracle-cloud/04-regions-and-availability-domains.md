# 04 - Regions and Availability Domains

OCI is built using three physical location concepts:

```text id="0ivftw"
Region
Availability Domain
Fault Domain
```

These concepts help you understand where your cloud resources run and how to design applications that stay available.

Oracle defines a region as a geographic area, an availability domain as one or more data centers inside a region, and fault domains as hardware groupings inside an availability domain.

## 1. Region

A **Region** is a geographic location where OCI has cloud infrastructure.

Examples of regions:

```text id="bowdco"
Saudi Arabia
United Arab Emirates
Germany
United Kingdom
United States
```

When you create a resource, you usually choose the region first.

Example:

```text id="hvrpud"
Region: Saudi Arabia Central
Resource: Compute Instance
```

## Why Regions Matter

Regions affect:

```text id="54go7u"
Latency
Availability
Compliance
Cost
Disaster recovery
```

If your users are in Jordan or the Middle East, choosing a nearby region usually gives lower latency than choosing a far region.

## 2. Availability Domain

An **Availability Domain** is an isolated data center location inside a region.

A region can have one or more availability domains.

```text id="mhna97"
Region
├── Availability Domain 1
├── Availability Domain 2
└── Availability Domain 3
```

Availability domains are isolated from each other and designed so they are unlikely to fail at the same time.

## Why Availability Domains Matter

Availability Domains help with high availability.

If you put everything in one availability domain and that domain has a problem, your application may go down.

Better design:

```text id="8wt6j2"
Load Balancer
├── Compute Instance in AD-1
└── Compute Instance in AD-2
```

If one availability domain has a problem, the other one can still run the application.

## 3. Fault Domain

A **Fault Domain** is a smaller isolation area inside an availability domain.

Each availability domain contains three fault domains.

```text id="ca9mzq"
Availability Domain
├── Fault Domain 1
├── Fault Domain 2
└── Fault Domain 3
```

Fault domains help protect against hardware failure or maintenance inside one availability domain.

## Simple Explanation

Think about it like this:

```text id="s9q6cu"
Region              → City
Availability Domain → Building
Fault Domain        → Floor inside the building
```

If one floor has a problem, the other floors may still work.

If one building has a problem, another building may still work.

If one city has a problem, another city may still work.

## Region vs Availability Domain vs Fault Domain

| Concept             | Meaning                                      | Example Use                                |
| ------------------- | -------------------------------------------- | ------------------------------------------ |
| Region              | Geographic area                              | Choose where your cloud resources run      |
| Availability Domain | Isolated data center inside a region         | Run app across multiple data centers       |
| Fault Domain        | Hardware group inside an availability domain | Spread instances across different hardware |

## Resource Placement

Some OCI resources are regional.

Examples:

```text id="c6lbti"
VCN
Route Table
Security List
Object Storage Bucket
```

Some resources are availability-domain specific.

Examples:

```text id="u8bdrm"
Compute Instance
Block Volume
```

This means when creating a Compute Instance, OCI may ask you to choose an availability domain.

## Basic Architecture Example

Simple application in one region:

```text id="vdl8rn"
Region
└── Availability Domain 1
    ├── Fault Domain 1 → Web Server 1
    ├── Fault Domain 2 → Web Server 2
    └── Fault Domain 3 → Database
```

Better high availability design:

```text id="imgdf8"
Region
├── Availability Domain 1
│   └── Web Server 1
│
└── Availability Domain 2
    └── Web Server 2
```

## High Availability Levels

### Low Availability

```text id="8cj2zi"
One server
One fault domain
One availability domain
One region
```

If the server fails, the application goes down.

### Better Availability

```text id="nnuqj0"
Two servers
Different fault domains
Same availability domain
```

This protects against some hardware failures.

### Higher Availability

```text id="r2k0ek"
Two servers
Different availability domains
Same region
```

This protects against an availability domain problem.

### Disaster Recovery

```text id="xxrlk3"
Primary region
Backup region
```

This protects against a larger regional issue.

## DevOps Example

For a learning project, you can start simple:

```text id="4pcszs"
One region
One availability domain
One compute instance
```

For a production project, you should think about:

```text id="xauqpq"
Multiple compute instances
Multiple fault domains
Multiple availability domains
Load balancer
Backups
Disaster recovery region
```

## Common Beginner Mistakes

### Choosing a Far Region

If your users are in the Middle East, choosing a far region may increase latency.

### Putting Everything in One Place

If all resources are in one fault domain or one availability domain, the application has a single point of failure.

### Ignoring Fault Domains

Even inside one availability domain, use fault domains to spread resources across different hardware.

### Confusing Region and Availability Domain

A region is the geographic area.

An availability domain is inside the region.

A fault domain is inside the availability domain.

## Simple Final Example

```text id="2kmpxa"
Region: Saudi Arabia Central

Availability Domain:
AD-1

Fault Domains:
FD-1
FD-2
FD-3
```

If you create three Compute Instances, a better design is:

```text id="we805i"
Instance 1 → FD-1
Instance 2 → FD-2
Instance 3 → FD-3
```

This reduces the chance that one hardware problem affects all instances.

## Summary

```text id="h79slk"
Region              → Geographic cloud location
Availability Domain → Isolated data center area inside a region
Fault Domain        → Hardware isolation group inside an availability domain
```

> Regions decide where your resources run. Availability domains protect against data center failures. Fault domains protect against hardware failures inside one availability domain.

