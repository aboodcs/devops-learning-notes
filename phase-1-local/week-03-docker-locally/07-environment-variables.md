# 07 - Environment Variables

**Environment variables** are values passed to an application from outside the code.

They are used to configure containers without changing the application files.

```text id="zf0k7m"
Application code stays the same
Environment variables change the behavior
```

Example:

```text id="a12np8"
APP_ENV=development
PORT=5000
DATABASE_HOST=db
REDIS_HOST=redis
```

## Simple Explanation

Instead of writing configuration directly inside the code:

```python id="th6d4z"
database_host = "localhost"
```

You can read it from an environment variable:

```python id="xl7y4s"
database_host = os.getenv("DATABASE_HOST")
```

Now the same application can run in different environments:

```text id="d7hxlc"
Development → DATABASE_HOST=localhost
Docker      → DATABASE_HOST=redis
Production  → DATABASE_HOST=prod-db
```

## Why Do We Use Environment Variables?

Environment variables help with:

```text id="kvq7lg"
Application configuration
Docker container configuration
Different environments
Avoiding hardcoded values
CI/CD pipelines
Docker Compose
Kubernetes ConfigMaps and Secrets
```

## Common Examples

```text id="nswo7f"
APP_ENV=development
APP_PORT=5000
DEBUG=true
DATABASE_HOST=postgres
DATABASE_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
UPLOAD_DIR=/app/uploads
```

## Bad Practice

Hardcoding values inside the application is bad.

```python id="dwl3d7"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

Why is this bad?

```text id="ri4gue"
The app works only in one environment
Changing configuration requires code changes
Docker containers may not reach localhost correctly
Production becomes harder to manage
```

## Better Practice

Read configuration from environment variables.

```python id="ixwt79"
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
```

Meaning:

```text id="ypzmlh"
Use REDIS_HOST from environment
If not found, use localhost
Use REDIS_PORT from environment
If not found, use 6379
```

## Environment Variables in Docker

You can pass environment variables to a container using `-e`.

Example:

```bash id="mg0gdr"
docker run -d \
  --name my-app \
  -e APP_ENV=development \
  -e APP_PORT=5000 \
  my-app:1.0.0
```

Meaning:

```text id="wtz7u2"
APP_ENV=development is available inside the container
APP_PORT=5000 is available inside the container
```

## Check Environment Variables Inside Container

Run a test container:

```bash id="gqobtr"
docker run -it --rm \
  -e APP_ENV=development \
  alpine sh
```

Inside the container:

```bash id="y9rsy3"
printenv
```

Or check one variable:

```bash id="xr00oq"
echo $APP_ENV
```

You should see:

```text id="eocuo5"
development
```

## Example with Nginx

Run Nginx with an environment variable:

```bash id="bts7rs"
docker run -d \
  --name nginx-env \
  -e APP_NAME=nginx-demo \
  nginx:alpine
```

Check inside:

```bash id="j8x2u4"
docker exec -it nginx-env sh
```

Then:

```bash id="wrvvya"
echo $APP_NAME
```

Exit:

```bash id="xsl8ru"
exit
```

## Using --env-file

Instead of writing many `-e` flags, you can use an environment file.

Create `.env`:

```text id="m6z37x"
APP_ENV=development
APP_PORT=5000
REDIS_HOST=redis
REDIS_PORT=6379
```

Run container:

```bash id="xvscjl"
docker run -d \
  --name my-app \
  --env-file .env \
  my-app:1.0.0
```

This passes all variables from `.env` into the container.

## Important Security Note

Do not push real `.env` files to GitHub.

`.env` files may contain secrets.

Example:

```text id="zdlogg"
DATABASE_PASSWORD=secret123
API_KEY=abcd1234
TOKEN=my-private-token
```

Add `.env` to `.gitignore`:

```text id="ojb5ec"
.env
.env.*
```

You can create `.env.example` without real secrets:

```text id="jmb3w7"
APP_ENV=development
APP_PORT=5000
DATABASE_HOST=change-me
DATABASE_PASSWORD=change-me
```

## Environment Variables in Docker Compose

Docker Compose makes environment variables easier.

Example `docker-compose.yml`:

```yaml id="zawltv"
services:
  web:
    image: my-app:1.0.0
    ports:
      - "5000:5000"
    environment:
      APP_ENV: development
      REDIS_HOST: redis
      REDIS_PORT: 6379

  redis:
    image: redis:7-alpine
```

Here, the `web` container can use:

```text id="n7qvwq"
REDIS_HOST=redis
REDIS_PORT=6379
```

The hostname `redis` works because Docker Compose creates a network and service name automatically.

## Docker Compose with env_file

You can also use an `.env` file.

```yaml id="sq9ji8"
services:
  web:
    image: my-app:1.0.0
    ports:
      - "5000:5000"
    env_file:
      - .env
```

`.env`:

```text id="qy9ccx"
APP_ENV=development
APP_PORT=5000
REDIS_HOST=redis
REDIS_PORT=6379
```

## .env in Docker Compose

Docker Compose also reads a `.env` file for variable substitution.

Example `.env`:

```text id="imcedw"
APP_VERSION=1.0.0
HOST_PORT=5000
CONTAINER_PORT=5000
```

`docker-compose.yml`:

```yaml id="uxr54c"
services:
  web:
    image: my-app:${APP_VERSION}
    ports:
      - "${HOST_PORT}:${CONTAINER_PORT}"
```

This becomes:

```yaml id="kpyo08"
services:
  web:
    image: my-app:1.0.0
    ports:
      - "5000:5000"
```

## env_file vs environment

| Option              | Meaning                                      |
| ------------------- | -------------------------------------------- |
| `environment`       | Write variables directly inside compose file |
| `env_file`          | Load variables from a file                   |
| `.env` substitution | Replace values inside compose file           |

Example:

```yaml id="v6w5ly"
environment:
  APP_ENV: development
```

Example:

```yaml id="avqnv4"
env_file:
  - .env
```

Example:

```yaml id="iw0kfn"
image: my-app:${APP_VERSION}
```

## Practical Flask Example

Project structure:

```text id="m3f9tf"
flask-env-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── .gitignore
```

## app.py

```python id="n98yja"
import os
from flask import Flask

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "flask-app")

@app.route("/")
def home():
    return f"Hello from {APP_NAME}. Environment: {APP_ENV}\n"

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
```

## requirements.txt

```text id="mjs8qo"
flask
```

## Dockerfile

```dockerfile id="qykq5p"
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

## .env

```text id="xu90ir"
APP_NAME=env-demo-app
APP_ENV=development
APP_PORT=5000
```

## .gitignore

```text id="qxq6rs"
.env
__pycache__/
*.pyc
```

## docker-compose.yml

```yaml id="y9td1z"
services:
  web:
    build: .
    container_name: flask-env-app
    ports:
      - "5000:5000"
    env_file:
      - .env
```

## Run the App

Build and start:

```bash id="ri3ef2"
docker compose up --build
```

Open:

```text id="d3e9oy"
http://localhost:5000
```

Expected output:

```text id="glvhgz"
Hello from env-demo-app. Environment: development
```

## Change Environment Without Changing Code

Edit `.env`:

```text id="afbi4z"
APP_NAME=production-demo
APP_ENV=production
APP_PORT=5000
```

Restart:

```bash id="vvjtf7"
docker compose down
docker compose up --build
```

Now the app uses the new values.

## Environment Variables Inside Dockerfile

You can define environment variables inside a Dockerfile using `ENV`.

Example:

```dockerfile id="n4asce"
ENV APP_ENV=production
ENV APP_PORT=5000
```

Full example:

```dockerfile id="wbna55"
FROM python:3.12-slim

WORKDIR /app

ENV APP_ENV=production
ENV APP_PORT=5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

## ENV vs docker run -e

| Method                | Meaning                               |
| --------------------- | ------------------------------------- |
| `ENV` in Dockerfile   | Default value inside the image        |
| `docker run -e`       | Override value when running container |
| `env_file`            | Load values from file                 |
| Compose `environment` | Set values in compose file            |

Example:

```dockerfile id="u7ih6u"
ENV APP_ENV=production
```

Override it:

```bash id="tj7fab"
docker run -e APP_ENV=development my-app:1.0.0
```

The container will use:

```text id="ol2ib3"
APP_ENV=development
```

## Secrets vs Environment Variables

Environment variables are useful, but they are not perfect for secrets.

They can sometimes be visible through:

```text id="rwcr37"
Container inspection
Logs
Process environment
CI/CD settings
Misconfiguration
```

For simple labs, `.env` is okay.

For real production, use secret management tools.

Examples:

```text id="vlpgt0"
Docker secrets
Kubernetes Secrets
GitHub Actions Secrets
OCI Vault
AWS Secrets Manager
HashiCorp Vault
```

## Check Container Environment

Show environment variables of a running container:

```bash id="v1qa32"
docker exec CONTAINER_NAME printenv
```

Example:

```bash id="g9y0zw"
docker exec flask-env-app printenv
```

Check one variable:

```bash id="p8iy45"
docker exec flask-env-app printenv APP_ENV
```

## Inspect Environment Variables

You can inspect container configuration:

```bash id="n5vfl2"
docker inspect flask-env-app
```

Filter environment variables:

```bash id="adv730"
docker inspect flask-env-app --format='{{range .Config.Env}}{{println .}}{{end}}'
```

## Common Beginner Mistakes

### Hardcoding localhost

Bad inside Docker:

```text id="kl3v33"
REDIS_HOST=localhost
```

If Redis is in another container, `localhost` means the same container, not the Redis container.

Better in Docker Compose:

```text id="h127oa"
REDIS_HOST=redis
```

### Pushing .env to GitHub

Bad:

```text id="kzffbw"
.env uploaded to GitHub
```

Better:

```text id="nchp6e"
Add .env to .gitignore
Use .env.example for documentation
```

### Forgetting to Recreate Container

If you change environment variables, restart the container.

```bash id="csb2ko"
docker compose down
docker compose up -d
```

or:

```bash id="kqmnzf"
docker rm -f my-app
docker run ...
```

### Wrong Variable Name

The app must read the same variable name you pass.

Bad:

```text id="xj1rnx"
Docker: REDIS_HOST=redis
App reads: REDIS_SERVER
```

Better:

```text id="b7k9q7"
Docker: REDIS_HOST=redis
App reads: REDIS_HOST
```

### Spaces Around = in .env

Bad:

```text id="lrjiox"
APP_ENV = development
```

Better:

```text id="dp7yvi"
APP_ENV=development
```

## Useful Commands

Run with one environment variable:

```bash id="vzs6fr"
docker run -e APP_ENV=development my-app:1.0.0
```

Run with many environment variables:

```bash id="yleg5p"
docker run -e APP_ENV=development -e APP_PORT=5000 my-app:1.0.0
```

Run with env file:

```bash id="kxh3bd"
docker run --env-file .env my-app:1.0.0
```

Check variables inside container:

```bash id="hpxat0"
docker exec CONTAINER_NAME printenv
```

Use Docker Compose:

```bash id="gu43hi"
docker compose up --build
```

Stop Docker Compose:

```bash id="r15xsy"
docker compose down
```

## Summary

```text id="pb15yw"
Environment variable → External configuration value
.env file            → File containing environment variables
-e                   → Pass variable with docker run
--env-file           → Load variables from a file
environment          → Set variables in Docker Compose
env_file             → Load env file in Docker Compose
ENV                  → Default environment variable in Dockerfile
```

> Environment variables let you configure Docker containers without changing the application code.

