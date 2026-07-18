# Scenario 02 - Private Backend with a Public Load Balancer

## Goal

In this scenario, we will deploy a public Load Balancer that receives traffic from the Internet and forwards it to Compute Instances located inside a private subnet.

The Compute Instances will not have public IP addresses.

Users will access the application through the Load Balancer public IP only.

This is safer than exposing every Compute Instance directly to the Internet.

---

# Final Architecture

```text
                         Internet
                             │
                             ▼
                  Public Load Balancer
                      Public Subnet
                             │
                             ▼
                         Listener
                         TCP Port 80
                             │
                             ▼
                        Backend Set
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        Compute Instance 01      Compute Instance 02
            Private Subnet           Private Subnet
                 │                       │
                 ▼                       ▼
               Nginx                   Nginx
```

For outbound Internet access from the private instances:

```text
Private Compute Instances
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

---

# What We Want to Build

We want to create:

* One VCN
* One public subnet for the Load Balancer
* One private subnet for the backend servers
* One Internet Gateway
* One NAT Gateway
* One public Load Balancer
* Two private Compute Instances
* One Listener
* One Backend Set
* One Health Check
* Network Security Groups
* Nginx on both backend servers

The application will be accessed using:

```text
http://LOAD_BALANCER_PUBLIC_IP
```

The backend instances will not be accessed directly from the Internet.

---

# Why This Architecture Is Better

In the previous scenario, the Compute Instance had a public IP.

That architecture is useful for learning, but it is not ideal for a production application.

In this scenario:

```text
Internet users
      │
      ▼
Load Balancer
      │
      ▼
Private Compute Instances
```

Only the Load Balancer is public.

The backend servers remain private.

This reduces the attack surface because users cannot connect directly to the application servers.

---

# OCI Services Used

| Service                 | Purpose                                                 |
| ----------------------- | ------------------------------------------------------- |
| Compartment             | Organize the resources                                  |
| VCN                     | Provide the private cloud network                       |
| Public Subnet           | Host the public Load Balancer                           |
| Private Subnet          | Host the backend Compute Instances                      |
| Internet Gateway        | Allow Internet traffic to reach the Load Balancer       |
| NAT Gateway             | Allow private instances to access the Internet outbound |
| Route Tables            | Control traffic paths                                   |
| Network Security Groups | Control traffic between resources                       |
| Load Balancer           | Receive and distribute incoming traffic                 |
| Listener                | Accept traffic on a specific port                       |
| Backend Set             | Group backend servers                                   |
| Health Check            | Verify that backend servers are healthy                 |
| Compute Instances       | Run the application                                     |
| Nginx                   | Serve the website                                       |

---

# Main Architecture Decision

The most important decision in this scenario is separating public and private resources.

## Public Resources

The Load Balancer is public because Internet users must reach it.

It is placed inside a public subnet.

```text
Internet
   │
   ▼
Public Load Balancer
```

## Private Resources

The Compute Instances do not need public IP addresses.

They only need to receive traffic from the Load Balancer.

They are placed inside a private subnet.

```text
Load Balancer
   │
   ▼
Private Compute Instances
```

---

# Public Subnet

The public subnet will contain the Load Balancer.

It needs a route to the Internet Gateway.

Example route rule:

```text
Destination CIDR Block: 0.0.0.0/0
Target Type: Internet Gateway
Target: public-internet-gateway
```

This route allows the public Load Balancer to communicate with the Internet.

---

# Private Subnet

The private subnet will contain the backend Compute Instances.

The instances will not have public IP addresses.

They can receive traffic from the Load Balancer through the VCN's private network.

For outbound Internet access, the private subnet uses a NAT Gateway.

Example route rule:

```text
Destination CIDR Block: 0.0.0.0/0
Target Type: NAT Gateway
Target: private-nat-gateway
```

---

# Why Do Private Instances Need a NAT Gateway?

The backend servers may need Internet access to:

* Download operating system updates
* Install Nginx
* Download packages
* Contact external APIs
* Pull application dependencies

However, they should not accept connections directly from the Internet.

The NAT Gateway provides outbound-only Internet access.

```text
Private Instance
      │
      ▼
NAT Gateway
      │
      ▼
Internet
```

Internet users cannot start a connection through the NAT Gateway to reach the private instance.

---

# Internet Gateway vs NAT Gateway

| Feature                   | Internet Gateway             | NAT Gateway                      |
| ------------------------- | ---------------------------- | -------------------------------- |
| Used by                   | Public resources             | Private resources                |
| Supports inbound traffic  | Yes                          | No                               |
| Supports outbound traffic | Yes                          | Yes                              |
| Requires public IP        | Usually yes                  | No public IP on the instance     |
| Main purpose              | Public Internet connectivity | Private outbound Internet access |

The Load Balancer uses the Internet Gateway.

The backend instances use the NAT Gateway.

---

# Load Balancer Components

A Load Balancer is not only one resource.

It contains several connected components.

```text
Load Balancer
    │
    ├── Listener
    │
    ├── Backend Set
    │
    ├── Backend Servers
    │
    └── Health Check
```

---

# Listener

The Listener accepts incoming requests on a specific protocol and port.

For this scenario:

```text
Protocol: HTTP
Port: 80
```

The Listener receives requests from users and sends them to the Backend Set.

```text
User Request
     │
     ▼
Listener on Port 80
```

---

# Backend Set

The Backend Set is a logical group of backend servers.

It contains:

* Backend servers
* Load balancing policy
* Health check configuration
* Session persistence settings

Example:

```text
Backend Set: web-backend-set
Policy: Round Robin
```

---

# Backend Servers

The backend servers are the private Compute Instances running Nginx.

Example:

```text
Backend 01
Private IP: 10.0.2.10
Port: 80
```

```text
Backend 02
Private IP: 10.0.2.11
Port: 80
```

The Load Balancer connects to the private IP addresses, not public IP addresses.

---

# Health Check

The Load Balancer continuously checks whether each backend server is healthy.

Example health check:

```text
Protocol: HTTP
Port: 80
URL Path: /
Expected Status Code: 200
```

The Load Balancer may send a request similar to:

```text
GET /
```

If the backend responds successfully, it is marked healthy.

If it fails repeatedly, it is marked unhealthy.

```text
Healthy Backend
      │
      ▼
Receives Traffic
```

```text
Unhealthy Backend
      │
      ▼
Removed from Traffic Distribution
```

---

# Load Balancing Policy

For this scenario, we can use Round Robin.

```text
Request 1 → Backend 01
Request 2 → Backend 02
Request 3 → Backend 01
Request 4 → Backend 02
```

Round Robin distributes requests between the available healthy backend servers.

---

# Resource Relationships

```text
Compartment
    │
    ▼
VCN
    │
    ├── Public Subnet
    │       │
    │       ├── Internet Gateway Route
    │       │
    │       └── Public Load Balancer
    │               │
    │               ├── Listener
    │               ├── Backend Set
    │               └── Health Check
    │
    └── Private Subnet
            │
            ├── NAT Gateway Route
            │
            ├── Compute Instance 01
            │
            └── Compute Instance 02
```

---

# Network Security Design

We should not allow traffic from everywhere to every resource.

Each resource should only accept the traffic it needs.

For this scenario, using Network Security Groups is clearer than placing every rule inside the subnet Security List.

We can create:

```text
load-balancer-nsg
backend-servers-nsg
```

---

# Load Balancer NSG Rules

## Ingress Rule

Allow users from the Internet to access the Load Balancer.

```text
Source: 0.0.0.0/0
Protocol: TCP
Destination Port: 80
```

For HTTPS later:

```text
Source: 0.0.0.0/0
Protocol: TCP
Destination Port: 443
```

## Egress Rule

Allow the Load Balancer to connect to the backend servers.

```text
Destination: backend-servers-nsg
Protocol: TCP
Destination Port: 80
```

---

# Backend Servers NSG Rules

## Ingress Rule

Allow HTTP traffic only from the Load Balancer NSG.

```text
Source Type: Network Security Group
Source: load-balancer-nsg
Protocol: TCP
Destination Port: 80
```

Do not use this rule:

```text
Source: 0.0.0.0/0
Port: 80
```

The backend servers should accept application traffic only from the Load Balancer.

## SSH Rule

For a production architecture, do not expose SSH directly to the Internet.

Possible administration methods include:

* OCI Bastion
* A management instance
* VPN
* OCI Cloud Shell with proper private access
* Configuration management tools

For a beginner lab, use a controlled method instead of assigning public IP addresses to the backend servers.

---

# Traffic Flow

When a user opens the website:

```text
1. The user sends an HTTP request.

2. The request reaches the Load Balancer public IP.

3. The Internet Gateway allows the request into the VCN.

4. The Load Balancer Listener accepts the request on port 80.

5. The Listener forwards the request to the Backend Set.

6. The Backend Set selects a healthy backend server.

7. The Load Balancer connects to the server's private IP.

8. Nginx processes the request.

9. The response returns through the Load Balancer.

10. The Load Balancer sends the response to the user.
```

Architecture flow:

```text
Browser
   │
   ▼
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Public Load Balancer
   │
   ▼
Listener
   │
   ▼
Backend Set
   │
   ▼
Healthy Private Compute Instance
   │
   ▼
Nginx
```

---

# Build Order

Create the resources in this order:

1. Create the Compartment
2. Create the VCN
3. Create the Internet Gateway
4. Create the NAT Gateway
5. Create the public route table
6. Create the private route table
7. Create the public subnet
8. Create the private subnet
9. Create the Load Balancer NSG
10. Create the backend servers NSG
11. Create the two private Compute Instances
12. Install Nginx on both instances
13. Create the public Load Balancer
14. Create the Backend Set
15. Configure the Health Check
16. Add the backend servers
17. Create the HTTP Listener
18. Validate backend health
19. Open the Load Balancer public IP
20. Test traffic distribution

The Load Balancer should be created after the networking foundation and backend servers are ready.

---

# Suggested IP Address Plan

Example CIDR ranges:

```text
VCN CIDR:
10.0.0.0/16
```

```text
Public Subnet:
10.0.1.0/24
```

```text
Private Subnet:
10.0.2.0/24
```

Possible private IP addresses:

```text
Backend 01:
10.0.2.10
```

```text
Backend 02:
10.0.2.11
```

The exact addresses may be assigned automatically by OCI.

---

# OCI Console Navigation

The exact labels may change as the OCI Console is updated, but the resources are generally available through the following sections.

## Create the VCN

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Create VCN
```

---

## Create the Internet Gateway

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Internet Gateways
→ Create Internet Gateway
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

---

## Create Route Tables

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Route Tables
→ Create Route Table
```

Create one route table for the public subnet and another for the private subnet.

---

## Create Subnets

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Subnets
→ Create Subnet
```

Create:

```text
public-load-balancer-subnet
```

and:

```text
private-backend-subnet
```

---

## Create Network Security Groups

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Select the VCN
→ Network Security Groups
→ Create Network Security Group
```

Create:

```text
load-balancer-nsg
```

and:

```text
backend-servers-nsg
```

---

## Create Compute Instances

```text
Navigation Menu
→ Compute
→ Instances
→ Create Instance
```

For each instance:

* Select the private subnet
* Do not assign a public IPv4 address
* Attach the backend servers NSG
* Use an Ubuntu image
* Add your SSH key if required

---

## Create the Load Balancer

```text
Navigation Menu
→ Networking
→ Load Balancers
→ Create Load Balancer
```

Choose:

* Public visibility
* Flexible shape
* Public subnet
* Load Balancer NSG

---

# Installing Nginx

The private instances need outbound Internet access through the NAT Gateway.

On Backend 01:

```bash
sudo apt update
sudo apt install nginx -y
```

Create a custom page:

```bash
echo '<h1>Response from Backend Server 01</h1>' | \
sudo tee /var/www/html/index.html
```

On Backend 02:

```bash
sudo apt update
sudo apt install nginx -y
```

Create a different page:

```bash
echo '<h1>Response from Backend Server 02</h1>' | \
sudo tee /var/www/html/index.html
```

Verify Nginx:

```bash
sudo systemctl status nginx
```

Verify that port 80 is listening:

```bash
sudo ss -tulpn | grep :80
```

---

# Backend Set Configuration

Suggested configuration:

```text
Name:
web-backend-set
```

```text
Policy:
Round Robin
```

```text
Health Check Protocol:
HTTP
```

```text
Health Check Port:
80
```

```text
Health Check URL Path:
/
```

```text
Expected Status Code:
200
```

---

# Add Backend Servers

Add the private IP address of each Compute Instance.

Example:

```text
Backend 01:
10.0.2.10:80
```

```text
Backend 02:
10.0.2.11:80
```

After adding them, verify their status.

Expected result:

```text
Backend 01: OK
Backend 02: OK
```

Do not continue until the backend servers are healthy.

---

# Listener Configuration

Create an HTTP Listener.

```text
Name:
http-listener
```

```text
Protocol:
HTTP
```

```text
Port:
80
```

```text
Default Backend Set:
web-backend-set
```

---

# Validation

## Check Backend Health

Inside the Load Balancer details, open the Backend Set and confirm that both backends are healthy.

Expected status:

```text
OK
```

or:

```text
Healthy
```

---

## Test the Load Balancer

Open:

```text
http://LOAD_BALANCER_PUBLIC_IP
```

Refresh the page several times.

You should see responses from both servers:

```text
Response from Backend Server 01
```

and:

```text
Response from Backend Server 02
```

The exact behavior may depend on connection reuse, browser caching, and Load Balancer settings.

You can also test using curl:

```bash
for i in {1..10}; do
  curl -s http://LOAD_BALANCER_PUBLIC_IP
  echo
done
```

---

# Validation Checklist

Before troubleshooting, confirm:

```text
[ ] Load Balancer has a public IP
[ ] Load Balancer is inside the public subnet
[ ] Public subnet routes 0.0.0.0/0 to the Internet Gateway
[ ] Private subnet routes 0.0.0.0/0 to the NAT Gateway
[ ] Backend instances have no public IP addresses
[ ] Nginx is running on both servers
[ ] Nginx listens on port 80
[ ] Load Balancer NSG allows inbound TCP port 80
[ ] Backend NSG allows TCP port 80 from the Load Balancer NSG
[ ] Backend private IP addresses are correct
[ ] Health Check uses the correct port and path
[ ] Both backend servers are healthy
[ ] Listener points to the correct Backend Set
```

---

# Common Beginner Mistakes

## Backend Servers Are Unhealthy

Possible causes:

* Nginx is not running
* Wrong backend port
* Wrong health check path
* Backend NSG blocks the Load Balancer
* The wrong private IP was added
* The application returns an unexpected status code

Check Nginx:

```bash
sudo systemctl status nginx
```

Check locally:

```bash
curl http://localhost
```

---

## Private Instances Cannot Install Packages

Possible causes:

* NAT Gateway was not created
* Private route table is missing
* The private subnet uses the wrong route table
* DNS resolution is not working
* Egress traffic is blocked

The private route table should include:

```text
0.0.0.0/0 → NAT Gateway
```

---

## Load Balancer Is Not Reachable

Possible causes:

* The Load Balancer is private instead of public
* Port 80 is blocked
* The public subnet uses the wrong route table
* Internet Gateway route is missing
* Listener was not created

The public route table should include:

```text
0.0.0.0/0 → Internet Gateway
```

---

## Load Balancer Works but Shows Only One Server

Possible causes:

* The second backend is unhealthy
* Browser connection reuse
* Browser cache
* Session persistence is enabled
* The Backend Set policy is not configured as expected

Use repeated curl requests to test more clearly.

---

## Backend Server Has a Public IP

This breaks the main security goal of the scenario.

The backend servers should be private.

Verify:

```text
Public IPv4 Address:
Not Assigned
```

---

# Security Improvements

The lab uses HTTP for simplicity.

A more secure production design should include:

* HTTPS Listener
* TLS certificate
* OCI Certificates service
* Restricted administration access
* OCI Bastion
* Web Application Firewall
* Logging and monitoring
* Vulnerability scanning
* Least-privilege IAM policies
* Multiple backend instances
* Backups
* Autoscaling

Improved flow:

```text
Internet
   │
   ▼
Web Application Firewall
   │
   ▼
HTTPS Load Balancer
   │
   ▼
Private Backend Servers
```

---

# Failure Scenario

Suppose Backend Server 01 fails.

```text
Backend 01: Unhealthy
Backend 02: Healthy
```

The Load Balancer stops sending new requests to Backend 01.

Traffic continues through Backend 02.

```text
Internet
   │
   ▼
Load Balancer
   │
   ├── Backend 01: Unhealthy
   │
   └── Backend 02: Healthy
                      │
                      ▼
                Receives Traffic
```

This is one of the main reasons for using a Load Balancer.

---

# Cleanup Order

Delete the resources in a safe order:

1. Delete the Listener if necessary
2. Remove backend servers
3. Delete the Load Balancer
4. Terminate the Compute Instances
5. Delete the Network Security Groups
6. Delete the private subnet
7. Delete the public subnet
8. Delete the private route table
9. Delete the public route table
10. Delete the NAT Gateway
11. Delete the Internet Gateway
12. Delete the VCN
13. Delete the Compartment if it is empty

Some resources cannot be deleted while another resource still depends on them.

---

# What You Learned

After completing this scenario, you should understand:

* Why backend servers should be private
* Why the Load Balancer is placed in a public subnet
* How public and private subnets work together
* The difference between an Internet Gateway and a NAT Gateway
* How Listeners receive traffic
* How Backend Sets group servers
* How Health Checks detect failures
* How the Load Balancer connects to private IP addresses
* How NSGs restrict traffic between resources
* Why resource creation order matters
* How traffic travels from the Internet to a private application server

---

# Main Relationship to Remember

```text
Internet
    │
    ▼
Internet Gateway
    │
    ▼
Public Load Balancer
    │
    ▼
Listener
    │
    ▼
Backend Set
    │
    ▼
Private Compute Instances
```

For outbound access:

```text
Private Compute Instances
    │
    ▼
NAT Gateway
    │
    ▼
Internet
```

---

# Next Scenario

Scenario 03:

```text
Two-Tier Web Application
```

The next scenario will add a private database layer behind the web servers.

```text
Internet
    │
    ▼
Load Balancer
    │
    ▼
Web Servers
    │
    ▼
Private Database
```
