# Scenario 05 - Private Instance with a NAT Gateway

## Goal

In this scenario, we will create a private Compute Instance that can access the Internet without having a public IP address.

The instance will use a NAT Gateway for outbound Internet access.

This allows the server to:

* Install operating system updates
* Download packages
* Pull application dependencies
* Connect to external APIs
* Download files from the Internet

At the same time, Internet users will not be able to start a direct connection to the private instance.

---

# Final Architecture

```text
                    Internet
                        ▲
                        │
                 Outbound Traffic
                        │
                  NAT Gateway
                        ▲
                        │
                  Route Table
                        ▲
                        │
                 Private Subnet
                        ▲
                        │
              Private Compute Instance
                   No Public IP
```

Administrative access:

```text
Administrator
      │
      ▼
  OCI Bastion
      │
      ▼
Private Compute Instance
```

---

# What We Want to Build

We will create:

* One Compartment
* One VCN
* One private subnet
* One NAT Gateway
* One private Route Table
* One Network Security Group
* One private Compute Instance
* No public IP address
* Optional OCI Bastion access

The private instance should be able to run:

```bash
sudo apt update
```

It should also be able to reach an external website:

```bash
curl https://example.com
```

However, the instance should not be directly reachable from the Internet.

---

# Why Use a Private Instance?

A public Compute Instance normally has a public IP address.

```text
Internet
   │
   ▼
Public IP
   │
   ▼
Compute Instance
```

This makes direct Internet communication possible.

A private Compute Instance has only a private IP address.

```text
Private IP
   │
   ▼
Compute Instance
```

A private IP can be used only inside private networks such as:

* The same VCN
* A peered VCN
* A VPN-connected network
* A FastConnect-connected network
* A Bastion session

The private instance is not directly exposed to Internet users.

---

# Public IP vs Private IP

| Feature                         | Public IP         | Private IP |
| ------------------------------- | ----------------- | ---------- |
| Reachable from the Internet     | Yes, when allowed | No         |
| Used inside the VCN             | Yes               | Yes        |
| Exposes the resource publicly   | Potentially       | No         |
| Needed for direct public SSH    | Usually yes       | No         |
| Recommended for backend servers | Usually no        | Yes        |

---

# What Is a NAT Gateway?

NAT stands for Network Address Translation.

A NAT Gateway allows private resources to start outbound connections to the Internet.

```text
Private Instance
      │
      ▼
NAT Gateway
      │
      ▼
Internet
```

The response returns through the same NAT Gateway.

```text
Internet Response
       │
       ▼
NAT Gateway
       │
       ▼
Private Instance
```

The important rule is:

> The private instance starts the connection.

Internet users cannot use the NAT Gateway to start a new direct connection to the private instance.

---

# What NAT Gateway Does

The NAT Gateway supports outbound communication.

Examples:

```text
Private Instance → Ubuntu Package Repository
Private Instance → GitHub
Private Instance → Docker Registry
Private Instance → External API
Private Instance → Public Website
```

---

# What NAT Gateway Does Not Do

The NAT Gateway does not make the private instance publicly reachable.

It does not allow:

```text
Internet User → SSH → Private Instance
```

It does not allow:

```text
Internet User → HTTP → Private Instance
```

It does not assign a public IP address to the Compute Instance.

---

# Internet Gateway vs NAT Gateway

| Feature                     | Internet Gateway               | NAT Gateway                      |
| --------------------------- | ------------------------------ | -------------------------------- |
| Used by                     | Public resources               | Private resources                |
| Allows outbound traffic     | Yes                            | Yes                              |
| Allows inbound traffic      | Yes, when security rules allow | No new inbound connections       |
| Requires instance public IP | Usually yes                    | No                               |
| Typical subnet              | Public subnet                  | Private subnet                   |
| Main purpose                | Public Internet connectivity   | Private outbound Internet access |

---

# Service Gateway vs NAT Gateway

A Service Gateway allows private resources to reach supported Oracle services without sending traffic through the public Internet.

Examples include:

* Object Storage
* Some Oracle platform services

```text
Private Instance
      │
      ▼
Service Gateway
      │
      ▼
Oracle Services Network
```

A NAT Gateway is used for general Internet destinations.

```text
Private Instance
      │
      ▼
NAT Gateway
      │
      ▼
Public Internet
```

Use:

```text
Object Storage → Service Gateway
General Internet → NAT Gateway
```

---

# OCI Services Used

| Service                | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| Compartment            | Organize resources                       |
| VCN                    | Provide the private network              |
| Private Subnet         | Host the private Compute Instance        |
| NAT Gateway            | Provide outbound Internet access         |
| Route Table            | Send Internet traffic to the NAT Gateway |
| Network Security Group | Control instance traffic                 |
| Compute Instance       | Run the private server                   |
| OCI Bastion            | Provide controlled administrative access |
| DNS                    | Resolve domain names                     |

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
Private Compute Instance:
10.0.2.10
```

The exact private IP address may be assigned automatically by OCI.

---

# Resource Relationships

```text
Compartment
    │
    ▼
VCN
    │
    ├── NAT Gateway
    │
    ├── Private Route Table
    │       │
    │       └── 0.0.0.0/0 → NAT Gateway
    │
    ├── Private Subnet
    │       │
    │       ├── Private Route Table
    │       ├── Instance NSG
    │       └── Private Compute Instance
    │
    └── Optional Bastion
            │
            └── Administrative Access
```

---

# Main Dependency Chain

```text
VCN
  ↓
NAT Gateway
  ↓
Route Table
  ↓
Private Subnet
  ↓
Private Compute Instance
```

Creating the NAT Gateway alone is not enough.

The subnet must use a Route Table that sends Internet traffic to the NAT Gateway.

---

# Route Table Configuration

The private subnet needs a default route.

```text
Destination Type:
CIDR Block
```

```text
Destination CIDR:
0.0.0.0/0
```

```text
Target Type:
NAT Gateway
```

```text
Target:
private-nat-gateway
```

The complete route is:

```text
0.0.0.0/0 → NAT Gateway
```

This means:

> Send traffic for destinations outside the VCN through the NAT Gateway.

---

# Local VCN Traffic

Traffic between resources in the same VCN does not need the NAT Gateway.

Example:

```text
10.0.2.10 → 10.0.3.20
```

This traffic stays inside the VCN.

The NAT Gateway is used when the destination is outside the private network.

Example:

```text
10.0.2.10 → 8.8.8.8
```

---

# Private Subnet Configuration

When creating the subnet:

* Select the correct VCN
* Use a private CIDR range
* Select the private Route Table
* Do not allow public IPv4 addresses on VNICs
* Attach the appropriate Security List or NSG

Recommended setting:

```text
Prohibit public IP addresses on VNICs:
Enabled
```

This helps prevent accidental public exposure.

---

# Network Security Group

Create:

```text
private-instance-nsg
```

The required rules depend on what the server needs to do.

---

# Egress Rules

For a simple learning lab, allow outbound traffic.

```text
Destination:
0.0.0.0/0

Protocol:
All protocols
```

A more restrictive production design may allow only specific protocols.

For example:

## HTTPS

```text
Destination:
0.0.0.0/0

Protocol:
TCP

Destination Port:
443
```

## HTTP

```text
Destination:
0.0.0.0/0

Protocol:
TCP

Destination Port:
80
```

## DNS

```text
Protocol:
UDP

Destination Port:
53
```

DNS behavior also depends on the configured resolver.

---

# Ingress Rules

The private instance does not need a general Internet ingress rule.

Do not create:

```text
Source:
0.0.0.0/0

Port:
22
```

The instance has no public IP address, but unrestricted rules are still poor security practice.

Administrative access should come from a trusted private source.

Examples:

* OCI Bastion
* Another trusted NSG
* A VPN network
* A management subnet

---

# Optional SSH Rule for Bastion

Allow SSH only from the Bastion or trusted management source.

Example:

```text
Source Type:
Network Security Group

Source:
bastion-nsg

Protocol:
TCP

Destination Port:
22
```

Or use the exact private CIDR required by your administration design.

---

# Outbound Traffic Flow

When the private instance runs:

```bash
sudo apt update
```

The traffic flow is:

```text
1. The instance resolves the repository domain name.
2. The instance sends traffic to the private subnet Route Table.
3. The Route Table matches the destination 0.0.0.0/0.
4. The traffic is sent to the NAT Gateway.
5. The NAT Gateway translates the private source address.
6. The request reaches the Internet.
7. The response returns to the NAT Gateway.
8. The NAT Gateway forwards the response to the private instance.
```

Architecture:

```text
Private Instance
      │
      ▼
Private Route Table
      │
      ▼
NAT Gateway
      │
      ▼
Internet Repository
```

---

# Why the Instance Does Not Need a Public IP

The Compute Instance uses its private IP inside the VCN.

The NAT Gateway performs address translation for outbound connections.

From the instance perspective:

```text
Source:
10.0.2.10
```

The NAT Gateway translates the connection before sending it to the Internet.

The public destination sees the connection coming from the NAT service, not directly from the instance's private IP address.

---

# Build Order

Create resources in this order:

1. Create the Compartment
2. Create the VCN
3. Create the NAT Gateway
4. Create the private Route Table
5. Add the default route to the NAT Gateway
6. Create the private subnet
7. Prohibit public IP addresses in the subnet
8. Create the private instance NSG
9. Configure required egress rules
10. Create the private Compute Instance
11. Confirm that no public IP was assigned
12. Configure administrative access
13. Connect to the instance
14. Test DNS resolution
15. Test outbound HTTP and HTTPS
16. Install packages
17. Verify that inbound Internet access is unavailable
18. Review logs and network rules
19. Clean up the resources

---

# OCI Console Navigation

Console labels may change over time, but these resources are generally available through the following locations.

## Create the VCN

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Create VCN
```

---

## Create the NAT Gateway

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ NAT Gateways
→ Create NAT Gateway
```

Suggested name:

```text
private-nat-gateway
```

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

Suggested name:

```text
private-route-table
```

Add:

```text
0.0.0.0/0 → private-nat-gateway
```

---

## Create the Private Subnet

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Subnets
→ Create Subnet
```

Configure:

```text
Name:
private-subnet
```

```text
CIDR:
10.0.2.0/24
```

```text
Route Table:
private-route-table
```

```text
Public IPv4 addresses:
Prohibited
```

---

## Create the Network Security Group

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Network Security Groups
→ Create Network Security Group
```

Suggested name:

```text
private-instance-nsg
```

---

## Create the Compute Instance

```text
Navigation Menu
→ Compute
→ Instances
→ Create Instance
```

Configure:

* Select the correct Compartment
* Select Ubuntu or Oracle Linux
* Select the scenario VCN
* Select the private subnet
* Do not assign a public IPv4 address
* Attach `private-instance-nsg`
* Add your SSH public key

---

# Confirm the Instance Is Private

Open the instance details and verify:

```text
Public IPv4 Address:
Not Assigned
```

The instance should still have a private address.

Example:

```text
Private IPv4 Address:
10.0.2.10
```

---

# How to Access the Private Instance

Since the instance has no public IP address, this will not work directly from your laptop:

```bash
ssh ubuntu@10.0.2.10
```

Your laptop is not normally inside the OCI VCN.

You need a private access method.

---

# Option 1 - OCI Bastion

OCI Bastion provides controlled and temporary access to private resources.

Architecture:

```text
Your Computer
      │
      ▼
OCI Bastion
      │
      ▼
Private Compute Instance
```

General steps:

1. Create a Bastion in the same VCN
2. Create a session
3. Select the target private instance
4. Configure the SSH public key
5. Use the generated SSH command
6. Connect before the session expires

Bastion sessions are temporary, which is safer than permanently exposing SSH.

---

# Option 2 - Jump Server

A jump server is a public management server.

```text
Your Computer
      │
      ▼
Public Jump Server
      │
      ▼
Private Instance
```

This works, but the jump server must be secured carefully.

For learning, OCI Bastion is usually cleaner.

---

# Option 3 - VPN or FastConnect

A VPN connects your local or company network to OCI.

```text
Local Network
      │
      ▼
VPN
      │
      ▼
OCI VCN
      │
      ▼
Private Instance
```

This is common in enterprise environments.

---

# Validation

After connecting to the private instance, verify its network configuration.

## Show IP Addresses

```bash
ip addr
```

The instance should show a private address such as:

```text
10.0.2.10
```

---

## Check the Route

```bash
ip route
```

The operating system normally sends traffic to the subnet gateway.

OCI's VCN Route Table then decides whether traffic uses the NAT Gateway.

---

## Test DNS

```bash
getent hosts example.com
```

Or:

```bash
nslookup example.com
```

If `nslookup` is unavailable:

```bash
sudo apt install dnsutils -y
```

---

## Test HTTPS

```bash
curl -I https://example.com
```

Expected result includes an HTTP response such as:

```text
HTTP/2 200
```

---

## Test Public IP Visibility

Run:

```bash
curl https://ifconfig.me
```

The returned address will not be a public IP assigned directly to the instance.

The connection exits through the NAT Gateway.

---

## Install Packages

Ubuntu:

```bash
sudo apt update
sudo apt install nginx -y
```

Oracle Linux:

```bash
sudo dnf update -y
sudo dnf install nginx -y
```

Successful package installation confirms that outbound Internet access works.

---

# Testing What the NAT Gateway Allows

The private server should be able to initiate outbound traffic.

Examples:

```bash
curl https://example.com
```

```bash
git clone https://github.com/example/example.git
```

```bash
sudo apt update
```

```bash
pip install flask
```

---

# Testing What the NAT Gateway Blocks

From your local machine, you should not be able to connect directly using the private IP:

```bash
ssh ubuntu@10.0.2.10
```

This normally fails because the private IP is not routable from the public Internet.

There is also no public IP to use:

```bash
ssh ubuntu@PUBLIC_IP
```

No `PUBLIC_IP` should exist.

---

# Validation Checklist

```text
[ ] The VCN exists
[ ] The NAT Gateway exists
[ ] The NAT Gateway is available
[ ] The private Route Table exists
[ ] The Route Table contains 0.0.0.0/0 → NAT Gateway
[ ] The private subnet uses the correct Route Table
[ ] Public IP addresses are prohibited in the subnet
[ ] The Compute Instance has a private IP
[ ] The Compute Instance has no public IP
[ ] The NSG allows required outbound traffic
[ ] DNS resolution works
[ ] HTTPS connections work
[ ] Package installation works
[ ] The instance cannot be accessed directly from the Internet
[ ] Administrative access uses Bastion, VPN, or another trusted method
```

---

# Common Beginner Mistakes

## NAT Gateway Exists but Internet Access Does Not Work

Creating the NAT Gateway is not enough.

The private subnet Route Table must include:

```text
0.0.0.0/0 → NAT Gateway
```

Also verify that the subnet is actually associated with that Route Table.

---

## The Subnet Uses the Wrong Route Table

A VCN may contain multiple Route Tables.

The private subnet may accidentally use:

* The default Route Table
* A public Route Table
* A Route Table with no NAT rule

Open the subnet details and confirm its Route Table association.

---

## The Instance Has a Public IP

This breaks the main goal of the scenario.

Verify:

```text
Public IPv4 Address:
Not Assigned
```

Also prohibit public IP addresses at the subnet level.

---

## Egress Rules Block Traffic

The route may be correct, but the NSG or Security List may block outbound connections.

Check:

* TCP port 443 for HTTPS
* TCP port 80 for HTTP
* DNS traffic
* Required package repository traffic

---

## DNS Does Not Work

You may be able to reach an IP address but not a domain name.

Test:

```bash
curl -I https://1.1.1.1
```

Then test:

```bash
getent hosts example.com
```

If IP connectivity works but names fail, investigate DNS configuration.

---

## Trying to SSH Directly from the Internet

This command will not normally work:

```bash
ssh ubuntu@10.0.2.10
```

Use:

* OCI Bastion
* VPN
* Jump server
* Instance Console Connection where appropriate

---

## Using an Internet Gateway for the Private Subnet

A route to an Internet Gateway does not automatically make a private instance work without a public IP.

For private outbound access, use:

```text
0.0.0.0/0 → NAT Gateway
```

---

## Adding Port 22 from Everywhere

Do not create an unrestricted SSH rule:

```text
0.0.0.0/0 → TCP 22
```

The private instance should accept SSH only from a trusted private source.

---

# Troubleshooting Process

Use this order when outbound Internet access fails.

## Step 1 - Check the Instance

Verify:

```bash
ip addr
ip route
```

Confirm that the operating system network interface is active.

---

## Step 2 - Check DNS

```bash
getent hosts example.com
```

---

## Step 3 - Check the Subnet

Confirm:

* It is the intended private subnet
* It uses the private Route Table
* Public IP addresses are prohibited

---

## Step 4 - Check the Route Table

Confirm:

```text
Destination:
0.0.0.0/0

Target:
NAT Gateway
```

---

## Step 5 - Check the NAT Gateway

Confirm that the NAT Gateway:

* Exists
* Is in the same VCN
* Is available
* Has not been deleted or disabled

---

## Step 6 - Check Security Rules

Confirm that outbound traffic is permitted.

---

## Step 7 - Test by IP and Domain

Test IP connectivity:

```bash
curl -I https://1.1.1.1
```

Test DNS-based connectivity:

```bash
curl -I https://example.com
```

This helps separate routing problems from DNS problems.

---

# Security Benefits

This architecture reduces exposure because:

* The instance has no public IP
* The Internet cannot start direct connections
* SSH does not need to be publicly exposed
* Administrative access can be temporary
* Outbound access is controlled through one networking service
* Network rules can restrict destinations and protocols

---

# Security Limitations

A NAT Gateway does not inspect application traffic like a firewall.

It does not automatically protect against:

* Malicious downloads
* Compromised package repositories
* Data exfiltration
* Unsafe external APIs
* Malware contacting external servers
* Excessively broad egress rules

For stronger controls, consider:

* OCI Network Firewall
* Proxy servers
* Restricted egress rules
* Service Gateway
* DNS filtering
* Logging and monitoring
* Vulnerability scanning

---

# Cost Considerations

NAT Gateway usage may generate network-related charges depending on OCI pricing and traffic volume.

To reduce unnecessary Internet traffic:

* Use a Service Gateway for supported OCI services
* Avoid repeated large downloads
* Cache dependencies
* Remove unused resources
* Monitor outbound traffic
* Review current OCI pricing before production use

---

# Production Improvements

A production design may include:

* Multiple private subnets
* OCI Bastion
* VPN or FastConnect
* Service Gateway
* Network Firewall
* Restricted egress rules
* Flow Logs
* Monitoring
* Alarms
* Centralized logging
* Automated patching
* Vulnerability scanning
* Terraform
* Configuration management

Improved architecture:

```text
Private Compute Instance
          │
          ├── Service Gateway → OCI Services
          │
          └── Network Firewall
                    │
                    ▼
                NAT Gateway
                    │
                    ▼
                 Internet
```

---

# Failure Scenarios

## NAT Gateway Is Removed

```text
Private Instance: Running
NAT Gateway: Missing
Internet Access: Unavailable
```

Private VCN communication may still work, but general outbound Internet access fails.

---

## Default Route Is Removed

```text
NAT Gateway: Available
Route Table: Missing 0.0.0.0/0 rule
Internet Access: Unavailable
```

The NAT Gateway exists, but no traffic is sent to it.

---

## DNS Fails

```text
IP Connectivity: Working
Domain Names: Failing
```

Applications using domain names may stop working even though routing is correct.

---

## Egress Rule Is Removed

```text
Route Table: Correct
NAT Gateway: Available
NSG Egress: Blocked
Internet Access: Unavailable
```

Routing and security rules must both allow the connection.

---

# Cleanup Order

Delete resources in this order:

1. Terminate the private Compute Instance
2. Delete Bastion sessions
3. Delete the Bastion if it was created for this lab
4. Delete the private instance NSG
5. Delete the private subnet
6. Delete the private Route Table
7. Delete the NAT Gateway
8. Delete the VCN
9. Delete the Compartment if it is empty

A subnet cannot be deleted while active resources remain inside it.

---

# What You Learned

After completing this scenario, you should understand:

* What a private Compute Instance is
* Why private instances should not have public IP addresses
* What a NAT Gateway does
* What a NAT Gateway does not do
* The difference between an Internet Gateway and a NAT Gateway
* The difference between a NAT Gateway and a Service Gateway
* Why a Route Table is required
* How outbound Internet traffic leaves a private subnet
* Why the instance can download packages without being public
* Why SSH requires Bastion, VPN, or another private access method
* How NSGs and Route Tables work together
* How to troubleshoot private outbound connectivity

---

# Main Relationship to Remember

```text
Private Compute Instance
          │
          ▼
Private Subnet
          │
          ▼
Route Table
          │
          ▼
NAT Gateway
          │
          ▼
Internet
```

The most important rule is:

```text
0.0.0.0/0 → NAT Gateway
```

The security principle is:

```text
Outbound Internet access
without direct inbound Internet exposure
```

---

# Next Scenario

Scenario 06:

```text
Object Storage Backup
```

The next scenario will show how an application or Compute Instance can store backups inside OCI Object Storage.

```text
Compute Instance
      │
      ▼
Backup File
      │
      ▼
Service Gateway
      │
      ▼
OCI Object Storage
```
