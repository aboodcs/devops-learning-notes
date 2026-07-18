# Docker: Images, Containers, and Volumes

Docker uses three important parts:

* **Image**
* **Container**
* **Volume**

## 1. Docker Image

A Docker image is a **template** used to create containers.

It contains:

* The application
* Libraries
* Dependencies
* Configuration needed to run the application

An image does not run by itself.

Example:

```bash
docker pull nginx
```

This downloads the Nginx image.

Think of an image as a **blueprint**.

---

## 2. Docker Container

A container is a **running instance of an image**.

When you start an image, Docker creates a container from it.

Example:

```bash
docker run -d nginx
```

This creates and runs an Nginx container.

You can create many containers from the same image.

```text
Nginx Image
├── Container 1
├── Container 2
└── Container 3
```

Each container runs separately.

Think of a container as the **real object created from the blueprint**.

---

## 3. Docker Volume

A volume stores data outside the container.

Containers can be deleted, and their internal data may be lost.

Volumes keep important data safe.

Example:

```bash
docker run -d \
  -v nginx-data:/usr/share/nginx/html \
  nginx
```

Here:

* `nginx-data` is the volume
* `/usr/share/nginx/html` is the folder inside the container

Volumes are commonly used for:

* Databases
* Uploaded files
* Application data
* Configuration files

---

## How They Work Together

```text
Docker Image
     │
     ▼
Docker Container
     │
     ▼
Docker Volume
```

* The **image** provides the application.
* The **container** runs the application.
* The **volume** stores the application data.

## Simple Example

Imagine a database application:

* The image contains MySQL.
* The container runs MySQL.
* The volume stores the database files.

If the container is deleted, the volume can keep the database data.

## Summary

> An image is the template.

> A container is the running application.

> A volume stores persistent data.

