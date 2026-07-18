# Scenario 04 - High Availability Web Application

## Goal

In this scenario, we will build a highly available web application on Oracle Cloud Infrastructure.

The application will continue serving users even if one Compute Instance fails.

We will achieve this by:

* Running more than one application server
* Placing the servers in different Fault Domains
* Using a public Load Balancer
* Configuring health checks
* Keeping the database private
* Removing unhealthy servers automatically from traffic distribution

The main goal is not only to deploy an application.

The goal is to design the application so that the failure of one server does not bring down the entire service.

---

# Final Architecture

```text
                                Internet
                                    │
                                    ▼
                           Internet Gateway
                                    │
                                    ▼
                         Public Load Balancer
                            Public Subnet
                                    │
                                    ▼
                                Listener
                              HTTP Port 80
                                    │
                                    ▼
                               Backend Set
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
          Application Server 01          Application Server 02
              Fault Domain 1                 Fault Domain 2
             Private Subnet                 Private Subnet
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                            Private Database
```

Outbound Internet access:

```text
Private Application Servers
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

# What Is High Availability?

High Availability means designing a system so that it remains available when one component fails.

A normal single-server architecture looks like this:

```text
Internet
   │
   ▼
One Compute Instance
```

If that instance fails:

```text
Compute Instance: Down
Application: Down
```

This server becomes a single point of failure.

A highly available architecture uses multiple servers:

```text
Internet
   │
   ▼
Load Balancer
   │
   ├── Server 01
   └── Server 02
```

If one server fails, the other server continues receiving traffic.

---

# What Is a Single Point of Failure?

A single point of failure is one component whose failure causes the entire system to stop.

Examples include:

* One application server
* One database without redundancy
* One network path
* One deployment location
* One process running without restart management
* One backend inside the Load Balancer

In this scenario, we remove the application server single point of failure by using two application servers.

---

# Availability Domains and Fault Domains

Oracle Cloud uses failure boundaries to reduce the effect of hardware or infrastructure failures.

## Availability Domain

An Availability Domain is a separate data center within an OCI Region.

Availability Domains are isolated from each other.

Depending on the OCI Region, there may be:

* One Availability Domain
* Multiple Availability Domains

You should not assume that every OCI Region contains three Availability Domains.

---

## Fault Domain

A Fault Domain is a grouping of hardware and infrastructure inside an Availability Domain.

Fault Domains reduce the chance that multiple instances are affected by the same hardware failure or maintenance event.

Example:

```text
Availability Domain
    │
    ├── Fault Domain 1
    ├── Fault Domain 2
    └── Fault Domain 3
```

In this scenario:

```text
Application Server 01 → Fault Domain 1
Application Server 02 → Fault Domain 2
```

If one Fault Domain has a problem, the second server may remain available.

---

# Availability Domain vs Fault Domain

| Feature            | Availability Domain        | Fault Domain                       |
| ------------------ | -------------------------- | ---------------------------------- |
| Scope              | Large failure boundary     | Smaller failure boundary           |
| Usually represents | Separate data center       | Separate hardware grouping         |
| Isolation level    | Higher                     | Lower                              |
| Used for           | Regional high availability | Instance distribution inside an AD |
| Availability       | Depends on Region          | Commonly available within an AD    |

---

# What We Want to Build

We will create:

* One Compartment
* One VCN
* One public Load Balancer subnet
* One private application subnet
* One private database subnet
* One Internet Gateway
* One NAT Gateway
* Route Tables
* Network Security Groups
* Two application Compute Instances
* One public Load Balancer
* One Backend Set
* One HTTP Listener
* One health check
* One private database
* A simple web application
* Monitoring and validation checks

The two application servers will be placed in separate Fault Domains.

---

# OCI Services Used

| Service                    | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| Compartment                | Organize resources                                     |
| VCN                        | Provide the private cloud network                      |
| Public Subnet              | Host the Load Balancer                                 |
| Private Application Subnet | Host application servers                               |
| Private Database Subnet    | Host the database                                      |
| Internet Gateway           | Connect the public Load Balancer to the Internet       |
| NAT Gateway                | Provide outbound Internet access for private servers   |
| Route Tables               | Control network traffic                                |
| Network Security Groups    | Restrict traffic between tiers                         |
| Compute Instances          | Run the application                                    |
| Fault Domains              | Separate application servers across failure boundaries |
| Load Balancer              | Distribute incoming traffic                            |
| Backend Set                | Group application servers                              |
| Health Check               | Detect unhealthy application servers                   |
| Listener                   | Accept incoming requests                               |
| Database                   | Store shared application data                          |
| Monitoring                 | Track resource health and performance                  |

---

# Architecture Layers

## Public Layer

The public layer contains only the Load Balancer.

```text
Internet
   │
   ▼
Public Load Balancer
```

The Load Balancer receives traffic from users.

It is the only application component exposed to the Internet.

---

## Application Layer

The application layer contains two Compute Instances.

```text
                  Load Balancer
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      App Server 01       App Server 02
      Fault Domain 1      Fault Domain 2
```

Both servers run the same application.

They should use:

* The same application version
* The same configuration
* The same database
* The same health endpoint
* The same listening port

---

## Database Layer

The database remains private.

```text
Application Servers
        │
        ▼
Private Database
```

Both application servers connect to the same database.

The database should not accept traffic from the Internet.

---

# Important Limitation

Using two application servers improves the availability of the application tier.

However, it does not automatically make the entire architecture highly available.

If there is only one database and it fails:

```text
App Server 01: Running
App Server 02: Running
Database: Down
Application: Unavailable
```

Therefore:

> Application-tier high availability is not the same as full-system high availability.

The database must also have its own high-availability strategy.

---

# Suggested IP Address Plan

## VCN

```text
10.0.0.0/16
```

## Public Load Balancer Subnet

```text
10.0.1.0/24
```

## Private Application Subnet

```text
10.0.2.0/24
```

## Private Database Subnet

```text
10.0.3.0/24
```

Example private addresses:

```text
Application Server 01:
10.0.2.10
```

```text
Application Server 02:
10.0.2.11
```

```text
Database:
10.0.3.10
```

OCI may assign the exact private IP addresses automatically.

---

# Resource Relationships

```text
Compartment
    │
    ▼
VCN
    │
    ├── Internet Gateway
    ├── NAT Gateway
    │
    ├── Public Load Balancer Subnet
    │       │
    │       ├── Public Route Table
    │       ├── Load Balancer NSG
    │       └── Public Load Balancer
    │               │
    │               ├── Listener
    │               ├── Backend Set
    │               └── Health Check
    │
    ├── Private Application Subnet
    │       │
    │       ├── Application Route Table
    │       ├── Application NSG
    │       ├── App Server 01
    │       │      └── Fault Domain 1
    │       └── App Server 02
    │              └── Fault Domain 2
    │
    └── Private Database Subnet
            │
            ├── Database NSG
            └── Private Database
```

---

# Main Availability Relationship

```text
Load Balancer
    │
    ├── Healthy App Server 01
    └── Healthy App Server 02
```

If one server fails:

```text
Load Balancer
    │
    ├── App Server 01: Unhealthy
    └── App Server 02: Healthy
                         │
                         ▼
                   Receives Traffic
```

The Load Balancer stops forwarding new requests to the unhealthy server.

---

# Network Security Design

Create three Network Security Groups:

```text
load-balancer-nsg
application-servers-nsg
database-nsg
```

---

# Load Balancer NSG

## Ingress Rule

Allow users to access the Load Balancer.

```text
Source:
0.0.0.0/0

Protocol:
TCP

Destination Port:
80
```

For HTTPS:

```text
Source:
0.0.0.0/0

Protocol:
TCP

Destination Port:
443
```

## Egress Rule

Allow the Load Balancer to connect to the application servers.

```text
Destination:
application-servers-nsg

Protocol:
TCP

Destination Port:
5000
```

---

# Application Servers NSG

## Ingress from Load Balancer

```text
Source:
load-balancer-nsg

Protocol:
TCP

Destination Port:
5000
```

The application servers should not accept application traffic directly from the Internet.

Do not configure:

```text
Source:
0.0.0.0/0

Destination Port:
5000
```

## Egress to Database

```text
Destination:
database-nsg

Protocol:
TCP

Destination Port:
3306
```

## Outbound Internet Access

The private application servers use the NAT Gateway for:

* Installing packages
* Downloading updates
* Pulling dependencies
* Contacting external services

---

# Database NSG

Allow MySQL traffic only from the application servers.

```text
Source:
application-servers-nsg

Protocol:
TCP

Destination Port:
3306
```

Do not allow:

```text
Source:
0.0.0.0/0

Destination Port:
3306
```

---

# Traffic Flow

A normal request follows this path:

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
Healthy Application Server
   │
   ▼
Private Database
```

The response returns through the same application server and Load Balancer.

---

# Load Balancer Configuration

## Listener

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
application-backend-set
```

---

## Backend Set

```text
Name:
application-backend-set
```

```text
Policy:
Round Robin
```

Backend servers:

```text
Application Server 01:
10.0.2.10:5000
```

```text
Application Server 02:
10.0.2.11:5000
```

---

# Health Check

Use a dedicated health endpoint.

```text
Protocol:
HTTP
```

```text
Port:
5000
```

```text
URL Path:
/health
```

```text
Expected Status Code:
200
```

The health check allows the Load Balancer to decide which servers should receive traffic.

---

# Example Health Endpoint

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Hello from OCI",
            "server": "application-server",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

The application must listen on:

```text
0.0.0.0:5000
```

Not only:

```text
127.0.0.1:5000
```

The Load Balancer cannot reach an application that listens only on localhost.

---

# Different Server Responses

To verify traffic distribution, configure each server with a different name.

On Application Server 01:

```bash
export SERVER_NAME="application-server-01"
```

On Application Server 02:

```bash
export SERVER_NAME="application-server-02"
```

Example application:

```python
import os

from flask import Flask, jsonify

app = Flask(__name__)

SERVER_NAME = os.getenv("SERVER_NAME", "unknown-server")


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Hello from OCI",
            "server": SERVER_NAME,
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200
```

---

# Run the Application

Install the required packages:

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Flask and Gunicorn:

```bash
pip install flask gunicorn
```

Run the application:

```bash
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  app:app
```

Verify the listening port:

```bash
sudo ss -tulpn | grep :5000
```

Test locally:

```bash
curl http://localhost:5000
```

Test health:

```bash
curl -i http://localhost:5000/health
```

---

# Using systemd

Running Gunicorn manually is not reliable.

If the server restarts, the application will stop.

Create a systemd service:

```bash
sudo nano /etc/systemd/system/oci-webapp.service
```

Example:

```ini
[Unit]
Description=OCI High Availability Web Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/webapp
Environment="SERVER_NAME=%H"
ExecStart=/home/ubuntu/webapp/venv/bin/gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service:

```bash
sudo systemctl enable oci-webapp
```

Start the service:

```bash
sudo systemctl start oci-webapp
```

Check its status:

```bash
sudo systemctl status oci-webapp
```

---

# Why Use Automatic Restart?

High availability is not only about having two servers.

Each server should also recover from application process failures.

With systemd:

```text
Application process crashes
        │
        ▼
systemd detects the failure
        │
        ▼
Application process restarts
```

This provides process-level recovery.

The Load Balancer provides server-level traffic failover.

---

# Build Order

Create the resources in this order:

1. Create the Compartment
2. Create the VCN
3. Create the Internet Gateway
4. Create the NAT Gateway
5. Create the public Route Table
6. Create the private application Route Table
7. Create the database Route Table
8. Create the public Load Balancer subnet
9. Create the private application subnet
10. Create the private database subnet
11. Create the Load Balancer NSG
12. Create the application servers NSG
13. Create the database NSG
14. Create the private database
15. Create Application Server 01 in Fault Domain 1
16. Create Application Server 02 in Fault Domain 2
17. Install the same application on both servers
18. Configure automatic application restart
19. Test each server locally
20. Test database connectivity
21. Create the public Load Balancer
22. Create the Backend Set
23. Configure the health check
24. Add both application servers
25. Create the HTTP Listener
26. Confirm both backends are healthy
27. Test traffic distribution
28. Simulate one server failure
29. Confirm the application remains available
30. Restore the failed server

---

# OCI Console Navigation

## Create Compute Instances

```text
Navigation Menu
→ Compute
→ Instances
→ Create Instance
```

For Application Server 01:

* Select the private application subnet
* Do not assign a public IP
* Attach `application-servers-nsg`
* Select Fault Domain 1

For Application Server 02:

* Select the same private application subnet
* Do not assign a public IP
* Attach `application-servers-nsg`
* Select Fault Domain 2

The exact Fault Domain selection may appear under advanced placement options.

---

## Create the Load Balancer

```text
Navigation Menu
→ Networking
→ Load Balancers
→ Create Load Balancer
```

Choose:

* Public Load Balancer
* Public subnet
* Flexible shape
* `load-balancer-nsg`

---

## Configure Backend Set

```text
Load Balancer Details
→ Backend Sets
→ Create Backend Set
```

Configure:

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
5000
```

```text
Health Check Path:
/health
```

---

## Add Backend Servers

```text
Backend Set
→ Backends
→ Add Backends
```

Add:

```text
Application Server 01 private IP
Port 5000
```

```text
Application Server 02 private IP
Port 5000
```

---

## Create Listener

```text
Load Balancer Details
→ Listeners
→ Create Listener
```

Configure:

```text
Protocol:
HTTP
```

```text
Port:
80
```

```text
Backend Set:
application-backend-set
```

---

# Validate Normal Traffic

Run:

```bash
for i in {1..10}; do
  curl -s http://LOAD_BALANCER_PUBLIC_IP
  echo
done
```

Expected responses:

```json
{
  "message": "Hello from OCI",
  "server": "application-server-01"
}
```

and:

```json
{
  "message": "Hello from OCI",
  "server": "application-server-02"
}
```

This confirms that both servers receive traffic.

---

# Failure Test 1 - Stop the Application

On Application Server 01:

```bash
sudo systemctl stop oci-webapp
```

Check the Load Balancer backend health.

Expected result:

```text
Application Server 01: Unhealthy
Application Server 02: Healthy
```

Test the Load Balancer again:

```bash
for i in {1..10}; do
  curl -s http://LOAD_BALANCER_PUBLIC_IP
  echo
done
```

All successful responses should come from Application Server 02.

---

# Restore Application Server 01

Start the application again:

```bash
sudo systemctl start oci-webapp
```

Check status:

```bash
sudo systemctl status oci-webapp
```

Wait for the Load Balancer health checks.

Expected result:

```text
Application Server 01: Healthy
Application Server 02: Healthy
```

---

# Failure Test 2 - Stop the Compute Instance

Stop Application Server 01 from the OCI Console.

Expected result:

```text
Application Server 01: Unavailable
Application Server 02: Healthy
```

The application should remain reachable through the Load Balancer.

Start the instance again and confirm that it returns to healthy status.

---

# Failure Test 3 - Block the Application Port

Temporarily block port `5000` on one server.

For example, using the operating-system firewall:

```bash
sudo ufw deny 5000/tcp
```

The Load Balancer should mark the server unhealthy.

Restore the rule:

```bash
sudo ufw delete deny 5000/tcp
```

Be careful when changing firewall rules on remote servers.

---

# What the Load Balancer Does During Failure

The Load Balancer sends health-check requests regularly.

```text
Load Balancer
      │
      ├── GET /health → Server 01
      └── GET /health → Server 02
```

If Server 01 stops responding successfully:

```text
Server 01 health check: Failed
Server 02 health check: Passed
```

The Load Balancer stops sending new application traffic to Server 01.

It continues using Server 02.

---

# Health Check Timing

Failover is not always immediate.

The Load Balancer may need several failed health checks before marking a backend unhealthy.

Similarly, it may need several successful checks before returning a recovered backend to service.

This prevents temporary network problems from causing constant backend status changes.

---

# Connection Draining

When removing or replacing a backend server, existing connections may still be active.

Connection draining allows existing requests to finish before the server is fully removed.

Without connection draining:

```text
Active request
     │
Server removed immediately
     │
Request may fail
```

With connection draining:

```text
Stop sending new requests
          │
Allow active requests to finish
          │
Remove backend safely
```

This is important during deployments and maintenance.

---

# Session State Problem

High availability introduces a common application problem.

Suppose a user logs in through Application Server 01.

If session data is stored only in that server's memory:

```text
User login
   │
   ▼
Server 01 stores session
```

The next request may go to Server 02:

```text
User request
   │
   ▼
Server 02
   │
   ▼
Session not found
```

The user may appear logged out.

---

# How to Handle Session State

Better options include:

* Store sessions in the database
* Store sessions in Redis
* Use signed stateless tokens
* Use an external session store
* Avoid local in-memory session state

A highly available application should be as stateless as possible.

---

# Stateless Application Design

A stateless application server does not depend on local memory or local files to serve the next request.

Bad design:

```text
User uploads file
      │
      ▼
Stored only on Server 01 local disk
```

If the next request goes to Server 02, the file is unavailable.

Better design:

```text
User uploads file
      │
      ▼
Object Storage
      │
      ├── Server 01 can access it
      └── Server 02 can access it
```

Shared data should be stored in shared services.

---

# Shared Data Recommendations

Use:

* Database for structured application data
* Object Storage for uploaded files
* Redis for shared cache or sessions
* File Storage when multiple servers require shared filesystem access

Avoid storing important application data only on one Compute Instance.

---

# Deployment Problem

If you manually update only one server:

```text
Server 01: Application Version 2
Server 02: Application Version 1
```

Users may receive different behavior depending on which server handles the request.

Both servers should run the same version.

---

# Basic Rolling Deployment

A simple rolling deployment process:

1. Remove Server 01 from Load Balancer traffic
2. Wait for existing connections to finish
3. Deploy the new application version
4. Validate Server 01
5. Add Server 01 back to the Backend Set
6. Confirm it is healthy
7. Remove Server 02 from traffic
8. Deploy the new version
9. Validate Server 02
10. Add Server 02 back to traffic

This keeps at least one server available during deployment.

---

# Validation Checklist

```text
[ ] Two application servers exist
[ ] Servers are placed in different Fault Domains
[ ] Both servers use the same application version
[ ] Both servers use the same configuration
[ ] Both servers use the same database
[ ] Both servers have no public IP addresses
[ ] Load Balancer is public
[ ] Load Balancer accepts TCP port 80
[ ] Application servers accept port 5000 only from the Load Balancer
[ ] Database accepts traffic only from the application NSG
[ ] Both servers return HTTP 200 from /health
[ ] Both backends are healthy
[ ] Traffic reaches both servers
[ ] Application remains available when one server stops
[ ] Recovered server returns to healthy status
[ ] Application process starts automatically after reboot
[ ] Session data is not stored only in local memory
[ ] Uploaded files are not stored only on one server
```

---

# Common Beginner Mistakes

## Both Servers Are in the Same Fault Domain

This reduces the availability benefit.

If both servers share the same failure boundary, one hardware or maintenance event may affect both.

Better:

```text
Server 01 → Fault Domain 1
Server 02 → Fault Domain 2
```

---

## Only One Backend Is Added

Creating two Compute Instances is not enough.

Both instances must be added to the Load Balancer Backend Set.

Check:

```text
Backend Set
├── Application Server 01
└── Application Server 02
```

---

## One Backend Is Unhealthy

Possible causes:

* Application is not running
* Wrong port
* Wrong health-check path
* NSG blocks traffic
* Application listens only on localhost
* Database failure affects the health endpoint

Check locally:

```bash
curl -i http://localhost:5000/health
```

Check listening ports:

```bash
sudo ss -tulpn | grep :5000
```

---

## Different Application Versions

Both servers should run the same code.

Check the application version or Git commit on both servers.

Example:

```bash
git rev-parse HEAD
```

The result should be identical.

---

## Local Session Storage

The application works until traffic moves to another server.

Use shared session storage or stateless authentication.

---

## Local File Uploads

A file uploaded to Server 01 is not available on Server 02.

Use Object Storage or File Storage.

---

## Health Check Is Too Simple

A health endpoint that always returns HTTP 200 may report a server as healthy even when important dependencies are unavailable.

However, a health check that depends on every external service may mark all servers unhealthy during one shared dependency failure.

Health-check design must match the application's requirements.

---

# Monitoring

## Load Balancer Monitoring

Monitor:

* Backend health
* HTTP response codes
* Request count
* Connection errors
* Response latency
* Failed health checks

## Compute Monitoring

Monitor:

* CPU utilization
* Memory usage
* Disk usage
* Network traffic
* Process health
* Application logs

## Application Monitoring

Monitor:

* Request rate
* Error rate
* Response time
* Database connection failures
* Application restarts

## Database Monitoring

Monitor:

* Active connections
* CPU usage
* Storage usage
* Query latency
* Failed connections
* Backup status

---

# Alerts

Useful alerts include:

```text
Backend server becomes unhealthy
```

```text
HTTP 5xx error rate increases
```

```text
Application server CPU exceeds threshold
```

```text
Database connections fail
```

```text
Disk usage becomes high
```

Alerts help engineers detect failures before users report them.

---

# Full-System High Availability Improvements

To improve the architecture further, consider:

* Database high availability
* Multiple Availability Domains when supported
* Autoscaling
* HTTPS
* Web Application Firewall
* OCI Certificates
* OCI Vault
* Object Storage for shared files
* Redis for shared sessions
* Monitoring and alarms
* Automated backups
* Infrastructure as Code
* Automated deployment pipelines
* Disaster recovery in another Region

---

# Availability vs Disaster Recovery

High Availability and Disaster Recovery are not the same.

## High Availability

Protects against local component failures.

Examples:

* One server fails
* One Fault Domain fails
* One application process crashes

## Disaster Recovery

Protects against larger failures.

Examples:

* Entire Region becomes unavailable
* Major network outage
* Severe configuration corruption
* Data loss

High Availability usually keeps the application running in the same Region.

Disaster Recovery may require another Region.

---

# Failure Scenarios

## Application Server 01 Fails

```text
Server 01: Unhealthy
Server 02: Healthy
Application: Available
```

## Application Server 02 Fails

```text
Server 01: Healthy
Server 02: Unhealthy
Application: Available
```

## Both Application Servers Fail

```text
Server 01: Unhealthy
Server 02: Unhealthy
Application: Unavailable
```

## Database Fails

```text
Application Servers: Running
Database: Unavailable
Application: Partially or fully unavailable
```

## Load Balancer Configuration Fails

```text
Servers: Healthy
Database: Healthy
Listener or NSG: Incorrect
Application: Unreachable
```

High availability requires every important layer to be considered.

---

# Cleanup Order

Delete resources in this order:

1. Stop application traffic
2. Remove backend servers
3. Delete the Listener if necessary
4. Delete the Load Balancer
5. Terminate Application Server 01
6. Terminate Application Server 02
7. Delete the database if the data is no longer needed
8. Delete the Network Security Groups
9. Delete the public subnet
10. Delete the private application subnet
11. Delete the private database subnet
12. Delete the Route Tables
13. Delete the NAT Gateway
14. Delete the Internet Gateway
15. Delete the VCN
16. Delete the Compartment if it is empty

Verify backups before deleting the database.

---

# What You Learned

After completing this scenario, you should understand:

* What High Availability means
* What a single point of failure is
* The difference between Availability Domains and Fault Domains
* Why application servers should be distributed across failure boundaries
* How a Load Balancer detects unhealthy servers
* How traffic continues when one server fails
* Why application processes need automatic restart
* Why session state should not remain only in server memory
* Why uploaded files should use shared storage
* Why both servers must run the same application version
* Why application-tier redundancy does not guarantee database availability
* The difference between High Availability and Disaster Recovery
* How to test failures instead of only assuming the design works

---

# Main Relationship to Remember

```text
                        Load Balancer
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        Application Server 01   Application Server 02
           Fault Domain 1          Fault Domain 2
```

Normal operation:

```text
Server 01: Healthy
Server 02: Healthy
Traffic: Distributed
```

One server fails:

```text
Server 01: Unhealthy
Server 02: Healthy
Traffic: Sent to Server 02
```

---

# Next Scenario

Scenario 05:

```text
Private Instance with NAT Gateway
```

The next scenario will focus on outbound Internet access from a private Compute Instance without assigning it a public IP address.

```text
Private Compute Instance
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
