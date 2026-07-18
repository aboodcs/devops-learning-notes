# Docker Compose: Run a Multi-Container App Locally

**Docker Compose** lets us run multiple containers as one application using a single file:

```text
docker-compose.yml
```

This project contains two containers:

```text
Browser
   │
   ▼
Flask Container
   │
   ▼
Redis Container
```

* **Flask** runs the website.
* **Redis** stores the number of visits.

Repository:

```text
https://github.com/aboodcs/dockerized-flask-app
```

## Project Files

```text
dockerized-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## The Compose File

Your `docker-compose.yml` contains:

```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "5000:80"
    depends_on:
      - redis

  redis:
    image: redis:alpine
    container_name: redis
```

Your Compose file defines two services named `web` and `redis`.

## The `web` Service

```yaml
web:
  build: .
```

`web` is the Flask application container.

```yaml
build: .
```

This tells Docker Compose to find the `Dockerfile` in the current directory and build the Flask image.

Your Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
```

It installs Python and the project dependencies, copies the application files, and starts `app.py` on port `80`.

## Port Mapping

```yaml
ports:
  - "5000:80"
```

This means:

```text
Computer port 5000 → Flask container port 80
```

Therefore, you access the application using:

```text
http://localhost:5000
```

## The `redis` Service

```yaml
redis:
  image: redis:alpine
  container_name: redis
```

This creates a second container using the lightweight Redis image.

Redis stores the visit counter for the application.

## How Flask Connects to Redis

Your `app.py` contains:

```python
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)
```

The Flask application uses:

```python
host="redis"
```

because `redis` is the service name in the Compose file.

Docker Compose automatically creates a network where services can communicate using their service names.

## Application Routes

Your application has two routes.

### Home Route

Open:

```text
http://localhost:5000/
```

Output:

```text
Hello GitHub!
```

### Visit Counter Route

Open:

```text
http://localhost:5000/visit
```

Output:

```text
Visit count: 1
```

Refresh the page:

```text
Visit count: 2
```

Flask sends a request to Redis, and Redis increases the visit number.

## Start the Application

Clone the repository:

```bash
git clone https://github.com/aboodcs/dockerized-flask-app.git
cd dockerized-flask-app
```

Start both containers:

```bash
docker compose up --build
```

Run them in the background:

```bash
docker compose up -d --build
```

`docker compose up` builds, creates, and starts the application services.

## Check the Containers

```bash
docker compose ps
```

You should see two services:

```text
web
redis
```

View the logs:

```bash
docker compose logs -f
```

## Stop the Application

```bash
docker compose down
```

This stops and removes both containers.


## Summary

```text
Dockerfile          → Builds the Flask image
web service         → Runs the Flask application
redis service       → Stores the visit counter
ports               → Opens Flask on localhost:5000
depends_on          → Starts Redis with the Flask service
docker compose up   → Starts the complete application
docker compose down → Stops the complete application
```

> Docker Compose runs your Flask application and Redis together with one command.

