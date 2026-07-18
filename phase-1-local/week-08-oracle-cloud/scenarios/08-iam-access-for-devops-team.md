# Scenario 08 - Configure IAM Access for a DevOps Team

## Goal

In this scenario, we will configure controlled access for a DevOps team in Oracle Cloud Infrastructure.

We will create:

* DevOps users
* A DevOps group
* A dedicated Compartment
* IAM Policies
* Read-only access for auditors
* Limited administrative access for DevOps engineers
* A safer permission model based on least privilege

The main goal is to avoid giving every team member full administrator access to the entire tenancy.

---

# Final Access Architecture

```text
                         OCI Tenancy
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Identity Domain             Compartments
                 │                         │
                 ▼                         ▼
              Users                  Dev Compartment
                 │                         │
                 ▼                         ▼
              Groups                  OCI Resources
                 │                         │
                 ▼                         │
             IAM Policies ────────────────┘
```

DevOps team flow:

```text
DevOps User
    │
    ▼
DevOps Group
    │
    ▼
IAM Policy
    │
    ▼
Allowed Resources
    │
    ▼
Development Compartment
```

---

# What We Want to Build

We will create:

* One Compartment named `development`
* One IAM group named `devops-team`
* One IAM group named `devops-readonly`
* One IAM group named `network-admins`
* Two DevOps users
* One auditor user
* Policies for Compute
* Policies for networking
* Policies for Load Balancers
* Read-only policies
* Optional permissions for Object Storage
* MFA requirements
* A testing process for every user

Example users:

```text
abdulrahman.devops
```

```text
sara.devops
```

```text
omar.auditor
```

---

# Why IAM Is Important

IAM stands for Identity and Access Management.

IAM answers four important questions:

```text
Who are you?
```

```text
How do you prove your identity?
```

```text
Which group do you belong to?
```

```text
What are you allowed to do?
```

Without proper IAM controls, users may receive more permissions than they need.

That can cause:

* Accidental deletion
* Security incidents
* Unauthorized access
* Exposure of sensitive data
* Unexpected cloud costs
* Difficult auditing
* Compliance problems

---

# Main IAM Components

OCI IAM includes several connected concepts:

```text
Identity Domain
      │
      ├── Users
      ├── Groups
      ├── Authentication Settings
      └── MFA
```

Policies connect identities to resources:

```text
Group
   │
   ▼
Policy
   │
   ▼
Compartment
   │
   ▼
Resources
```

---

# Identity Domain

An Identity Domain is a container for identities and authentication settings.

It can contain:

* Users
* Groups
* Applications
* MFA configuration
* Password policies
* Federation settings
* Sign-on policies

The default Identity Domain is commonly used for OCI Console users.

Conceptually:

```text
Tenancy
   │
   ▼
Identity Domain
   │
   ├── Users
   ├── Groups
   └── Authentication Rules
```

---

# User

A User represents a human identity.

Examples:

```text
DevOps Engineer
Cloud Administrator
Developer
Auditor
Security Engineer
```

A User can:

* Sign in to the OCI Console
* Use the OCI CLI
* Use API keys
* Belong to one or more Groups
* Use MFA
* Receive permissions through Group membership

A User should normally receive permissions through Groups, not through individual exceptions.

---

# Group

A Group contains Users who need similar permissions.

Example:

```text
devops-team
├── abdulrahman.devops
└── sara.devops
```

The Group itself does not automatically have permissions.

Policies grant permissions to the Group.

```text
Users
  │
  ▼
Group
  │
  ▼
Policy
  │
  ▼
Resources
```

---

# IAM Policy

An IAM Policy is a collection of statements that grant permissions.

Example:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

This means:

```text
Who:
devops-team
```

```text
Action:
manage
```

```text
Resource:
instance-family
```

```text
Location:
development compartment
```

---

# Policy Statement Structure

A common OCI policy statement follows this structure:

```text
Allow group <group-name>
to <verb> <resource-type>
in compartment <compartment-name>
```

Example:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

The statement contains four major parts.

## Subject

```text
group devops-team
```

Who receives the permission.

## Verb

```text
manage
```

The permission level.

## Resource Type

```text
instance-family
```

The resource category.

## Scope

```text
in compartment development
```

Where the permission applies.

---

# OCI Permission Verbs

OCI commonly uses four permission verbs:

```text
inspect
read
use
manage
```

They represent increasing levels of access.

```text
inspect
   ↓
read
   ↓
use
   ↓
manage
```

---

# Inspect

`inspect` provides basic visibility.

A user may be able to see:

* Resource names
* Resource types
* Basic metadata
* Resource listings

The user may not be able to read detailed configuration or modify anything.

Example:

```text
Allow group devops-readonly
to inspect all-resources
in compartment development
```

Use `inspect` when users only need basic inventory visibility.

---

# Read

`read` includes `inspect` and allows users to view more detailed information.

Users may be able to:

* List resources
* Open resource details
* Read configuration
* View status
* View metadata

They still cannot normally make changes.

Example:

```text
Allow group devops-readonly
to read all-resources
in compartment development
```

Use `read` for:

* Auditors
* Support engineers
* Observers
* Junior team members
* Troubleshooting roles that do not need write access

---

# Use

`use` includes some operational actions without full administration.

Depending on the resource type, it may allow users to:

* Use an existing network
* Attach resources
* Start or stop some resources
* Connect resources together
* Consume an existing service

It may not allow deletion or full configuration management.

Example:

```text
Allow group devops-team
to use virtual-network-family
in compartment development
```

This can allow the team to use existing networking resources without giving full network administration rights.

---

# Manage

`manage` is the broadest standard verb.

It generally includes:

* Create
* Update
* Start
* Stop
* Attach
* Detach
* Delete
* Read
* Inspect

Example:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

Use `manage` carefully.

Do not assume that every DevOps engineer needs `manage all-resources`.

---

# Permission Hierarchy

Conceptually:

```text
manage
├── use
├── read
└── inspect
```

And:

```text
use
├── read
└── inspect
```

And:

```text
read
└── inspect
```

The exact permissions depend on the resource type.

---

# Resource Families

OCI Policies can target individual resources or resource families.

Examples:

```text
instance-family
```

```text
virtual-network-family
```

```text
volume-family
```

```text
load-balancers
```

```text
object-family
```

A resource family groups related resource types.

---

# Instance Family

`instance-family` generally covers resources related to Compute Instances.

Conceptually, it may include:

* Instances
* Console connections
* VNIC attachments
* Instance actions
* Related Compute operations

Example:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

This allows the DevOps team to manage Compute resources inside the `development` Compartment.

---

# Virtual Network Family

`virtual-network-family` covers VCN networking resources.

Conceptually, it may include:

* VCNs
* Subnets
* Route Tables
* Internet Gateways
* NAT Gateways
* Service Gateways
* Security Lists
* Network Security Groups
* VNIC-related networking components

Example:

```text
Allow group network-admins
to manage virtual-network-family
in compartment development
```

Networking permissions are powerful and should often be separated from general application permissions.

---

# Volume Family

`volume-family` covers Block Volume-related resources.

Example:

```text
Allow group devops-team
to manage volume-family
in compartment development
```

This may allow the team to:

* Create Block Volumes
* Attach volumes
* Detach volumes
* Resize volumes
* Delete volumes
* Manage backups where included

Storage deletion can cause permanent data loss, so use this permission carefully.

---

# Load Balancer Permissions

Example:

```text
Allow group devops-team
to manage load-balancers
in compartment development
```

This lets the team manage:

* Load Balancers
* Listeners
* Backend Sets
* Backend servers
* Health checks
* Certificates associated with supported operations

---

# Object Storage Permissions

Object Storage permissions should be separated according to the required actions.

A broad example:

```text
Allow group devops-team
to manage object-family
in compartment development
```

This may be broader than necessary.

A safer design may separate:

* Bucket administration
* Object upload and download
* Object deletion

For example, a backup operator may need to manage objects but not delete buckets.

---

# Compartments

A Compartment is a logical container for OCI resources.

Example:

```text
Tenancy
├── development
├── staging
├── production
└── security
```

Compartments help organize:

* Resources
* Access
* Cost tracking
* Ownership
* Policies
* Environments

---

# Why Use Compartments for Access Control?

Suppose the DevOps team needs full access to development resources but only read access to production.

A compartment structure makes this possible.

```text
development
└── DevOps Team: Manage

production
└── DevOps Team: Read
```

Example policies:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

```text
Allow group devops-team
to read instance-family
in compartment production
```

The same group receives different access in different environments.

---

# Suggested Compartment Structure

```text
Tenancy
├── shared-services
├── development
├── staging
├── production
└── security
```

## Shared Services

Contains:

* Shared networks
* Bastion
* DNS
* Central logging
* Monitoring services
* Shared Container Registry

## Development

Contains:

* Development Compute Instances
* Test databases
* Development Load Balancers
* Temporary storage

## Staging

Contains:

* Pre-production infrastructure
* Integration testing resources
* Release validation environments

## Production

Contains:

* Customer-facing workloads
* Production databases
* Production storage
* Production networking

## Security

Contains:

* Vaults
* Keys
* Security monitoring
* Audit-related resources
* Security tooling

---

# Environment Separation

Do not place every environment inside one Compartment.

Bad structure:

```text
one-compartment
├── dev-instance
├── staging-instance
├── production-instance
├── dev-database
└── production-database
```

This makes policies harder to control.

Better:

```text
development
├── dev-instance
└── dev-database

staging
├── staging-instance
└── staging-database

production
├── prod-instance
└── prod-database
```

---

# Principle of Least Privilege

Least privilege means:

> Give a user only the permissions required to perform their job.

Not:

```text
Give everyone administrator access because it is easier.
```

Example:

A developer needs to restart a development Compute Instance.

The developer does not need to:

* Delete the production database
* Modify IAM Policies
* Delete VCNs
* Manage billing
* Disable security services
* Read every secret

---

# Bad Access Design

```text
Allow group devops-team
to manage all-resources
in tenancy
```

This gives extremely broad access.

The team may be able to:

* Delete production resources
* Modify networking
* Access sensitive storage
* Change databases
* Remove security controls
* Create costly resources

This should not be the default policy for a normal DevOps team.

---

# Better Access Design

```text
Allow group devops-team
to manage instance-family
in compartment development
```

```text
Allow group devops-team
to manage load-balancers
in compartment development
```

```text
Allow group devops-team
to use virtual-network-family
in compartment development
```

```text
Allow group devops-team
to manage volume-family
in compartment development
```

This gives the team broad control inside development but not across the entire tenancy.

---

# Separation of Duties

Separation of duties means dividing sensitive responsibilities between roles.

Example:

```text
DevOps Team
└── Manages Compute and deployments
```

```text
Network Admins
└── Manage VCN networking
```

```text
Security Team
└── Manage Vault, security tools, and policies
```

```text
Database Admins
└── Manage production databases
```

```text
Auditors
└── Read resources and logs
```

No single normal team should automatically control everything.

---

# Proposed Groups

Create the following Groups:

```text
devops-team
```

```text
devops-readonly
```

```text
network-admins
```

Optional:

```text
production-approvers
```

---

# DevOps Team Responsibilities

The `devops-team` Group may be responsible for:

* Creating Compute Instances
* Updating application servers
* Managing Block Volumes
* Managing Load Balancers
* Deploying applications
* Viewing logs
* Managing development resources
* Operating non-production infrastructure

It should not automatically manage:

* IAM users and Policies
* Production databases
* Security keys
* Billing
* Tenancy-wide resources

---

# Read-Only Team Responsibilities

The `devops-readonly` Group may:

* View Compute Instances
* View networking resources
* View Load Balancers
* Read configuration
* Review resource states
* Support troubleshooting

It should not:

* Create resources
* Delete resources
* Start or stop resources
* Change configuration
* Modify network rules

---

# Network Administrators

The `network-admins` Group may manage:

* VCNs
* Subnets
* Route Tables
* Gateways
* NSGs
* Security Lists
* Network peering
* Load Balancer networking dependencies

This role should be limited to authorized engineers.

---

# Suggested Policies

## DevOps Compute Access

```text
Allow group devops-team
to manage instance-family
in compartment development
```

## DevOps Block Volume Access

```text
Allow group devops-team
to manage volume-family
in compartment development
```

## DevOps Load Balancer Access

```text
Allow group devops-team
to manage load-balancers
in compartment development
```

## DevOps Network Usage

```text
Allow group devops-team
to use virtual-network-family
in compartment development
```

## Read-Only Access

```text
Allow group devops-readonly
to read all-resources
in compartment development
```

## Network Administrator Access

```text
Allow group network-admins
to manage virtual-network-family
in compartment development
```

---

# Why DevOps Uses but Does Not Manage Networking

A DevOps engineer may need to:

* Attach an instance to an existing subnet
* Use an existing NSG
* Select an existing VCN
* Deploy a Load Balancer into an approved subnet

The engineer may not need to:

* Delete the VCN
* Change the default route
* Remove the NAT Gateway
* Open unrestricted inbound access
* Delete production subnets

Therefore:

```text
use virtual-network-family
```

may be safer than:

```text
manage virtual-network-family
```

---

# Policy Design Example

```text
DevOps Team
├── Manage Compute
├── Manage Volumes
├── Manage Load Balancers
└── Use Networking
```

```text
Network Admins
└── Manage Networking
```

```text
Auditors
└── Read Resources
```

---

# Possible Policy File

Create a policy named:

```text
development-devops-access
```

Policy statements:

```text
Allow group devops-team to manage instance-family in compartment development
```

```text
Allow group devops-team to manage volume-family in compartment development
```

```text
Allow group devops-team to manage load-balancers in compartment development
```

```text
Allow group devops-team to use virtual-network-family in compartment development
```

```text
Allow group devops-readonly to read all-resources in compartment development
```

```text
Allow group network-admins to manage virtual-network-family in compartment development
```

---

# Parent and Child Compartments

Compartments may be nested.

Example:

```text
applications
├── development
├── staging
└── production
```

Policy scope must be considered carefully.

A policy applied at a parent level may affect child Compartments depending on the statement and resource hierarchy.

Always test the actual effective access.

Do not assume a policy affects only the visible parent folder.

---

# Tenancy-Level Policies

Policies can be scoped to the tenancy.

Example:

```text
Allow group auditors
to read all-resources
in tenancy
```

This gives read access across the tenancy.

That may be appropriate for authorized auditors, but it is broader than compartment-level access.

Use tenancy-wide policies only when required.

---

# Authentication vs Authorization

These are different concepts.

## Authentication

Proves who the user is.

Examples:

* Username and password
* MFA
* API key
* Federation
* Security token

## Authorization

Determines what the authenticated user may do.

Examples:

* Read Compute Instances
* Create a Block Volume
* Delete a Load Balancer
* Manage networking

Flow:

```text
User signs in
      │
      ▼
Authentication succeeds
      │
      ▼
IAM Policies are evaluated
      │
      ▼
Action allowed or denied
```

---

# MFA

MFA stands for Multi-Factor Authentication.

It requires more than one authentication factor.

Example:

```text
Password
   +
Authenticator Code
```

If a password is stolen, the attacker still needs the second factor.

MFA should be enabled for:

* Administrators
* DevOps engineers
* Security engineers
* Database administrators
* Users with production access
* Users who manage IAM

---

# Password Policy

A strong Identity Domain password policy should consider:

* Minimum password length
* Password complexity
* Password history
* Account lockout
* Password expiration where appropriate
* Recovery methods
* MFA enforcement

Passwords should not be shared between team members.

Every engineer should have an individual account.

---

# Shared Accounts Are a Bad Practice

Avoid:

```text
Username:
devops-admin
```

used by the entire team.

Problems include:

* No accountability
* Difficult auditing
* Password sharing
* Difficult offboarding
* Increased breach impact
* No clear ownership

Better:

```text
abdulrahman.devops
sara.devops
mohammad.devops
```

Each person receives access through Group membership.

---

# OCI Console Navigation

Console labels may change, but IAM resources are generally available under Identity and Security.

---

# Create a Compartment

```text
Navigation Menu
→ Identity & Security
→ Compartments
→ Create Compartment
```

Configure:

```text
Name:
development
```

```text
Description:
Development resources for the DevOps team
```

```text
Parent Compartment:
Root or approved parent Compartment
```

---

# Create a Group

```text
Navigation Menu
→ Identity & Security
→ Domains
→ Select Identity Domain
→ Groups
→ Create Group
```

Create:

```text
devops-team
```

```text
devops-readonly
```

```text
network-admins
```

---

# Create a User

```text
Navigation Menu
→ Identity & Security
→ Domains
→ Select Identity Domain
→ Users
→ Create User
```

Example:

```text
Username:
abdulrahman.devops
```

```text
Email:
USER_EMAIL
```

Create individual users for each team member.

---

# Add User to Group

Open the User or Group details.

Conceptual navigation:

```text
Identity Domain
→ Groups
→ devops-team
→ Add User to Group
```

Add:

```text
abdulrahman.devops
```

```text
sara.devops
```

Add the auditor to:

```text
devops-readonly
```

---

# Create a Policy

```text
Navigation Menu
→ Identity & Security
→ Policies
→ Create Policy
```

Configure:

```text
Name:
development-devops-access
```

```text
Compartment:
Appropriate policy location
```

Add the required policy statements.

---

# Policy Location vs Policy Target

A policy has a location where the policy object is stored.

The policy statements define where permissions apply.

These are related but not always the same concept.

Example statement:

```text
Allow group devops-team
to manage instance-family
in compartment development
```

The statement clearly targets the `development` Compartment.

Always review both:

* Where the Policy is created
* What resource scope the statement targets

---

# Create Initial DevOps Users

Suggested example:

```text
User:
abdulrahman.devops
Group:
devops-team
```

```text
User:
sara.devops
Group:
devops-team
```

```text
User:
omar.auditor
Group:
devops-readonly
```

---

# Initial Sign-In Process

A new user may receive:

* An invitation email
* A temporary password
* A password reset requirement
* Identity Domain sign-in details

The user should:

1. Open the invitation
2. Set a private password
3. Configure MFA
4. Sign in
5. Verify access
6. Report unexpected permissions

---

# Testing DevOps Access

Sign in as a member of `devops-team`.

The user should be able to:

```text
List Compute Instances in development
```

```text
Create a Compute Instance in development
```

```text
Start and stop development instances
```

```text
Create and attach Block Volumes
```

```text
Manage development Load Balancers
```

```text
Use approved development networking
```

The user should not be able to:

```text
Manage production resources
```

```text
Create IAM Policies
```

```text
Delete the production VCN
```

```text
Manage tenancy billing
```

---

# Testing Read-Only Access

Sign in as a member of `devops-readonly`.

The user should be able to:

* List resources
* Open resource details
* View states
* Read configuration

The user should not be able to:

* Create an instance
* Stop an instance
* Delete a volume
* Modify a Load Balancer
* Change NSG rules

---

# Testing Network Administrator Access

Sign in as a member of `network-admins`.

The user should be able to:

* Create a VCN
* Create subnets
* Configure Route Tables
* Manage gateways
* Manage NSGs
* Manage Security Lists

The user should not automatically be able to:

* Manage IAM
* Access production databases
* Manage billing
* Read sensitive Object Storage buckets

---

# Positive and Negative Testing

Do not test only what a user can do.

Also test what the user must not be able to do.

## Positive Test

```text
DevOps user can create a development Compute Instance.
```

## Negative Test

```text
DevOps user cannot delete a production database.
```

Both tests are necessary.

---

# Access Testing Matrix

| Action                       | DevOps Team | Read-Only |     Network Admin |
| ---------------------------- | ----------: | --------: | ----------------: |
| View development instances   |         Yes |       Yes | Depends on policy |
| Create development instances |         Yes |        No |                No |
| Stop development instances   |         Yes |        No |                No |
| Create Block Volumes         |         Yes |        No |                No |
| Manage Load Balancers        |         Yes |        No | Depends on policy |
| Use existing subnets         |         Yes |        No |               Yes |
| Modify Route Tables          |          No |        No |               Yes |
| Manage IAM Policies          |          No |        No |                No |
| Manage production resources  |          No |        No |                No |

---

# Permission Troubleshooting

When a user receives an authorization error, check the following:

```text
User
  ↓
Group Membership
  ↓
Policy Statement
  ↓
Resource Type
  ↓
Compartment Scope
  ↓
Requested Action
```

---

# Common Authorization Error Causes

## User Is Not in the Group

The Policy is correct, but the User is not a member of the Group.

Check:

```text
Identity Domain
→ Users
→ Select User
→ Groups
```

---

## Group Name Is Wrong

The Policy references:

```text
devop-team
```

but the actual Group is:

```text
devops-team
```

Policy names must match the intended identity.

---

## Wrong Compartment

The Policy allows access in:

```text
development
```

but the resource is inside:

```text
staging
```

The permission does not apply.

---

## Wrong Resource Family

The user needs to manage Load Balancers, but the policy only grants:

```text
manage instance-family
```

Compute permissions do not automatically grant Load Balancer permissions.

---

## Verb Is Too Limited

The policy grants:

```text
read instance-family
```

but the user tries to create an instance.

`read` does not allow creation.

---

## Policy Created in the Wrong Scope

The Policy may not be visible or effective from the intended hierarchy.

Review:

* Parent Compartment
* Child Compartment
* Tenancy scope
* Identity Domain
* Policy statement wording

---

## Policy Changes Have Not Propagated Yet

IAM changes may not always appear instantly.

After updating Group membership or a Policy:

1. Wait briefly
2. Sign out and sign in again if necessary
3. Retry the action
4. Recheck the Policy

---

# Common Beginner Mistakes

## Giving Everyone Administrator Access

This is easy but dangerous.

Bad:

```text
Manage all-resources in tenancy
```

Better:

```text
Manage only required resource families
in the required Compartment
```

---

## Creating Policies for Individual Users

Group-based access is easier to manage.

Bad:

```text
Special access for each individual user
```

Better:

```text
User → Group → Policy
```

---

## Mixing Development and Production

If both environments share one Compartment, access control becomes harder.

Separate them.

---

## Forgetting MFA

Password-only access is weaker.

Enable MFA for privileged users.

---

## Using Shared Accounts

Shared accounts remove accountability.

Use individual identities.

---

## Giving DevOps Full Network Administration

Application deployment access does not always require permission to delete VCNs or change critical routes.

Use `use` where sufficient.

---

## Giving Read-Only Users `manage`

Auditors normally need `read`, not `manage`.

---

## Never Testing Denied Actions

A policy may be broader than expected.

Test both allowed and denied operations.

---

# Offboarding Process

When a team member leaves:

1. Disable the User
2. Remove the User from Groups
3. Revoke active sessions
4. Remove API keys
5. Remove authentication tokens
6. Review credentials owned by the User
7. Reassign resources where necessary
8. Review Audit logs
9. Confirm the User cannot sign in

Do not simply stop sharing the password.

---

# API Keys

Users may need API keys for OCI CLI access.

An API key uses:

* Public key uploaded to OCI
* Private key stored by the User
* Fingerprint
* User OCID
* Tenancy OCID
* Region

The private key must be protected.

Never commit it to Git.

Add patterns such as:

```gitignore
*.pem
.oci/
```

---

# User API Keys vs Instance Principals

Use User API keys for:

* Developer workstations
* Personal CLI access
* Approved automation tied to a human identity

Use Instance Principals for:

* Compute workloads
* Server-side automation
* Backup scripts
* Applications running on OCI Compute

Workloads should not normally use a human User's private API key.

---

# CI/CD Access

CI/CD systems also need controlled access.

Possible methods include:

* Workload identity
* Resource principals
* OIDC federation
* Dedicated automation users
* Short-lived credentials
* Instance Principals when running on OCI Compute

Avoid storing long-lived administrator credentials in CI/CD secrets.

---

# Production Access Design

A stronger production model may use:

```text
Development:
DevOps Team can manage
```

```text
Staging:
DevOps Team can manage
```

```text
Production:
DevOps Team can read
```

```text
Production Changes:
Require approval or deployment automation
```

This reduces accidental manual production changes.

---

# Example Environment Policies

## Development

```text
Allow group devops-team
to manage instance-family
in compartment development
```

## Staging

```text
Allow group devops-team
to manage instance-family
in compartment staging
```

## Production

```text
Allow group devops-team
to read instance-family
in compartment production
```

Production deployments may be handled by a controlled automation identity.

---

# Break-Glass Account

A break-glass account is an emergency administrator identity.

It should:

* Be used only during emergencies
* Have strong MFA
* Have protected credentials
* Be monitored
* Trigger alerts when used
* Be reviewed after every use

It should not be the normal daily account.

---

# Audit Logging

OCI Audit records API activity.

Audit data can help answer:

```text
Who performed the action?
```

```text
What action was performed?
```

```text
Which resource was affected?
```

```text
When did it happen?
```

```text
Was the request successful?
```

Audit logs are important for:

* Incident investigation
* Security reviews
* Compliance
* Troubleshooting
* Accountability

---

# Monitoring IAM Changes

Sensitive IAM events include:

* User creation
* User deletion
* Group membership changes
* Policy creation
* Policy modification
* API key creation
* MFA changes
* Authentication failures
* Administrator access changes

Production environments should monitor these events.

---

# Security Improvements

A production IAM design should include:

* Individual user accounts
* MFA
* Strong password policies
* Group-based permissions
* Least privilege
* Compartment separation
* Separation of duties
* Audit logging
* Access reviews
* Automated offboarding
* Short-lived credentials
* Restricted production access
* Alerts for IAM changes
* Federation with an enterprise identity provider
* Emergency break-glass procedures

---

# Periodic Access Review

Access should be reviewed regularly.

Questions to ask:

```text
Does this User still work with the team?
```

```text
Does this User still need production access?
```

```text
Is this Group still required?
```

```text
Are the Policies broader than necessary?
```

```text
Are unused API keys still active?
```

```text
Is MFA enabled?
```

Possible review schedule:

```text
Privileged access:
Monthly
```

```text
General access:
Quarterly
```

The exact schedule depends on organizational requirements.

---

# Example Access Review Table

| User            | Group            | Access             | Still Required | Action             |
| --------------- | ---------------- | ------------------ | -------------- | ------------------ |
| Abdulrahman     | devops-team      | Development manage | Yes            | Keep               |
| Sara            | devops-team      | Development manage | Yes            | Keep               |
| Omar            | devops-readonly  | Development read   | No             | Remove             |
| Automation user | Deployment group | Production deploy  | Yes            | Rotate credentials |

---

# Policy Design Process

Before writing a Policy, answer:

1. Who needs access?
2. What exact action must they perform?
3. Which resource type is involved?
4. Which Compartment contains the resource?
5. Is `read` enough?
6. Is `use` enough?
7. Is `manage` really required?
8. Should the permission apply to production?
9. How will the access be tested?
10. How will it be reviewed later?

---

# Think Like a Cloud Engineer

Do not begin with:

```text
Which large permission will make the error disappear?
```

Begin with:

```text
What is the minimum permission required for this task?
```

For example:

A DevOps engineer cannot create a Compute Instance.

Do not immediately grant:

```text
manage all-resources in tenancy
```

Instead investigate:

```text
Does the user belong to the correct Group?
```

```text
Does the Group have instance-family permission?
```

```text
Can the Group use the selected subnet?
```

```text
Can the Group use the selected image?
```

```text
Is the resource being created in the correct Compartment?
```

---

# Build Order

Create the IAM design in this order:

1. Define the required team roles
2. Create the Compartment structure
3. Create the Identity Groups
4. Create individual Users
5. Add Users to the correct Groups
6. Enable MFA
7. Write least-privilege Policies
8. Create the Policies
9. Sign in as a DevOps User
10. Test allowed Compute operations
11. Test allowed storage operations
12. Test approved network usage
13. Test denied IAM operations
14. Test denied production operations
15. Sign in as a read-only User
16. Test read-only behavior
17. Sign in as a network administrator
18. Test networking operations
19. Review Audit events
20. Document the final access matrix

---

# Validation Checklist

```text
[ ] Development Compartment exists
[ ] DevOps Group exists
[ ] Read-only Group exists
[ ] Network Administrators Group exists
[ ] Every engineer has an individual User
[ ] Shared administrator accounts are not used
[ ] Users belong to the correct Groups
[ ] MFA is enabled for privileged Users
[ ] DevOps Policy is scoped to development
[ ] DevOps users can manage development Compute
[ ] DevOps users can manage development volumes
[ ] DevOps users can manage development Load Balancers
[ ] DevOps users can use approved networking
[ ] DevOps users cannot manage IAM
[ ] DevOps users cannot manage production
[ ] Read-only users can view resources
[ ] Read-only users cannot modify resources
[ ] Network administrators can manage networking
[ ] Network administrators do not automatically manage IAM
[ ] Positive access tests succeed
[ ] Negative access tests fail as expected
[ ] Audit logs show test operations
[ ] Access design is documented
```

---

# Failure Scenarios

## DevOps User Can Access Production

Possible causes:

* Policy uses `in tenancy`
* Production is under a parent Compartment with inherited broad access
* User belongs to another privileged Group
* A tenancy-wide Policy grants broader access

Investigate all effective Group memberships and Policies.

---

## DevOps User Cannot Create an Instance

Possible causes:

* Missing `instance-family` permission
* Missing permission to use the subnet
* Missing permission to use the image
* Wrong Compartment
* User not in the expected Group
* Policy statement typo
* Policy propagation delay

---

## Read-Only User Can Delete Resources

This means the User has access from another Group or Policy.

Review:

* All Group memberships
* Tenancy-level Policies
* Parent Compartment Policies
* Administrator Groups
* Federation mappings

---

## User Cannot Sign In

Possible causes:

* User is disabled
* Wrong Identity Domain
* Invitation not completed
* Password expired
* MFA issue
* Account locked
* Incorrect sign-in URL

Authentication failures are separate from authorization failures.

---

## Policy Appears Correct but Access Still Fails

Check:

```text
User
↓
Group
↓
Policy
↓
Verb
↓
Resource Type
↓
Compartment
↓
Dependent Resources
```

Creating one resource may require permissions for several connected resources.

---

# Dependent Permissions Example

Creating a Compute Instance may require access to:

* Compute Instances
* Images
* VCN
* Subnet
* VNIC
* Boot Volume
* Availability Domain information

Therefore, one `instance-family` Policy may not always be enough for every complete workflow.

This teaches an important lesson:

> Cloud actions often involve several connected services.

---

# Troubleshooting Authorization

## Step 1 - Confirm the User

Verify the exact username and Identity Domain.

## Step 2 - Confirm Group Membership

List every Group the User belongs to.

## Step 3 - Review Every Relevant Policy

Check:

* Policies in the target Compartment
* Policies in parent Compartments
* Tenancy-level Policies

## Step 4 - Confirm the Resource Compartment

The resource may not be where you think it is.

## Step 5 - Confirm the Required Verb

Determine whether the action needs:

```text
inspect
read
use
manage
```

## Step 6 - Confirm Dependent Permissions

Check networking, images, volumes, and related resources.

## Step 7 - Test a Small Allowed Action

For example:

```text
List instances
```

Then test:

```text
Create instance
```

This helps identify the missing permission level.

---

# Cleanup Order

IAM resources should be removed carefully.

1. Confirm the lab Users are not used elsewhere
2. Remove Users from Groups
3. Revoke API keys and tokens
4. Disable or delete temporary Users
5. Delete lab Policies
6. Delete lab Groups
7. Move or delete resources from the development Compartment
8. Delete the Compartment only when empty
9. Review Audit logs
10. Confirm no unexpected access remains

Do not delete a real employee identity just because it was used in a lab.

---

# What You Learned

After completing this scenario, you should understand:

* What OCI IAM is
* What Identity Domains are
* How Users, Groups, and Policies relate
* How a Policy statement is structured
* The difference between `inspect`, `read`, `use`, and `manage`
* What resource families are
* How Compartments control access scope
* Why environments should be separated
* What least privilege means
* Why Group-based access is better than individual access
* Why shared accounts are dangerous
* Why DevOps teams should not automatically receive tenancy administrator access
* How to separate DevOps, networking, security, and audit responsibilities
* Why MFA is important
* How to test both allowed and denied actions
* How to troubleshoot authorization errors
* Why one cloud action may require permissions across multiple services
* How Audit logs support accountability
* How to perform access reviews and offboarding

---

# Main Relationship to Remember

```text
User
  │
  ▼
Group
  │
  ▼
IAM Policy
  │
  ▼
Compartment
  │
  ▼
OCI Resources
```

Authentication answers:

```text
Who are you?
```

Authorization answers:

```text
What are you allowed to do?
```

The safest design is:

```text
Individual User
      │
      ▼
Role-Based Group
      │
      ▼
Least-Privilege Policy
      │
      ▼
Specific Compartment
```

Avoid:

```text
Everyone
   │
   ▼
Manage all-resources
   │
   ▼
Entire Tenancy
```

---

# Next Scenario

Scenario 09:

```text
Terraform Deploy Web Infrastructure
```

The next scenario will deploy OCI infrastructure using Terraform.

```text
Terraform
    │
    ▼
OCI Provider
    │
    ▼
VCN
    │
    ├── Subnet
    ├── Internet Gateway
    ├── Route Table
    ├── Security Rules
    └── Compute Instance
```

We will explain:

* OCI Provider authentication
* Terraform files
* Variables
* Data sources
* Networking resources
* Compute resources
* Outputs
* State
* Planning
* Applying
* Destroying
* Dependency relationships
