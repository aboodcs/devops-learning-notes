# 02 - Tenancy and Compartments

In OCI, two important organization concepts are:

```text id="7v80qt"
Tenancy      → Your main Oracle Cloud account
Compartment  → Folder-like area inside the tenancy
```

## What Is a Tenancy?

A **Tenancy** is your main OCI account.

When you create an Oracle Cloud account, Oracle creates a tenancy for you.

Think of tenancy as the top-level container for everything in your Oracle Cloud.

```text id="r8d4fm"
OCI Tenancy
├── Users
├── Groups
├── Policies
├── Compartments
├── Networks
├── Compute Instances
├── Storage
└── Databases
```

## Simple Explanation

A tenancy is like the main company account in Oracle Cloud.

Example:

```text id="savgi1"
Company: MyCompany
Cloud Account: MyCompany Tenancy
```

Everything you create in OCI belongs to your tenancy.

## What Is Inside a Tenancy?

A tenancy contains:

```text id="r1284s"
IAM users
Groups
Policies
Compartments
Cloud resources
Billing information
Regions
Identity domains
```

Your tenancy is the highest level of your OCI environment.

## What Is a Compartment?

A **Compartment** is a logical container inside a tenancy.

It is used to organize cloud resources.

Think of it like a folder.

```text id="cx6q8j"
Tenancy
├── Dev Compartment
├── Test Compartment
└── Production Compartment
```

Each compartment can contain OCI resources such as:

```text id="7sy8w0"
Compute Instances
VCNs
Subnets
Block Volumes
Object Storage Buckets
Load Balancers
Databases
```

## Why Do We Need Compartments?

Without compartments, all resources would be in one place.

That becomes messy and dangerous.

Compartments help you:

```text id="c7eqp4"
Organize resources
Separate environments
Control access
Manage billing
Protect production resources
```

## Example

Imagine you are building a DevOps project.

You can create separate compartments:

```text id="l71gms"
Dev        → For testing and learning
Staging    → Before production
Production → Real application
```

This makes your cloud account cleaner and safer.

## Tenancy vs Compartment

| Tenancy                             | Compartment                      |
| ----------------------------------- | -------------------------------- |
| Main OCI account                    | Logical container inside tenancy |
| Created when OCI account is created | Created by user/admin            |
| Top-level cloud environment         | Used to organize resources       |
| Contains all OCI resources          | Contains selected resources      |
| One tenancy per cloud account       | Many compartments inside tenancy |

## Root Compartment

Every tenancy has a root compartment.

The root compartment represents the whole tenancy.

```text id="io58s1"
Tenancy Root
├── Dev
├── Test
└── Production
```

For learning, you may see resources created in the root compartment.

But in real projects, it is better to create separate compartments.

## Best Practice

Do not put everything in the root compartment.

Better structure:

```text id="n80v79"
Tenancy
├── Networking
├── Development
├── Testing
├── Production
└── Security
```

This makes access control easier.

## Compartments and IAM Policies

Compartments are important because OCI policies can limit access to a specific compartment.

Example policy:

```text id="sus6p2"
allow group DevOps-Team to manage instance-family in compartment Dev
```

Meaning:

```text id="3g7tu3"
The DevOps-Team group can manage Compute Instances only inside the Dev compartment.
```

They do not automatically get access to Production.

## Simple IAM Flow

```text id="j3b7sf"
User
  ↓
Group
  ↓
Policy
  ↓
Compartment access
```

Example:

```text id="nhpax3"
Abdulrahman
  ↓
DevOps-Team
  ↓
allow group DevOps-Team to manage all-resources in compartment Dev
  ↓
Can manage resources inside Dev
```

## Create a Compartment

Console path:

```text id="5ouyvl"
OCI Console
→ Identity & Security
→ Compartments
→ Create Compartment
```

Example compartment name:

```text id="dgvtb1"
Dev
```

Description:

```text id="t9dr43"
Compartment for development and learning resources
```

## Compartment Hierarchy

Compartments can also have child compartments.

Example:

```text id="zm3iuv"
Tenancy
└── Projects
    ├── Project-A
    ├── Project-B
    └── Project-C
```

For beginners, keep the structure simple.

Start with:

```text id="xx0x2k"
Dev
Test
Production
```

## Moving Resources Between Compartments

Some OCI resources can be moved from one compartment to another.

Example:

```text id="opn69z"
Move Compute Instance from Dev to Test
```

But do not rely on moving resources too much.

It is better to plan the compartment structure before creating resources.

## Common Beginner Mistake

Creating resources in the wrong compartment.

Example:

```text id="g8pk7n"
You create a Compute Instance in root compartment,
but your policy allows access only to Dev compartment.
```

Then you may not see or manage the resource as expected.

Always check the selected compartment in the OCI Console.

## Where to Check Current Compartment

In many OCI Console pages, there is a compartment selector.

Example:

```text id="oh0i1y"
Compute
→ Instances
→ Compartment dropdown
```

If you do not see your resource, check if you are viewing the correct compartment.

## Practical Example

You want to create a learning environment.

Recommended structure:

```text id="do5sbo"
Tenancy
└── Dev
    ├── VCN
    ├── Public Subnet
    ├── Compute Instance
    └── Block Volume
```

Then create a group:

```text id="so02st"
DevOps-Team
```

And create a policy:

```text id="n4wnmm"
allow group DevOps-Team to manage all-resources in compartment Dev
```

Now users inside `DevOps-Team` can work safely inside the `Dev` compartment.

## Summary

```text id="h84g6f"
Tenancy      → Main Oracle Cloud account
Root compartment → Top-level compartment
Compartment  → Logical container for resources
IAM Policy   → Controls access to compartments
```

> A tenancy is your whole OCI account. A compartment is a folder-like space inside the tenancy used to organize and control access to resources.

