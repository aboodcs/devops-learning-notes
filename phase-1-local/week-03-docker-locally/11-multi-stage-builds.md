# 11 - Multi-Stage Builds

A **multi-stage build** is a Docker build technique used to create smaller and cleaner Docker images.

It allows you to use more than one `FROM` statement inside one Dockerfile.

```text id="nyjg7p"
Stage 1 → Build the application
Stage 2 → Run the application
```

## Simple Explanation

In normal Docker builds, you may install many tools just to build the app.

But the final container does not need all of them.

Example:

```text id="xvi8v2"
Build tools needed:
gcc
make
pip cache
node_modules
test tools

Runtime needed:
application files
runtime only
```

Multi-stage builds help you keep only what is needed in the final image.

## Why Do We Need Multi-Stage Builds?

Multi-stage builds help with:

```text id="lgq40d"
Smaller Docker images
Cleaner final image
Better security
Faster image transfer
Less unnecessary files
Production-ready containers
```

## Normal Dockerfile Problem

Example:

```dockerfile id="tqvxuk"
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

This works, but it may include:

```text id="zs9v71"
Large base image
Build cache
Extra tools
Unneeded files
More security risk
```

## Multi-Stage Build Idea

A multi-stage Dockerfile separates the build process from the final runtime image.

```text id="oh6b8l"
Builder stage
   ↓
Creates dependencies or build files
   ↓
Runtime stage
   ↓
Copies only required files
```

## Basic Format

```dockerfile id="q4i5z5"
FROM image AS builder

# build steps here

FROM image AS runtime

# copy only needed files from builder
COPY --from=builder /source /destination
```

Important part:

```dockerfile id="qg192b"
COPY --from=builder
```

This copies files from one stage into another stage.

## Simple Multi-Stage Example

```dockerfile id="jn88xd"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

This uses:

```text id="bx5pc3"
builder stage → install dependencies
final stage   → run the app
```

## Stage Names

You can name a stage using `AS`.

Example:

```dockerfile id="sjxzck"
FROM python:3.12-slim AS builder
```

Here, the stage name is:

```text id="glsp2d"
builder
```

Then you can copy from it:

```dockerfile id="gu25xa"
COPY --from=builder /root/.local /root/.local
```

## Python Flask Example

Project structure:

```text id="n8483x"
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

## app.py

```python id="kg5bw1"
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from multi-stage Docker build\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## requirements.txt

```text id="pkqqy7"
flask
gunicorn
```

## Dockerfile

```dockerfile id="w6n9mj"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Build the Image

```bash id="qfqh30"
docker build -t flask-multistage:1.0.0 .
```

## Run the Container

```bash id="km9l9s"
docker run -d \
  --name flask-multistage \
  -p 5000:5000 \
  flask-multistage:1.0.0
```

Open:

```text id="zrer0p"
http://localhost:5000
```

## Check the Container

```bash id="dtpyfg"
docker ps
```

Check logs:

```bash id="pezxpo"
docker logs flask-multistage
```

Stop and remove:

```bash id="ayh884"
docker rm -f flask-multistage
```

## Why This Dockerfile Is Better

The builder stage installs dependencies.

The runtime stage only gets:

```text id="m5m1rb"
Installed Python packages
Application file
Runtime image
Final command
```

It does not keep the full build process history as normal files.

## Node.js Multi-Stage Example

Multi-stage builds are very common with frontend apps.

Example:

```dockerfile id="0yq2c7"
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine AS runtime

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Meaning:

```text id="7rtvv0"
Node stage  → builds the frontend app
Nginx stage → serves the final static files
```

The final image does not contain:

```text id="k7kxhw"
Node.js
npm
source files
node_modules used for build
```

It only contains the built static files inside Nginx.

## Go Multi-Stage Example

Go applications can create a single binary.

```dockerfile id="ivwwue"
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY . .

RUN go build -o server .

FROM alpine:latest AS runtime

WORKDIR /app

COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
```

Meaning:

```text id="b0n24d"
Go builder image → compiles the application
Alpine runtime   → runs only the binary
```

## Multi-Stage Build Diagram

```text id="vokuyd"
Dockerfile
│
├── Stage 1: builder
│   ├── Install dependencies
│   ├── Build application
│   └── Prepare files
│
└── Stage 2: runtime
    ├── Copy only needed files
    ├── Expose port
    └── Start application
```

## COPY --from

The most important command in multi-stage builds is:

```dockerfile id="vaw0s4"
COPY --from=builder /source/path /destination/path
```

Example:

```dockerfile id="nzh5b4"
COPY --from=builder /app/dist /usr/share/nginx/html
```

Meaning:

```text id="u66daf"
Copy /app/dist from the builder stage
Put it inside /usr/share/nginx/html in the final stage
```

## Build Only a Specific Stage

You can build only one stage using `--target`.

Example:

```bash id="my0wpo"
docker build --target builder -t app-builder .
```

This is useful for debugging the build stage.

Example:

```bash id="pevf8h"
docker run -it --rm app-builder sh
```

## Compare Image Sizes

Build normal image:

```bash id="fizpjg"
docker build -t app-normal -f Dockerfile.normal .
```

Build multi-stage image:

```bash id="q1a2xt"
docker build -t app-multistage -f Dockerfile .
```

Check sizes:

```bash id="tvqwb5"
docker images
```

You should usually see that the multi-stage final image is smaller or cleaner.

## Multi-Stage with .dockerignore

Multi-stage builds are stronger when used with `.dockerignore`.

Example `.dockerignore`:

```text id="rumahv"
.git
.env
venv/
__pycache__/
*.pyc
*.log
node_modules/
dist/
build/
README.md
```

This keeps unnecessary files out of the build context.

## Multi-Stage with Non-Root User

For better security, run the final container as a non-root user.

Example:

```dockerfile id="4g8l6f"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN useradd --create-home appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .

ENV PATH=/home/appuser/.local/bin:$PATH

RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

This is better because the application does not run as root.

## Production Flask Multi-Stage Dockerfile

```dockerfile id="snx0nq"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN useradd --create-home appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

## Important Environment Variables

```dockerfile id="n7qy9v"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

Meaning:

```text id="agv7vb"
PYTHONDONTWRITEBYTECODE=1 → Do not create .pyc files
PYTHONUNBUFFERED=1        → Print logs directly without delay
```

These are useful for Python containers.

## Common Use Cases

Use multi-stage builds for:

```text id="hje6zl"
Frontend apps
Compiled apps
Python apps with build dependencies
Go apps
Java apps
Production Docker images
CI/CD Docker builds
```

## Benefits

```text id="jiapof"
Smaller final image
Less attack surface
Cleaner runtime environment
Better separation between build and runtime
No build tools in production image
Better for deployment
```

## Common Beginner Mistakes

### Forgetting COPY --from

Bad:

```dockerfile id="cis5di"
FROM node:20-alpine AS builder
RUN npm run build

FROM nginx:alpine
```

Nothing was copied from the builder stage.

Better:

```dockerfile id="dl7tme"
COPY --from=builder /app/dist /usr/share/nginx/html
```

### Copying Everything Again

Bad:

```dockerfile id="m1vncg"
COPY . .
```

in the final stage without need.

Better:

```dockerfile id="w6y4a7"
COPY --from=builder /app/dist /usr/share/nginx/html
```

Copy only what the final image needs.

### Using Large Final Image

Bad:

```dockerfile id="oc0hx2"
FROM python:3.12
```

Better:

```dockerfile id="nofsq5"
FROM python:3.12-slim
```

Use smaller runtime images when possible.

### Running as Root

Bad:

```text id="jji264"
Container runs as root by default
```

Better:

```dockerfile id="wy7d3j"
USER appuser
```

### Ignoring .dockerignore

Without `.dockerignore`, Docker may send unnecessary files to the build.

Better:

```text id="v4jzhb"
Use .dockerignore with multi-stage builds
```

## Useful Commands

Build image:

```bash id="s3sdyb"
docker build -t my-app:1.0.0 .
```

Build without cache:

```bash id="ypju09"
docker build --no-cache -t my-app:1.0.0 .
```

Build specific stage:

```bash id="mm8hrc"
docker build --target builder -t my-app-builder .
```

List images:

```bash id="gbmq0p"
docker images
```

Run container:

```bash id="wlbk4l"
docker run -d --name my-app -p 5000:5000 my-app:1.0.0
```

Check logs:

```bash id="zs01hm"
docker logs my-app
```

Enter container:

```bash id="dgy981"
docker exec -it my-app sh
```

Remove container:

```bash id="dhq6bb"
docker rm -f my-app
```

## Practical Lab

Create project:

```bash id="d32osw"
mkdir flask-multistage-lab
cd flask-multistage-lab
touch app.py requirements.txt Dockerfile .dockerignore
```

Add `requirements.txt`:

```text id="vl4j02"
flask
gunicorn
```

Add `app.py`:

```python id="l9ljre"
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker multi-stage build\n"
```

Add `.dockerignore`:

```text id="a18v2l"
.git
.env
venv/
__pycache__/
*.pyc
*.log
README.md
```

Add `Dockerfile`:

```dockerfile id="vywyih"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build:

```bash id="17c581"
docker build -t flask-multistage-lab:1.0.0 .
```

Run:

```bash id="p15j1x"
docker run -d \
  --name flask-multistage-lab \
  -p 5000:5000 \
  flask-multistage-lab:1.0.0
```

Test:

```bash id="kkoc3m"
curl http://localhost:5000
```

Clean up:

```bash id="8dsssk"
docker rm -f flask-multistage-lab
```

## Summary

```text id="m86it0"
Multi-stage build → Dockerfile with multiple stages
Builder stage     → Installs dependencies or builds the app
Runtime stage     → Runs the final application
COPY --from       → Copies files from one stage to another
--target          → Builds a specific stage
```

```text id="90b75o"
Use multi-stage builds to create smaller, cleaner, and safer Docker images.
```

> Multi-stage builds separate building from running, so the final Docker image contains only what the application needs.

