# 08 - Load Balancer

A **Load Balancer** distributes traffic across multiple servers.

Instead of users connecting to one Compute Instance directly, users connect to the Load Balancer.

The Load Balancer then sends traffic to healthy backend servers.

```text id="e58y2s"
User
 ↓
Load Balancer
 ↓
Compute Instances
```

## Why Do We Need a Load Balancer?

If you have only one server, the application depends on that server.

```text id="8fj6fp"
User → Compute Instance
```

If the Compute Instance fails, the application goes down.

With a Load Balancer:

```text id="ad7f96"
User
 ↓
Load Balancer
 ├── Compute Instance 1
 ├── Compute Instance 2
 └── Compute Instance 3
```

If one instance fails, traffic can go to another healthy instance.

## What Does a Load Balancer Do?

A Load Balancer helps with:

```text id="p19i8q"
Traffic distribution
High availability
Health checks
Better reliability
Scaling applications
Single public entry point
```

## Simple Explanation

Think of a Load Balancer like a receptionist.

Users do not choose which server to visit.

The Load Balancer receives the request and sends it to an available server.

```text id="mtklsr"
Request comes in
      ↓
Load Balancer checks available servers
      ↓
Request goes to a healthy server
```

## Basic Architecture

```text id="ci0079"
Internet
   ↓
Public Load Balancer
   ↓
Backend Set
   ├── Web Server 1
   ├── Web Server 2
   └── Web Server 3
```

The user only sees the Load Balancer address.

The backend servers stay behind it.

## Main Load Balancer Components

The main OCI Load Balancer parts are:

```text id="zob2gd"
Load Balancer
Listener
Backend Set
Backend Servers
Health Check
Rules
```

## 1. Load Balancer

The **Load Balancer** is the main resource.

It receives traffic from users and forwards it to backend servers.

Example:

```text id="btn7ic"
User → Load Balancer → Web Servers
```

In OCI, a Load Balancer can be:

```text id="ev2jlk"
Public Load Balancer
Private Load Balancer
```

## 2. Public Load Balancer

A **Public Load Balancer** has a public IP address.

It can receive traffic from the internet.

Use it for:

```text id="girv85"
Public websites
APIs
Web applications
Frontend services
```

Example:

```text id="c7zqpu"
Internet
   ↓
Public Load Balancer
   ↓
Web Servers
```

## 3. Private Load Balancer

A **Private Load Balancer** does not have a public IP address.

It is only reachable inside the VCN.

Use it for:

```text id="n8bec9"
Internal applications
Private APIs
Microservices
Internal company systems
```

Example:

```text id="ut3j8n"
Application Server
      ↓
Private Load Balancer
      ↓
Internal Backend Servers
```

## Public vs Private Load Balancer

| Public Load Balancer       | Private Load Balancer            |
| -------------------------- | -------------------------------- |
| Has public IP              | Has private IP only              |
| Accessible from internet   | Accessible inside VCN            |
| Used for websites and APIs | Used for internal services       |
| Needs public subnet        | Usually placed in private subnet |

## 4. Listener

A **Listener** listens for incoming traffic on a specific port and protocol.

Examples:

```text id="okxszq"
HTTP on port 80
HTTPS on port 443
TCP on port 8080
```

Example listener:

```text id="w58gou"
Protocol: HTTP
Port: 80
```

Meaning:

```text id="z5sxmg"
The Load Balancer accepts HTTP traffic on port 80.
```

## 5. Backend Set

A **Backend Set** is a group of backend servers.

It contains:

```text id="u9ckto"
Backend servers
Load balancing policy
Health check configuration
```

Example:

```text id="q2dy0o"
Backend Set: web-backend-set
├── Web Server 1
├── Web Server 2
└── Web Server 3
```

## 6. Backend Servers

**Backend Servers** are the real servers that run the application.

In OCI, backend servers are usually Compute Instances.

Example:

```text id="z98xdd"
Compute Instance 1 → 10.0.1.10:80
Compute Instance 2 → 10.0.1.11:80
```

The Load Balancer forwards traffic to these backend servers.

## 7. Health Check

A **Health Check** checks if a backend server is working.

Example:

```text id="1v6syf"
GET /
Port: 80
Protocol: HTTP
```

If the backend server responds correctly, it is healthy.

If the backend server does not respond, the Load Balancer stops sending traffic to it.

```text id="gub0zn"
Healthy backend   → receives traffic
Unhealthy backend → does not receive traffic
```

## Health Check Example

```text id="6wjsci"
Load Balancer
   ↓
Check Web Server 1 → Healthy
Check Web Server 2 → Unhealthy
Check Web Server 3 → Healthy
```

Traffic goes only to healthy servers:

```text id="pc8ko5"
Web Server 1
Web Server 3
```

## 8. Load Balancing Policy

The policy decides how traffic is distributed.

Common idea:

```text id="ox1ppj"
Send requests across backend servers
```

Example:

```text id="z9nlyl"
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 1
Request 4 → Server 2
```

This helps avoid sending all traffic to one server.

## Common Ports

| Port | Usage                              |
| ---: | ---------------------------------- |
|   80 | HTTP                               |
|  443 | HTTPS                              |
| 8080 | Web app testing                    |
| 5000 | Flask app                          |
| 3000 | Node.js app                        |
|   22 | SSH, not usually for Load Balancer |

Usually, a Load Balancer receives traffic on port `80` or `443`.

## Load Balancer with Public Subnet

A common beginner architecture:

```text id="b3d6zf"
VCN
├── Public Subnet
│   └── Public Load Balancer
│
└── Private Subnet
    ├── Compute Instance 1
    └── Compute Instance 2
```

Traffic flow:

```text id="gdbqjc"
User
 ↓
Internet
 ↓
Load Balancer
 ↓
Compute Instances
```

## Load Balancer with Web Servers

Example:

```text id="aavtdk"
User
 ↓
Load Balancer: 129.x.x.x
 ↓
Backend Set
 ├── web-1:80
 └── web-2:80
```

The user opens:

```text id="0qxm4x"
http://LOAD_BALANCER_PUBLIC_IP
```

The Load Balancer sends the request to one backend server.

## Security Rules

For the Load Balancer to work, security rules must allow traffic.

You usually need:

```text id="ux8bqj"
Internet → Load Balancer port 80 or 443
Load Balancer → Backend servers on app port
```

Example:

```text id="o0jed1"
Allow HTTP 80 from 0.0.0.0/0 to Load Balancer
Allow traffic from Load Balancer subnet to backend servers
```

## Important Security Note

Do not expose backend servers directly if they do not need public access.

Better design:

```text id="yiyn1b"
Internet
 ↓
Load Balancer
 ↓
Private Compute Instances
```

This keeps backend servers safer.

## Load Balancer vs Compute Public IP

### Without Load Balancer

```text id="3m7w5a"
User → Compute Instance Public IP
```

Problem:

```text id="sftrnv"
One server only
No automatic health check
Less reliable
Harder to scale
```

### With Load Balancer

```text id="6avsn3"
User → Load Balancer → Multiple Compute Instances
```

Better because:

```text id="y0to1z"
More reliable
Can scale to multiple servers
Can remove unhealthy servers
One stable entry point
```

## OCI Console Path

To create a Load Balancer:

```text id="hl8xc8"
OCI Console
→ Networking
→ Load Balancers
→ Create Load Balancer
```

During creation, you usually choose:

```text id="jhht80"
Load Balancer type
Visibility: Public or Private
VCN
Subnet
Bandwidth / shape
Listener
Backend set
Backend servers
Health check
```

## Beginner Example

You have two Compute Instances running Nginx.

```text id="cu86ob"
web-1 → 10.0.1.10
web-2 → 10.0.1.11
```

You create a Load Balancer:

```text id="yjz79v"
Public Load Balancer
Listener: HTTP 80
Backend Set: web-backend-set
Backends:
- 10.0.1.10:80
- 10.0.1.11:80
Health Check: HTTP /
```

Now users access:

```text id="29pkx9"
http://LOAD_BALANCER_PUBLIC_IP
```

The Load Balancer distributes requests between `web-1` and `web-2`.

## Simple Nginx Test

On each backend Compute Instance, install Nginx:

```bash id="n3g357"
sudo apt update
sudo apt install nginx -y
```

Change the page on server 1:

```bash id="0ocxgn"
echo "Hello from web-1" | sudo tee /var/www/html/index.html
```

Change the page on server 2:

```bash id="yxlebo"
echo "Hello from web-2" | sudo tee /var/www/html/index.html
```

Then open the Load Balancer public IP in the browser.

You may see traffic going to different servers.

## Common Beginner Mistakes

### Backend Servers Are Unhealthy

Check:

```text id="am8y16"
Is the app running?
Is the port correct?
Is the health check path correct?
Do security rules allow traffic?
Is the backend server listening on the right IP?
```

### Wrong Listener Port

If the listener is on port `80`, users should access:

```text id="btbxs2"
http://LOAD_BALANCER_IP
```

If the listener is on port `443`, users should access:

```text id="7m0wnn"
https://LOAD_BALANCER_IP
```

### Security Rules Missing

The Load Balancer may exist, but traffic fails because security rules block it.

Always check:

```text id="v9xncw"
Load Balancer subnet rules
Backend subnet rules
NSG rules if used
Operating system firewall
```

### Backend App Listening Only on localhost

Bad:

```text id="p5yp3w"
127.0.0.1:5000
```

Better:

```text id="evheqy"
0.0.0.0:5000
```

If the app listens only on localhost, the Load Balancer cannot reach it.

## Simple Troubleshooting Flow

If the Load Balancer is not working:

```text id="q8kxib"
1. Check Load Balancer status
2. Check listener port
3. Check backend set
4. Check backend health
5. Check Compute Instance app is running
6. Check security rules
7. Check route tables
8. Check OS firewall
9. Check application logs
```

## Load Balancer in DevOps

Load Balancers are important in DevOps because they support:

```text id="dlqzhz"
Production deployments
High availability
Rolling updates
Scaling
Blue-green deployments
Canary deployments
Health-based routing
```

Example deployment idea:

```text id="9xjgi1"
Old version running on web-1
New version deployed to web-2
Load Balancer checks health
Traffic moves only to healthy servers
```

## Summary

```text id="2axwib"
Load Balancer  → Distributes traffic
Public LB      → Receives traffic from internet
Private LB     → Used inside the VCN
Listener       → Port and protocol for incoming traffic
Backend Set    → Group of backend servers
Backend Server → Compute Instance running the app
Health Check   → Checks if backend is working
```

> A Load Balancer gives your application one stable entry point and distributes traffic across healthy backend servers.

