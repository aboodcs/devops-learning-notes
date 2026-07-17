# 03 - IAM Users, Groups, and Policies

**IAM** means **Identity and Access Management**.

In OCI, IAM controls:

```text
Who can access OCI
What they can do
Where they can do it
```

The main IAM parts are:

```text
Users       → People or accounts
Groups      → Collection of users
Policies    → Permission rules
Compartments → Places where resources are organized
```

## Why Do We Need IAM?

Without IAM, every user may have too much access.

That is dangerous.

IAM helps you give each user only the permissions they need.

```text
User → Group → Policy → Access to OCI resources
```

Example:

```text
Abdulrahman → DevOps Group → Can manage Compute Instances in Dev compartment
```

## 1. Users

A **User** represents a person or account that can log in to OCI.

Examples:

```text
admin user
developer user
devops user
auditor user
```

A user can:

```text
Login to OCI Console
Use OCI CLI
Use Terraform
Use API keys
Manage cloud resources if allowed
```

But a user does not get permissions automatically.

Permissions come from groups and policies.

## 2. Groups

A **Group** is a collection of users.

Instead of giving permissions to every user one by one, you give permissions to a group.

Then you add users to that group.

Example:

```text
Group: DevOps-Team
├── abood
├── ahmad
└── sara
```

If the group has permission to manage Compute Instances, all users inside the group get that permission.

## Why Use Groups?

Groups make permission management easier.

Bad way:

```text
Give permissions directly to every user
```

Better way:

```text
Add users to groups
Give permissions to groups
```

Example groups:

```text
DevOps-Team
Developers
Network-Admins
Security-Team
Auditors
```

## 3. Policies

A **Policy** is a rule that gives permissions.

A policy answers three questions:

```text
Who gets access?
What can they do?
Where can they do it?
```

Basic policy format:

```text
allow group GROUP_NAME to VERB RESOURCE_TYPE in compartment COMPARTMENT_NAME
```

Example:

```text
allow group DevOps-Team to manage instance-family in compartment Dev
```

Meaning:

```text
Group: DevOps-Team
Permission: manage
Resource: Compute instances
Location: Dev compartment
```

## Policy Verbs

OCI policies use permission levels called verbs.

```text
inspect → List resources
read    → View resource details
use     → Use resources
manage  → Full control
```

## 1. inspect

`inspect` allows users to list resources.

Example:

```text
allow group Auditors to inspect all-resources in compartment Dev
```

Meaning:

```text
They can see that resources exist.
```

## 2. read

`read` allows users to view resource details.

Example:

```text
allow group Auditors to read all-resources in compartment Dev
```

Meaning:

```text
They can view resource information, but not change it.
```

## 3. use

`use` allows users to work with resources but not fully manage them.

Example:

```text
allow group Developers to use instance-family in compartment Dev
```

Meaning:

```text
They can use Compute resources, but they do not have full admin control.
```

## 4. manage

`manage` gives full control.

Example:

```text
allow group DevOps-Team to manage all-resources in compartment Dev
```

Meaning:

```text
They can create, update, and delete resources in the Dev compartment.
```

Use `manage` carefully.

## Common Resource Types

```text
all-resources          → All resource types
instance-family        → Compute instances
volume-family          → Block volumes
virtual-network-family → VCNs, subnets, route tables, gateways
object-family          → Object Storage
database-family        → Database resources
```

## Example Policies

### DevOps Team Can Manage Compute

```text
allow group DevOps-Team to manage instance-family in compartment Dev
```

### Network Admins Can Manage Networking

```text
allow group Network-Admins to manage virtual-network-family in compartment Dev
```

### Developers Can Use Instances

```text
allow group Developers to use instance-family in compartment Dev
```

### Auditors Can Read Everything

```text
allow group Auditors to read all-resources in compartment Dev
```

### Admins Can Manage Everything in Tenancy

```text
allow group Cloud-Admins to manage all-resources in tenancy
```

This is powerful and should be used only for trusted administrators.

## 4. Compartments

A **Compartment** is a logical container for OCI resources.

Example:

```text
Tenancy
├── Dev
├── Test
└── Production
```

You can create resources inside compartments:

```text
Compute Instances
VCNs
Subnets
Load Balancers
Block Volumes
Object Storage Buckets
```

Policies usually apply to a compartment.

Example:

```text
allow group DevOps-Team to manage all-resources in compartment Dev
```

This gives access only inside the `Dev` compartment.

## IAM Flow Example

```text
User: abood
   │
   ▼
Group: DevOps-Team
   │
   ▼
Policy:
allow group DevOps-Team to manage instance-family in compartment Dev
   │
   ▼
Result:
abood can manage Compute Instances inside Dev compartment
```

## Real Beginner Example

Suppose we have a developer named `abood`.

We want him to manage Compute Instances only in the `Dev` compartment.

Steps:

```text
1. Create user: abood
2. Create group: DevOps-Team
3. Add abood to DevOps-Team
4. Create policy for DevOps-Team
```

Policy:

```text
allow group DevOps-Team to manage instance-family in compartment Dev
```

Now `abood` can manage Compute Instances in `Dev`.

He cannot automatically manage networking, databases, or production resources unless another policy allows it.

## Console Path

To manage IAM in OCI Console:

```text
OCI Console
→ Identity & Security
→ Domains
→ Default domain
→ Users
```

For groups:

```text
OCI Console
→ Identity & Security
→ Domains
→ Default domain
→ Groups
```

For policies:

```text
OCI Console
→ Identity & Security
→ Policies
```

For compartments:

```text
OCI Console
→ Identity & Security
→ Compartments
```

## Important Security Rule

Use the principle of least privilege.

This means:

```text
Give users only the permissions they need.
Do not give manage all-resources unless required.
Separate Dev, Test, and Production.
Use groups instead of direct user permissions.
Review policies regularly.
```

## Common Mistakes

### Giving Too Much Access

Bad:

```text
allow group Developers to manage all-resources in tenancy
```

This gives developers full access to everything.

Better:

```text
allow group Developers to use instance-family in compartment Dev
```

### Not Using Compartments

Putting everything in one place makes access control harder.

Better:

```text
Dev compartment
Test compartment
Production compartment
```

### Creating Policies for Every User

Bad:

```text
Policy for user1
Policy for user2
Policy for user3
```

Better:

```text
Add users to groups
Create policies for groups
```

## IAM Summary

```text
User        → Person or account
Group       → Collection of users
Policy      → Permission rule
Compartment → Logical place for resources
Verb        → Permission level
Resource    → OCI service or resource type
```

## Simple Final Example

```text
User:
abood

Group:
DevOps-Team

Compartment:
Dev

Policy:
allow group DevOps-Team to manage instance-family in compartment Dev
```

Meaning:

```text
abood can manage Compute Instances in the Dev compartment because he is inside the DevOps-Team group.
```

## Summary

```text
Users do not get permissions alone.
Users are added to groups.
Groups receive permissions through policies.
Policies define what can be done and where.
Compartments organize resources and limit access scope.
```

> In OCI IAM, users belong to groups, groups get policies, and policies control access to resources inside compartments.

