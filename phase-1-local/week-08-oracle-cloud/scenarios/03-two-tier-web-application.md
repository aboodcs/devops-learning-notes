# Scenario 03 - Two-Tier Web Application

## Goal

In this scenario, we will build a two-tier web application on Oracle Cloud Infrastructure.

The architecture will contain:

1. An application tier
2. A database tier

Internet users will access the application through a public Load Balancer.

The Load Balancer will forward requests to private Compute Instances running the web application.

The application servers will connect to a private MySQL DB System.

The database will not be accessible directly from the Internet.

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
                     ┌────────────┴────────────┐
                     ▼                         ▼
             Application Server 01     Application Server 02
                 Private Subnet            Private Subnet
                     │                         │
                     └────────────┬────────────┘
                                  │
                                  ▼
                          MySQL DB System
                         Database Subnet
                             Private IP
```

Outbound Internet access for the application servers:

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

# What Is a Two-Tier Application?

A two-tier application separates the system into two main layers.

## Tier 1 - Application Tier

The application tier:

* Receives requests
* Runs application logic
* Validates user input
* Connects to the database
* Returns responses to users

In this scenario, the application runs on Compute Instances.

## Tier 2 - Database Tier

The database tier:

* Stores application data
* Processes database queries
* Returns results to the application
* Keeps data separate from the web-facing layer

In this scenario, the database tier uses a private MySQL DB System.

---

# Why Separate the Application and Database?

Running the application and database on separate resources provides several benefits.

## Better Security

The database is not exposed directly to the Internet.

Only the application servers can connect to it.

## Independent Scaling

We can add more application servers without moving the database.

## Easier Maintenance

The application and database can be updated independently.

## Better Resource Management

The application servers and database use different compute and storage resources.

## Clearer Architecture

Each layer has one main responsibility.

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
* Three Route Tables
* Three Network Security Groups
* Two Compute Instances
* One public Load Balancer
* One Backend Set
* One HTTP Listener
* One MySQL DB System
* One application database
* One database user
* A simple web application

Users will access:

```text
http://LOAD_BALANCER_PUBLIC_IP
```

The application servers will connect internally to:

```text
MYSQL_PRIVATE_IP:3306
```

---

# OCI Services Used

| Service                    | Purpose                                                   |
| -------------------------- | --------------------------------------------------------- |
| Compartment                | Organize the scenario resources                           |
| VCN                        | Provide the private cloud network                         |
| Public Subnet              | Host the public Load Balancer                             |
| Private Application Subnet | Host the Compute Instances                                |
| Private Database Subnet    | Host the MySQL DB System                                  |
| Internet Gateway           | Connect the public Load Balancer to the Internet          |
| NAT Gateway                | Give private application servers outbound Internet access |
| Route Tables               | Control traffic paths                                     |
| Network Security Groups    | Restrict communication between tiers                      |
| Load Balancer              | Receive and distribute incoming requests                  |
| Compute Instances          | Run the application                                       |
| MySQL DB System            | Store application data                                    |
| Backend Set                | Group application servers                                 |
| Health Check               | Verify application availability                           |
| Listener                   | Accept incoming HTTP traffic                              |

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

The Load Balancer needs to receive requests from Internet users, so it is placed in a public subnet.

---

## Application Layer

The application layer contains the Compute Instances.

```text
Load Balancer
      │
      ▼
Private Application Servers
```

The application servers:

* Do not have public IP addresses
* Receive traffic only from the Load Balancer
* Connect to the database using private networking
* Use the NAT Gateway for outbound Internet access

---

## Database Layer

The database layer contains the MySQL DB System.

```text
Application Servers
        │
        ▼
Private MySQL DB System
```

The database:

* Does not receive traffic from Internet users
* Does not need a public IP address
* Accepts database connections only from the application tier
* Uses port `3306` for MySQL connections

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

Example resource addresses:

```text
Load Balancer:
10.0.1.x
```

```text
Application Server 01:
10.0.2.10
```

```text
Application Server 02:
10.0.2.11
```

```text
MySQL DB System:
10.0.3.x
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
    │
    ├── NAT Gateway
    │
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
    │       ├── Application Server 01
    │       └── Application Server 02
    │
    └── Private Database Subnet
            │
            ├── Database Route Table
            ├── Database NSG
            └── MySQL DB System
```

---

# Main Communication Relationships

Three important network relationships exist in this architecture.

## User to Load Balancer

```text
Internet User
      │
      │ TCP 80
      ▼
Public Load Balancer
```

## Load Balancer to Application Servers

```text
Load Balancer
      │
      │ TCP 5000
      ▼
Application Servers
```

## Application Servers to Database

```text
Application Servers
      │
      │ TCP 3306
      ▼
MySQL DB System
```

Each layer should accept traffic only from the layer directly before it.

---

# Route Table Design

## Public Route Table

Used by the public Load Balancer subnet.

```text
Destination:
0.0.0.0/0

Target:
Internet Gateway
```

This allows the Load Balancer to communicate with Internet users.

---

## Application Route Table

Used by the private application subnet.

```text
Destination:
0.0.0.0/0

Target:
NAT Gateway
```

This allows application servers to:

* Install packages
* Download application dependencies
* Install security updates
* Contact external APIs

The application servers still do not accept direct inbound Internet connections.

---

## Database Route Table

The database subnet does not normally need direct Internet access for this basic scenario.

Local communication inside the VCN is automatically handled using the VCN local route.

The application servers communicate with the database using private IP addresses.

Do not add an Internet Gateway route to the database subnet.

---

# Network Security Design

Create three Network Security Groups:

```text
load-balancer-nsg
application-servers-nsg
database-nsg
```

Each NSG represents one architecture layer.

---

# Load Balancer NSG

## Ingress Rule

Allow HTTP traffic from the Internet.

```text
Source Type:
CIDR

Source:
0.0.0.0/0

IP Protocol:
TCP

Destination Port:
80
```

## Egress Rule

Allow the Load Balancer to communicate with the application servers.

```text
Destination Type:
Network Security Group

Destination:
application-servers-nsg

IP Protocol:
TCP

Destination Port:
5000
```

If the application listens on port `80`, replace port `5000` with port `80`.

---

# Application Servers NSG

## Ingress from Load Balancer

Allow application traffic only from the Load Balancer.

```text
Source Type:
Network Security Group

Source:
load-balancer-nsg

IP Protocol:
TCP

Destination Port:
5000
```

Do not allow:

```text
0.0.0.0/0 → TCP 5000
```

The Internet should not connect directly to the application servers.

## Egress to Database

Allow the application servers to connect to MySQL.

```text
Destination Type:
Network Security Group

Destination:
database-nsg

IP Protocol:
TCP

Destination Port:
3306
```

## Optional SSH Rule

Do not assign public IP addresses to the application servers.

For administrative access, consider:

* OCI Bastion
* VPN
* A controlled management instance
* Configuration management
* Instance Console Connection

---

# Database NSG

## Ingress Rule

Allow MySQL traffic only from the application servers.

```text
Source Type:
Network Security Group

Source:
application-servers-nsg

IP Protocol:
TCP

Destination Port:
3306
```

Do not allow:

```text
0.0.0.0/0 → TCP 3306
```

Do not allow the Load Balancer to connect directly to the database.

The Load Balancer should communicate only with the application tier.

---

# Security Flow

```text
Internet
   │
   │ Allowed: TCP 80
   ▼
Load Balancer NSG
   │
   │ Allowed: TCP 5000
   ▼
Application NSG
   │
   │ Allowed: TCP 3306
   ▼
Database NSG
```

Anything outside this expected path should be blocked.

---

# Application Request Flow

Suppose a user opens the application.

```text
http://LOAD_BALANCER_PUBLIC_IP
```

The complete request flow is:

1. The user sends an HTTP request.
2. The request reaches the Load Balancer public IP.
3. The Load Balancer Listener accepts the request on port 80.
4. The Backend Set selects a healthy application server.
5. The Load Balancer forwards the request to port 5000.
6. The application processes the request.
7. The application opens a private connection to MySQL on port 3306.
8. The database processes the SQL query.
9. The database returns the result to the application.
10. The application creates an HTTP response.
11. The response returns through the Load Balancer.
12. The Load Balancer returns the response to the user.

```text
Browser
   │
   ▼
Public Load Balancer
   │
   ▼
Application Server
   │
   ▼
MySQL DB System
   │
   ▼
Application Server
   │
   ▼
Load Balancer
   │
   ▼
Browser
```

---

# Example Application

We can use a simple Flask application that stores page visits inside MySQL.

The application will:

1. Connect to MySQL
2. Create a table
3. Insert or update a counter
4. Return the current visit count

Example response:

```text
Hello from OCI!

Application Server: app-server-01
Total Visits: 15
Database: Connected
```

---

# Application Environment Variables

Do not hardcode database connection information inside the application code.

Use environment variables:

```bash
DB_HOST=10.0.3.10
DB_PORT=3306
DB_NAME=webapp
DB_USER=webapp_user
DB_PASSWORD=CHANGE_ME
```

The `DB_HOST` value should use the MySQL DB System private endpoint or private IP address.

---

# Example Flask Application

Create `app.py`:

```python
import os
import socket

import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "webapp"),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id INT PRIMARY KEY,
            visit_count INT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO visits (id, visit_count)
        VALUES (1, 0)
        ON DUPLICATE KEY UPDATE id = id
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


@app.get("/")
def index():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE visits
        SET visit_count = visit_count + 1
        WHERE id = 1
        """
    )

    cursor.execute(
        """
        SELECT visit_count
        FROM visits
        WHERE id = 1
        """
    )

    visit_count = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(
        {
            "message": "Hello from OCI",
            "application_server": socket.gethostname(),
            "total_visits": visit_count,
            "database": "connected",
        }
    )


@app.get("/health")
def health():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()

        return jsonify({"status": "healthy"}), 200
    except mysql.connector.Error:
        return jsonify({"status": "unhealthy"}), 503


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
```

---

# Python Dependencies

Create `requirements.txt`:

```text
Flask
mysql-connector-python
gunicorn
```

Install the dependencies:

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

# Run the Application

Set the environment variables:

```bash
export DB_HOST="MYSQL_PRIVATE_IP"
export DB_PORT="3306"
export DB_NAME="webapp"
export DB_USER="webapp_user"
export DB_PASSWORD="CHANGE_ME"
```

Start the application using Gunicorn:

```bash
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  app:app
```

Check that the application is listening:

```bash
sudo ss -tulpn | grep :5000
```

Test locally:

```bash
curl http://localhost:5000
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# MySQL Database Preparation

Create the application database:

```sql
CREATE DATABASE webapp;
```

Create a dedicated user:

```sql
CREATE USER 'webapp_user'@'10.0.2.%'
IDENTIFIED BY 'CHANGE_ME';
```

Grant only the permissions needed by the application:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE
ON webapp.*
TO 'webapp_user'@'10.0.2.%';
```

Apply the changes:

```sql
FLUSH PRIVILEGES;
```

The application should not use the MySQL administrator account.

---

# Why Use a Dedicated Database User?

The application does not need complete administrative access.

A dedicated user limits the damage if the application credentials are exposed.

The application user should not normally be allowed to:

* Create other users
* Modify global MySQL settings
* Access unrelated databases
* Grant permissions
* Delete the entire DB System

This follows the principle of least privilege.

---

# Load Balancer Configuration

## Backend Set

```text
Name:
application-backend-set
```

```text
Policy:
Round Robin
```

## Health Check

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

Using `/health` is better than checking `/` because the health endpoint can verify that the application and database are working.

---

# Important Health Check Decision

There are two possible health check designs.

## Basic Health Check

```text
GET /health
```

Checks only whether the application process is running.

## Dependency-Aware Health Check

```text
GET /health
```

Checks:

* Application process
* Database connection
* Basic database query

The example application uses a dependency-aware health check.

If the database fails, the endpoint returns:

```text
HTTP 503
```

The Load Balancer may then mark the application server unhealthy.

This behavior must be chosen carefully.

If every application server depends on the same failed database, all servers may become unhealthy simultaneously.

---

# Listener Configuration

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

# Build Order

Create the resources in this order:

1. Create the Compartment
2. Create the VCN
3. Create the Internet Gateway
4. Create the NAT Gateway
5. Create the public Route Table
6. Create the application Route Table
7. Create the database Route Table
8. Create the public Load Balancer subnet
9. Create the private application subnet
10. Create the private database subnet
11. Create the Load Balancer NSG
12. Create the application servers NSG
13. Create the database NSG
14. Create the MySQL DB System
15. Record the MySQL private endpoint
16. Create the application database
17. Create the application database user
18. Create the two Compute Instances
19. Install the application dependencies
20. Configure the database environment variables
21. Start the application on both servers
22. Test the application locally
23. Test database connectivity
24. Create the public Load Balancer
25. Create the Backend Set
26. Configure the Health Check
27. Add both application servers
28. Create the HTTP Listener
29. Confirm that both backends are healthy
30. Test the application through the Load Balancer

---

# Why This Build Order Matters

The application cannot start successfully without the database connection details.

The Load Balancer should not be created before the application servers are ready.

The resources depend on each other:

```text
VCN
  ↓
Subnets
  ↓
NSGs
  ↓
Database
  ↓
Application Servers
  ↓
Load Balancer
```

Creating resources in the correct order makes troubleshooting easier.

---

# OCI Console Navigation

Console labels may change over time, but the resources are generally available through these sections.

## Create the VCN

```text
Navigation Menu
→ Networking
→ Virtual Cloud Networks
→ Create VCN
```

---

## Create the Subnets

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
private-application-subnet
private-database-subnet
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
application-servers-nsg
database-nsg
```

---

## Create the MySQL DB System

```text
Navigation Menu
→ Databases
→ MySQL HeatWave
→ DB Systems
→ Create DB System
```

During creation:

* Select the correct Compartment
* Select the scenario VCN
* Select the private database subnet
* Attach the database NSG
* Configure administrator credentials
* Choose an appropriate shape
* Configure backups
* Do not expose the database publicly

---

## Create the Compute Instances

```text
Navigation Menu
→ Compute
→ Instances
→ Create Instance
```

For each instance:

* Select the private application subnet
* Do not assign a public IPv4 address
* Attach `application-servers-nsg`
* Add your SSH public key
* Choose Ubuntu or Oracle Linux

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
* Public Load Balancer subnet
* `load-balancer-nsg`

---

# Validate Database Connectivity

From an application server, test whether port `3306` is reachable:

```bash
nc -zv MYSQL_PRIVATE_IP 3306
```

Expected result:

```text
Connection to MYSQL_PRIVATE_IP 3306 port succeeded
```

Install the MySQL client:

```bash
sudo apt update
sudo apt install mysql-client -y
```

Connect to the database:

```bash
mysql \
  -h MYSQL_PRIVATE_IP \
  -P 3306 \
  -u webapp_user \
  -p
```

Inside MySQL:

```sql
USE webapp;
SHOW TABLES;
SELECT * FROM visits;
```

---

# Validate the Application

Test each application server locally:

```bash
curl http://localhost:5000
```

Test the health endpoint:

```bash
curl -i http://localhost:5000/health
```

Expected status:

```text
HTTP/1.1 200 OK
```

---

# Validate the Load Balancer

Open:

```text
http://LOAD_BALANCER_PUBLIC_IP
```

Or run:

```bash
for i in {1..10}; do
  curl -s http://LOAD_BALANCER_PUBLIC_IP
  echo
done
```

You should receive responses from both application servers.

Example:

```json
{
  "application_server": "app-server-01",
  "database": "connected",
  "message": "Hello from OCI",
  "total_visits": 1
}
```

Then:

```json
{
  "application_server": "app-server-02",
  "database": "connected",
  "message": "Hello from OCI",
  "total_visits": 2
}
```

The visit counter remains shared because both application servers use the same database.

---

# Validation Checklist

```text
[ ] The Load Balancer is public
[ ] The Load Balancer subnet uses the Internet Gateway
[ ] Application servers are private
[ ] Application servers have no public IP addresses
[ ] Application subnet uses the NAT Gateway
[ ] Database is inside a private subnet
[ ] Database port 3306 is not open to the Internet
[ ] Load Balancer accepts TCP port 80
[ ] Application servers accept port 5000 only from the Load Balancer NSG
[ ] Database accepts port 3306 only from the application NSG
[ ] Both application servers can connect to MySQL
[ ] The application uses a dedicated database user
[ ] Database credentials are not hardcoded in the source code
[ ] The application responds locally
[ ] The health endpoint returns HTTP 200
[ ] Both Load Balancer backends are healthy
[ ] The application works through the Load Balancer
[ ] Both application servers share the same database data
```

---

# Common Beginner Mistakes

## Application Cannot Connect to MySQL

Possible causes:

* Wrong MySQL private IP address
* Wrong database username
* Wrong password
* Wrong database name
* Database NSG blocks port 3306
* Application NSG blocks egress traffic
* Application and database are in different VCNs
* The database is not active
* MySQL user host restrictions are incorrect

Test the port:

```bash
nc -zv MYSQL_PRIVATE_IP 3306
```

Test authentication:

```bash
mysql -h MYSQL_PRIVATE_IP -u webapp_user -p
```

---

## Load Balancer Backends Are Unhealthy

Possible causes:

* Application is not running
* Application listens only on `127.0.0.1`
* Wrong backend port
* Wrong health check path
* Application NSG blocks the Load Balancer
* Database failure makes `/health` return HTTP 503

Verify the listening address:

```bash
sudo ss -tulpn | grep :5000
```

The application should listen on:

```text
0.0.0.0:5000
```

Not only:

```text
127.0.0.1:5000
```

---

## Private Servers Cannot Install Packages

Possible causes:

* NAT Gateway is missing
* Application Route Table has no default route
* The subnet uses the wrong Route Table
* DNS resolution is not working
* Egress rules are too restrictive

Expected route:

```text
0.0.0.0/0 → NAT Gateway
```

---

## Database Is Accidentally Exposed

Never create this database ingress rule:

```text
Source:
0.0.0.0/0

Port:
3306
```

The correct source should be:

```text
Source:
application-servers-nsg

Port:
3306
```

---

## Application Uses the Administrator Account

Do not configure the application with the MySQL administrator username.

Create a dedicated user with limited permissions.

Bad:

```text
DB_USER=admin
```

Better:

```text
DB_USER=webapp_user
```

---

## Credentials Are Committed to Git

Do not store this inside `app.py`:

```python
password = "MyRealDatabasePassword"
```

Do not commit a `.env` file containing real credentials.

Add it to `.gitignore`:

```gitignore
.env
*.pem
```

For a production environment, use a secret-management solution instead of plain environment variables.

---

# Failure Scenarios

## One Application Server Fails

```text
Application Server 01: Unhealthy
Application Server 02: Healthy
```

The Load Balancer removes Server 01 from rotation and sends traffic to Server 02.

```text
Load Balancer
    │
    ├── Server 01: Unhealthy
    │
    └── Server 02: Healthy
                    │
                    ▼
              Receives Traffic
```

The application remains available.

---

## Database Fails

```text
Application Server 01: Running
Application Server 02: Running
Database: Unavailable
```

The web processes may still be running, but requests requiring data will fail.

If `/health` checks the database, both application servers may become unhealthy.

This demonstrates an important lesson:

> Adding multiple application servers does not make the database highly available.

Database high availability must be designed separately.

---

## Load Balancer Fails

OCI manages the Load Balancer service, but incorrect configuration can still make the application unavailable.

Possible causes:

* Listener missing
* Backend Set misconfigured
* Incorrect NSG rules
* Wrong health check
* Wrong backend IP addresses

---

# Security Improvements

A production version should include:

* HTTPS instead of HTTP
* TLS certificate
* OCI Certificates
* OCI Web Application Firewall
* OCI Bastion
* OCI Vault for credentials
* Database backups
* Automatic backup retention
* Logging
* Metrics
* Alerts
* Vulnerability scanning
* Restricted IAM policies
* Multiple availability or fault domains
* Database high availability
* Application autoscaling

Improved architecture:

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
Private Application Servers
   │
   ▼
Private Highly Available Database
```

---

# Monitoring Ideas

Monitor the following:

## Load Balancer

* Backend health
* HTTP response codes
* Request count
* Connection errors
* Response time

## Application Servers

* CPU usage
* Memory usage
* Disk usage
* Application process
* Application logs

## Database

* CPU usage
* Storage usage
* Active connections
* Failed connections
* Query performance
* Backup status

---

# Cleanup Order

Delete resources in this order:

1. Stop the application processes
2. Delete the Load Balancer Listener if necessary
3. Remove the backend servers
4. Delete the Load Balancer
5. Terminate the application Compute Instances
6. Delete the MySQL DB System
7. Confirm whether database backups should also be deleted
8. Delete the Load Balancer NSG
9. Delete the application servers NSG
10. Delete the database NSG
11. Delete the public Load Balancer subnet
12. Delete the private application subnet
13. Delete the private database subnet
14. Delete the Route Tables
15. Delete the NAT Gateway
16. Delete the Internet Gateway
17. Delete the VCN
18. Delete the Compartment if it is empty

Be careful when deleting the database.

Database deletion may permanently remove application data.

---

# What You Learned

After completing this scenario, you should understand:

* What a two-tier application is
* Why the application and database should be separated
* Why the database belongs in a private subnet
* How the application connects to the database
* How NSGs control communication between tiers
* Why the Load Balancer should not connect directly to the database
* How private application servers access the Internet through a NAT Gateway
* Why database credentials should not be hardcoded
* Why applications should use dedicated database users
* How Load Balancer health checks interact with application dependencies
* Why multiple application servers do not automatically make the database highly available
* How traffic moves through the entire architecture
* Why resource creation order matters

---

# Main Relationship to Remember

```text
Internet
    │
    ▼
Public Load Balancer
    │
    ▼
Private Application Servers
    │
    ▼
Private Database
```

Network permissions should follow the same direction:

```text
Internet
   │ TCP 80
   ▼
Load Balancer NSG
   │ TCP 5000
   ▼
Application NSG
   │ TCP 3306
   ▼
Database NSG
```

---

# Next Scenario

Scenario 04:

```text
High Availability Web Application
```

The next scenario will distribute resources across failure boundaries and explain how the application continues working when one server becomes unavailable.

```text
                         Load Balancer
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
        Application Server 01    Application Server 02
           Fault Domain 1           Fault Domain 2
```
