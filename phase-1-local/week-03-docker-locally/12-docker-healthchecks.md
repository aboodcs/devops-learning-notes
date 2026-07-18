# 12 - Docker Healthchecks

A **Docker healthcheck** is a test that Docker runs inside a container to check if the application is healthy.

A container can be running, but the application inside it may not be working correctly.

```text id="89ockx"
Container running does not always mean application healthy
```

## Simple Explanation

Without healthcheck:

```text id="4zuk77"
Docker only knows:
Container process is running
```

With healthcheck:

```text id="n25njp"
Docker checks:
Is the application really responding?
```

Example:

```text id="n7f7dp"
Nginx container is running
Docker healthcheck tests http://localhost
If it responds → healthy
If it fails → unhealthy
```

## Why Do We Need Healthchecks?

Healthchecks help you detect problems inside containers.

Examples:

```text id="zgjt80"
Application not responding
Web server down
Database not ready
API endpoint failing
Redis not reachable
Wrong port configuration
```

A container may show `Up`, but the app may still be broken.

Healthchecks make this clearer.

## Container Status Without Healthcheck

Run a container:

```bash id="q9h4xt"
docker run -d --name nginx-test nginx:alpine
```

Check:

```bash id="fnmgap"
docker ps
```

You may see:

```text id="dljx5i"
STATUS: Up 10 seconds
```

This only means the main container process is running.

It does not prove the website works.

## Container Status With Healthcheck

With a healthcheck, Docker can show:

```text id="i3ekqu"
healthy
unhealthy
starting
```

Example:

```text id="bdva9k"
STATUS: Up 30 seconds (healthy)
```

or:

```text id="xp53zk"
STATUS: Up 30 seconds (unhealthy)
```

## Healthcheck States

| State          | Meaning                                  |
| -------------- | ---------------------------------------- |
| `starting`     | Docker is waiting before checking        |
| `healthy`      | Healthcheck command succeeds             |
| `unhealthy`    | Healthcheck command fails too many times |
| no healthcheck | No healthcheck configured                |

## Basic Healthcheck Command

A healthcheck runs a command inside the container.

Example:

```dockerfile id="lq6nuh"
HEALTHCHECK CMD curl -f http://localhost || exit 1
```

Meaning:

```text id="m5tnga"
curl -f http://localhost → Check if the app responds
exit 1                  → Mark as failed if curl fails
```

## Dockerfile Healthcheck Example

Example Dockerfile for Nginx:

```dockerfile id="xv7vd4"
FROM nginx:alpine

HEALTHCHECK CMD wget --spider -q http://localhost || exit 1
```

Build:

```bash id="zl6ij7"
docker build -t nginx-healthcheck:1.0.0 .
```

Run:

```bash id="orppfg"
docker run -d --name nginx-health -p 8080:80 nginx-healthcheck:1.0.0
```

Check:

```bash id="kbpa14"
docker ps
```

You should see something like:

```text id="ezixva"
Up 20 seconds (healthy)
```

## Healthcheck Options

You can control how Docker runs the healthcheck.

Example:

```dockerfile id="sx1sm4"
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
  CMD wget --spider -q http://localhost || exit 1
```

## Option Meaning

| Option           | Meaning                                  |
| ---------------- | ---------------------------------------- |
| `--interval`     | How often Docker runs the check          |
| `--timeout`      | Maximum time allowed for one check       |
| `--retries`      | Number of failed checks before unhealthy |
| `--start-period` | Grace period before failures count       |

## Simple Option Example

```dockerfile id="vkz7jo"
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget --spider -q http://localhost || exit 1
```

Meaning:

```text id="felbos"
Check every 10 seconds
Each check can take maximum 3 seconds
After 3 failed checks, mark container unhealthy
```

## Healthcheck in docker run

You can add a healthcheck directly when running a container.

Example:

```bash id="w0ef6v"
docker run -d \
  --name nginx-health \
  -p 8080:80 \
  --health-cmd="wget --spider -q http://localhost || exit 1" \
  --health-interval=10s \
  --health-timeout=3s \
  --health-retries=3 \
  nginx:alpine
```

Check:

```bash id="j9m0qh"
docker ps
```

## Healthcheck in Docker Compose

Healthchecks are commonly used in Docker Compose.

Example:

```yaml id="mq70f0"
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 10s
```

Run:

```bash id="v0bkwc"
docker compose up -d
```

Check:

```bash id="t1zgg4"
docker compose ps
```

## Flask Healthcheck Example

A good application should have a health endpoint.

Example:

```text id="h8wgxz"
/health
```

## app.py

```python id="mylzh5"
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask\n"

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## requirements.txt

```text id="fa0j86"
flask
```

## Dockerfile

```dockerfile id="hvrham"
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
```

Build:

```bash id="m5ov5z"
docker build -t flask-healthcheck:1.0.0 .
```

Run:

```bash id="r3tu3u"
docker run -d \
  --name flask-health \
  -p 5000:5000 \
  flask-healthcheck:1.0.0
```

Check:

```bash id="oowczx"
docker ps
```

Test manually:

```bash id="ou8h81"
curl http://localhost:5000/health
```

Expected output:

```json id="s80s6f"
{
  "status": "healthy"
}
```

## Healthcheck Exit Codes

Docker uses exit codes to decide health.

```text id="ecdfzz"
exit 0 → healthy
exit 1 → unhealthy
```

Example:

```dockerfile id="to4me7"
HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
```

If `curl` succeeds, exit code is `0`.

If `curl` fails, the command exits with `1`.

## Inspect Healthcheck Result

Use `docker inspect`:

```bash id="e6emvb"
docker inspect flask-health
```

Show only health status:

```bash id="kl65tc"
docker inspect --format='{{.State.Health.Status}}' flask-health
```

Show healthcheck logs:

```bash id="z7j75z"
docker inspect --format='{{json .State.Health}}' flask-health
```

## View Health Events

Docker can show health status changes.

```bash id="7hpuxl"
docker events
```

In another terminal, restart or break the container.

You may see events like:

```text id="0axoo9"
health_status: healthy
health_status: unhealthy
```

## Healthcheck with Redis

Redis can be checked using `redis-cli ping`.

Example Docker Compose:

```yaml id="xltogg"
services:
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
```

Healthy Redis should return:

```text id="vqzq5m"
PONG
```

## Healthcheck with PostgreSQL

PostgreSQL can be checked using `pg_isready`.

Example:

```yaml id="sn18we"
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: abood
      POSTGRES_PASSWORD: 123abood
      POSTGRES_DB: appdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U abood -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
```

This checks if PostgreSQL is ready to accept connections.

## CMD vs CMD-SHELL

There are two common healthcheck styles.

### CMD

```yaml id="l72x2w"
test: ["CMD", "wget", "--spider", "-q", "http://localhost"]
```

This runs the command directly.

### CMD-SHELL

```yaml id="o9fko7"
test: ["CMD-SHELL", "curl -f http://localhost || exit 1"]
```

This runs the command through a shell.

Use `CMD-SHELL` when you need shell features like:

```text id="dcyirw"
||
&&
environment variables
pipes
```

## Healthcheck and depends_on

In Docker Compose, `depends_on` controls startup order.

But basic `depends_on` does not always mean the dependency is ready.

Example problem:

```text id="ch6djm"
Web container starts
Database container starts
But database is not ready yet
Web app fails
```

With healthcheck, Compose can wait for a healthy dependency.

Example:

```yaml id="xleair"
services:
  web:
    build: .
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: abood
      POSTGRES_PASSWORD: 123abood
      POSTGRES_DB: appdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U abood -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Meaning:

```text id="vx9vud"
Start web only after postgres becomes healthy
```

## Disable a Healthcheck

Some images already have healthchecks.

You can disable it:

```bash id="kxifhd"
docker run --no-healthcheck IMAGE_NAME
```

In Dockerfile:

```dockerfile id="napvh4"
HEALTHCHECK NONE
```

## Good Healthcheck Endpoint

A good `/health` endpoint should be simple.

It should check:

```text id="gal9oi"
Application is running
Important dependencies are reachable if needed
Response is fast
Status code is correct
```

Example:

```text id="xzva1x"
/health → 200 OK
```

Avoid making healthchecks too heavy.

Bad healthcheck:

```text id="qspvka"
Runs expensive database query every few seconds
```

Better:

```text id="ndoy7n"
Simple lightweight check
```

## Healthcheck vs Logs

Healthchecks and logs are different.

| Healthcheck                    | Logs                  |
| ------------------------------ | --------------------- |
| Shows if app is healthy        | Shows what happened   |
| Gives status healthy/unhealthy | Gives detailed output |
| Good for monitoring            | Good for debugging    |

Use both together.

```bash id="upcr02"
docker ps
docker logs CONTAINER_NAME
```

## Healthcheck vs Restart Policy

A healthcheck marks the container as unhealthy.

But Docker does not automatically restart an unhealthy container just because of healthcheck.

For automatic restarts, use restart policy:

```bash id="zzqfpi"
docker run -d \
  --name web \
  --restart unless-stopped \
  nginx:alpine
```

Important:

```text id="yvj51b"
Healthcheck detects health
Restart policy restarts when the container exits
```

They are related, but not the same thing.

## Practical Lab

Create project:

```bash id="u0z9k2"
mkdir docker-healthcheck-lab
cd docker-healthcheck-lab
touch app.py requirements.txt Dockerfile
```

Add `requirements.txt`:

```text id="l5ul1l"
flask
```

Add `app.py`:

```python id="sqo7ex"
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running\n"

@app.route("/health")
def health():
    return "healthy\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Add `Dockerfile`:

```dockerfile id="p52lo5"
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
```

Build:

```bash id="uxzfhe"
docker build -t healthcheck-lab:1.0.0 .
```

Run:

```bash id="gt8a1o"
docker run -d \
  --name healthcheck-lab \
  -p 5000:5000 \
  healthcheck-lab:1.0.0
```

Check status:

```bash id="yphdna"
docker ps
```

Test health endpoint:

```bash id="y8dv8a"
curl http://localhost:5000/health
```

Inspect health:

```bash id="llmcwj"
docker inspect --format='{{.State.Health.Status}}' healthcheck-lab
```

Clean up:

```bash id="rmfaip"
docker rm -f healthcheck-lab
```

## Common Beginner Mistakes

### Checking Wrong Port

Bad:

```dockerfile id="r1enki"
HEALTHCHECK CMD curl -f http://localhost:80 || exit 1
```

when the app runs on port `5000`.

Better:

```dockerfile id="axivwy"
HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
```

### Using curl Without Installing It

If the image does not include `curl`, this will fail:

```dockerfile id="fxy73c"
HEALTHCHECK CMD curl -f http://localhost || exit 1
```

Fix by installing `curl`, or use a tool that exists in the image.

For Alpine Nginx, use:

```dockerfile id="i8da9a"
HEALTHCHECK CMD wget --spider -q http://localhost || exit 1
```

### Healthcheck Too Slow

Bad:

```text id="awwpzx"
Healthcheck takes 20 seconds every 10 seconds
```

Better:

```text id="rx3fr0"
Fast check that returns quickly
```

### Healthcheck Too Strict

If the healthcheck depends on too many things, it may mark the app unhealthy even when the app is mostly working.

Start simple.

### Forgetting start_period

Some apps need time to start.

Use:

```dockerfile id="dxvw8o"
--start-period=20s
```

This gives the app time before Docker counts failures.

## Useful Commands

Check containers:

```bash id="jq15hy"
docker ps
```

Inspect health:

```bash id="t93hsg"
docker inspect --format='{{.State.Health.Status}}' CONTAINER_NAME
```

View logs:

```bash id="rntok9"
docker logs CONTAINER_NAME
```

Follow logs:

```bash id="s4ssrm"
docker logs -f CONTAINER_NAME
```

Run with healthcheck:

```bash id="typ9d6"
docker run \
  --health-cmd="curl -f http://localhost:5000/health || exit 1" \
  IMAGE_NAME
```

Disable healthcheck:

```bash id="ggmvxq"
docker run --no-healthcheck IMAGE_NAME
```

## Summary

```text id="lgnhah"
Healthcheck     → Test that checks if container app is healthy
healthy         → Healthcheck passed
unhealthy       → Healthcheck failed too many times
starting        → Container is still in grace/start period
HEALTHCHECK     → Dockerfile instruction for healthcheck
--health-cmd    → Add healthcheck from docker run
healthcheck     → Docker Compose healthcheck section
```

```text id="m989qd"
Running container does not always mean healthy app.
Use healthchecks to verify the application is really working.
```

> Docker healthchecks help you know if the application inside a running container is actually healthy and responding correctly.

