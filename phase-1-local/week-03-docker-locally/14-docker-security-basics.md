# 14 - Docker Security Basics

Docker security means running containers in a safer way.

A container is isolated, but it is not automatically secure.

You still need to protect:

```text id="11vp49"
Images
Containers
Secrets
Networks
Volumes
Host machine
Docker daemon
```

## Simple Explanation

Docker makes applications easier to run, but bad configuration can create security problems.

```text id="q9l1fp"
Bad Docker setup → secrets leaked, ports exposed, root access risk
Good Docker setup → smaller images, limited access, safer containers
```

## Why Docker Security Matters

Containers can contain:

```text id="ha0efz"
Application code
Environment variables
Database passwords
API keys
Private files
Configuration files
```

If you build or run containers incorrectly, you may expose sensitive data.

## Main Docker Security Rules

```text id="ryxj7p"
Use trusted images
Use small base images
Do not run as root
Do not store secrets in images
Expose only needed ports
Use .dockerignore
Limit CPU and memory
Use read-only filesystems when possible
Scan images
Keep images updated
Protect volumes
Do not mount Docker socket
```

## 1. Use Trusted Images

Use official or trusted images.

Good examples:

```text id="yo50dj"
nginx:alpine
redis:7-alpine
postgres:16-alpine
python:3.12-slim
```

Bad idea:

```text id="t5gxcz"
Using random unknown images from the internet
```

Pull image:

```bash id="drp4iq"
docker pull nginx:alpine
```

Check images:

```bash id="0c92dm"
docker images
```

## 2. Use Specific Tags

Avoid using only `latest` in real projects.

Bad:

```dockerfile id="nvqiin"
FROM python:latest
```

Better:

```dockerfile id="0lxooi"
FROM python:3.12-slim
```

Why?

```text id="vzusj9"
latest can change without warning
specific tags make builds more predictable
rollback becomes easier
```

## 3. Use Small Base Images

Small images usually contain fewer unnecessary packages.

Good examples:

```dockerfile id="nbyzzn"
FROM python:3.12-slim
```

```dockerfile id="quf4hi"
FROM nginx:alpine
```

Benefits:

```text id="lgwu26"
Smaller image size
Fewer packages
Smaller attack surface
Faster pull and push
```

## 4. Do Not Run Containers as Root

By default, many containers run as root.

This is not always safe.

Bad:

```dockerfile id="c0v9lq"
FROM python:3.12-slim

WORKDIR /app

COPY . .

CMD ["python", "app.py"]
```

Better:

```dockerfile id="t48qzt"
FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home appuser

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
```

Check user inside container:

```bash id="fasu7k"
docker exec CONTAINER_NAME whoami
```

## Why Non-Root Is Better

If the application is compromised, the attacker gets fewer permissions inside the container.

```text id="ptmold"
root user    → more dangerous
normal user  → safer
```

## 5. Do Not Store Secrets in Dockerfile

Never put passwords or API keys inside Dockerfile.

Bad:

```dockerfile id="g3lrzs"
ENV DATABASE_PASSWORD=my-secret-password
ENV API_KEY=abcd1234
```

Why bad?

```text id="rs634v"
Secrets may stay in image history
Anyone with image access may see them
Hard to rotate secrets safely
```

Better:

```bash id="f3660d"
docker run -e DATABASE_PASSWORD=change-me my-app:1.0.0
```

For real projects, use secret managers.

Examples:

```text id="6xlwqf"
Docker secrets
Kubernetes Secrets
GitHub Actions Secrets
OCI Vault
HashiCorp Vault
```

## 6. Protect .env Files

`.env` files often contain sensitive values.

Example:

```text id="sdkbyy"
DATABASE_USER=admin
DATABASE_PASSWORD=secret123
API_KEY=private-key
```

Do not push `.env` to GitHub.

Add to `.gitignore`:

```text id="fxkf43"
.env
.env.*
```

Add to `.dockerignore`:

```text id="xdogq8"
.env
.env.*
```

Use `.env.example` instead:

```text id="h3btyv"
DATABASE_USER=change-me
DATABASE_PASSWORD=change-me
API_KEY=change-me
```

## 7. Use .dockerignore

`.dockerignore` prevents unnecessary files from entering the Docker build context.

Good `.dockerignore`:

```text id="utmv2n"
.git
.env
.env.*
*.pem
*.key
venv/
__pycache__/
*.pyc
*.log
node_modules/
.terraform/
*.tfstate
*.tfstate.backup
```

This protects against copying:

```text id="lr6n0u"
Secrets
Git history
Local virtual environments
Terraform state
Private keys
Logs
```

## 8. Expose Only Needed Ports

Do not expose ports randomly.

Bad:

```bash id="ofwijc"
docker run -p 0.0.0.0:5432:5432 postgres:16-alpine
```

This exposes PostgreSQL to the network.

Better:

```bash id="5e0g5u"
docker run -d \
  --name postgres-db \
  --network app-network \
  -e POSTGRES_PASSWORD=123abood \
  postgres:16-alpine
```

Only expose public services.

Example web app:

```bash id="l7pmfw"
docker run -d \
  --name web \
  -p 8080:80 \
  nginx:alpine
```

## Common Port Rule

```text id="de0xjh"
Web app     → expose port 80, 443, or app port
Database    → keep private inside Docker network
Redis       → keep private inside Docker network
Internal API → keep private unless needed
```

## 9. Use Docker Networks

Use custom Docker networks instead of connecting everything randomly.

Create network:

```bash id="y99sc8"
docker network create app-network
```

Run web container:

```bash id="6y2d13"
docker run -d \
  --name web \
  --network app-network \
  -p 8080:80 \
  nginx:alpine
```

Run Redis privately:

```bash id="7u0upx"
docker run -d \
  --name redis \
  --network app-network \
  redis:7-alpine
```

Now containers can communicate by name:

```text id="pfcxsk"
web → redis
```

Redis does not need to be exposed to the host.

## 10. Use Read-Only Filesystem

Some containers do not need to write to the filesystem.

Run with read-only mode:

```bash id="xyrz39"
docker run -d \
  --name nginx-readonly \
  --read-only \
  --tmpfs /tmp \
  -p 8080:80 \
  nginx:alpine
```

Meaning:

```text id="nki0xz"
--read-only → container filesystem cannot be changed
--tmpfs /tmp → temporary writable space
```

This reduces damage if the container is compromised.

## 11. Limit CPU and Memory

Do not allow one container to use all host resources.

Limit memory:

```bash id="i6s7tn"
docker run -d \
  --name web \
  --memory="256m" \
  nginx:alpine
```

Limit CPU:

```bash id="ogssxn"
docker run -d \
  --name web \
  --cpus="0.5" \
  nginx:alpine
```

Use both:

```bash id="ocbtup"
docker run -d \
  --name web \
  --memory="256m" \
  --cpus="0.5" \
  nginx:alpine
```

Check usage:

```bash id="0rxoe5"
docker stats
```

## 12. Drop Linux Capabilities

Containers can have Linux capabilities.

You can remove unnecessary capabilities.

More secure:

```bash id="dytt3k"
docker run -d \
  --name web \
  --cap-drop ALL \
  nginx:alpine
```

Sometimes an app needs a specific capability.

Example:

```bash id="f7k0qo"
docker run -d \
  --name web \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  nginx:alpine
```

Use this carefully.

## 13. Use no-new-privileges

This prevents processes from gaining extra privileges.

```bash id="o3brqz"
docker run -d \
  --name web \
  --security-opt no-new-privileges:true \
  nginx:alpine
```

This is a good security option for many containers.

## 14. Protect Volumes

Volumes can contain important data.

Example:

```text id="epbqmf"
Database files
Uploaded files
Application data
Configuration files
```

Do not delete volumes without checking.

List volumes:

```bash id="1ugrzb"
docker volume ls
```

Inspect volume:

```bash id="8462o6"
docker volume inspect VOLUME_NAME
```

Be careful with:

```bash id="6hd4wv"
docker volume prune
```

This deletes unused volumes.

## 15. Use Read-Only Mounts for Config Files

If a container only needs to read a config file, mount it as read-only.

```bash id="all8sn"
docker run -d \
  --name app \
  -v $(pwd)/config.yml:/app/config.yml:ro \
  my-app:1.0.0
```

The `:ro` means:

```text id="db5lrr"
read-only
```

The container can read the file but cannot change it.

## 16. Do Not Mount Docker Socket

This is dangerous:

```bash id="oz6cse"
-v /var/run/docker.sock:/var/run/docker.sock
```

Why?

```text id="sgskv5"
The container can control Docker on the host
It may start or delete containers
It may access sensitive host resources
```

Avoid mounting Docker socket unless you fully understand the risk.

## 17. Scan Docker Images

Image scanning checks for known vulnerabilities.

With Docker Scout:

```bash id="6y169p"
docker scout quickview nginx:alpine
```

Check CVEs:

```bash id="s9ogpb"
docker scout cves nginx:alpine
```

You can also use tools like:

```text id="i8i7bw"
Trivy
Grype
Snyk
Docker Scout
```

## 18. Keep Images Updated

Old images may contain vulnerable packages.

Update image:

```bash id="ko6u28"
docker pull nginx:alpine
```

Rebuild your app:

```bash id="rakimx"
docker build --no-cache -t my-app:1.0.1 .
```

Run new version:

```bash id="w90dhs"
docker rm -f my-app
docker run -d --name my-app my-app:1.0.1
```

## 19. Use Multi-Stage Builds

Multi-stage builds keep build tools out of the final image.

Example:

```dockerfile id="yy4riq"
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

Benefits:

```text id="v09ynj"
Smaller final image
Cleaner runtime
Fewer unnecessary packages
Better security
```

## 20. Docker Compose Security Example

Example `docker-compose.yml`:

```yaml id="pr1q1t"
services:
  web:
    image: nginx:alpine
    container_name: secure-nginx
    ports:
      - "8080:80"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
      - /var/run
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    mem_limit: 256m
    cpus: 0.5
    networks:
      - app-network

networks:
  app-network:
```

Run:

```bash id="nf1lx9"
docker compose up -d
```

Check:

```bash id="fqhbc9"
docker compose ps
```

## Secure Docker Run Example

```bash id="j80n1j"
docker run -d \
  --name secure-web \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory="256m" \
  --cpus="0.5" \
  -p 8080:80 \
  nginx:alpine
```

This container is safer because:

```text id="tdrwbp"
Filesystem is read-only
Capabilities are dropped
Privilege escalation is blocked
Memory is limited
CPU is limited
Only port 8080 is exposed
```

## Common Beginner Mistakes

### Running Everything as Root

Bad:

```text id="b2z72t"
Container runs as root
```

Better:

```dockerfile id="89m1hl"
USER appuser
```

### Putting Secrets in Image

Bad:

```dockerfile id="88rubv"
ENV API_KEY=my-real-api-key
```

Better:

```text id="5xcl7z"
Use environment variables or secret manager at runtime
```

### Exposing Database Ports

Bad:

```bash id="l4p1kh"
-p 5432:5432
```

Better:

```text id="9ukz8b"
Keep database inside private Docker network
```

### Using latest Everywhere

Bad:

```dockerfile id="imx9qo"
FROM python:latest
```

Better:

```dockerfile id="d506ci"
FROM python:3.12-slim
```

### Ignoring .dockerignore

Bad:

```text id="y9ie7b"
No .dockerignore file
```

Better:

```text id="kkaj6m"
Use .dockerignore to keep secrets and unnecessary files out
```

### Giving Containers Too Many Permissions

Bad:

```bash id="j6ls5m"
docker run --privileged my-app
```

Better:

```text id="jegcg2"
Avoid --privileged unless absolutely required
```

## Dangerous Commands to Avoid

Avoid these unless you understand them:

```bash id="gypdp1"
docker run --privileged IMAGE
```

```bash id="i9mu5b"
docker run -v /:/host IMAGE
```

```bash id="obzszu"
docker run -v /var/run/docker.sock:/var/run/docker.sock IMAGE
```

These can give the container too much access to the host.

## Practical Security Checklist

Before running a container, ask:

```text id="m76bvr"
Is the image trusted?
Is the tag specific?
Does the container run as non-root?
Are secrets outside the image?
Is .dockerignore used?
Are only required ports exposed?
Are CPU and memory limited?
Are volumes protected?
Is the Docker socket not mounted?
Is the image scanned?
```

## Useful Commands

Check running containers:

```bash id="2f8zkw"
docker ps
```

Check image history:

```bash id="6jes4w"
docker history IMAGE_NAME
```

Inspect container:

```bash id="i9tgce"
docker inspect CONTAINER_NAME
```

Check container user:

```bash id="3sr12m"
docker exec CONTAINER_NAME whoami
```

Check environment variables:

```bash id="gn9hq5"
docker exec CONTAINER_NAME printenv
```

Check exposed ports:

```bash id="whmfb6"
docker port CONTAINER_NAME
```

Check resource usage:

```bash id="q5adki"
docker stats
```

Scan image:

```bash id="akgefl"
docker scout cves IMAGE_NAME
```

List volumes:

```bash id="e5rt4s"
docker volume ls
```

List networks:

```bash id="zjwtiq"
docker network ls
```

## Summary

```text id="syyrvy"
Use trusted images
Use specific tags
Use small base images
Run as non-root
Do not store secrets in images
Use .dockerignore
Expose only needed ports
Use private Docker networks
Limit CPU and memory
Use read-only mode when possible
Drop unnecessary capabilities
Scan images
Protect volumes
Avoid Docker socket mounts
```

> Docker security basics are about reducing risk: use trusted images, protect secrets, limit permissions, expose only what is needed, and keep containers small and controlled.

