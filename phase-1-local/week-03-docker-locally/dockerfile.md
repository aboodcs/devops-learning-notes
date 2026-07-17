# Write a Dockerfile from Scratch

A **Dockerfile** is a text file containing instructions that Docker uses to build a Docker image.

The process is:

```text
Dockerfile → Docker Image → Docker Container
```

## Practical Example

This guide uses a simple Flask application.

You can view the complete project here:

[Dockerized Flask App on GitHub](https://github.com/aboodcs/dockerized-flask-app)

## Project Structure

```text
my-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

## 1. Create the Application

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker!"

app.run(host="0.0.0.0", port=5000)
```

Create `requirements.txt`:

```text
flask
```

## 2. Create the Dockerfile

Create a file named:

```text
Dockerfile
```

Add:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Dockerfile Explanation

### `FROM`

```dockerfile
FROM python:3.12-slim
```

Chooses the base image.

This image already contains Python.

### `WORKDIR`

```dockerfile
WORKDIR /app
```

Creates and selects `/app` as the working directory inside the image.

### `COPY`

```dockerfile
COPY requirements.txt .
```

Copies `requirements.txt` from the project folder into the image.

### `RUN`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Installs the Python dependencies while building the image.

### Copy the Application

```dockerfile
COPY . .
```

Copies the remaining project files into the image.

### `EXPOSE`

```dockerfile
EXPOSE 5000
```

Documents that the application uses port `5000`.

`EXPOSE` does not publish the port by itself. The port is published when running the container with `-p`.

### `CMD`

```dockerfile
CMD ["python", "app.py"]
```

Defines the command that runs when the container starts.

## 3. Build the Image

Run this command inside the project directory:

```bash
docker build -t my-python-app .
```

* `docker build` builds the image.
* `-t my-python-app` gives the image a name.
* `.` tells Docker to use the current directory as the build context.

## 4. Run the Container

```bash
docker run -d -p 5000:5000 --name my-container my-python-app
```

The port mapping means:

```text
Host port 5000 → Container port 5000
```

Open:

```text
http://localhost:5000
```

You should see:

```text
Hello from Docker!
```

## 5. Useful Commands

View running containers:

```bash
docker ps
```

View container logs:

```bash
docker logs my-container
```

Stop the container:

```bash
docker stop my-container
```

Remove the container:

```bash
docker rm my-container
```

Remove the image:

```bash
docker rmi my-python-app
```

## Summary

```text
FROM      → Choose the base image
WORKDIR   → Set the working directory
COPY      → Copy files into the image
RUN       → Run commands during the image build
EXPOSE    → Document the application port
CMD       → Start the application
```

> A Dockerfile is the recipe, the image is the built result, and the container is the running application.

## Example Repository

The complete working example is available here:

https://github.com/aboodcs/dockerized-flask-app

