# 04 - Docker Images and Tags

A **Docker image** is a template used to create containers.

A **Docker tag** is a label used to identify a specific version of an image.

```text id="d8q1ws"
Docker Image → Template
Docker Tag   → Version or label
Container    → Running copy of an image
```

## Simple Explanation

Think of it like this:

```text id="sz7jwi"
Image → Class
Container → Object created from that class
Tag → Version of the class
```

Example:

```text id="xn4m9z"
nginx:alpine
```

Meaning:

```text id="to8v6k"
nginx  → Image name
alpine → Tag
```

## Why Do We Need Docker Images?

A Docker image contains everything needed to run an application.

It can include:

```text id="rcavem"
Operating system files
Application code
Dependencies
Runtime
Configuration
Default command
```

Example:

```text id="o7q94t"
Python Flask app image
├── Python runtime
├── Flask dependency
├── Application files
└── Command to start the app
```

## Image vs Container

| Image                         | Container                   |
| ----------------------------- | --------------------------- |
| Template                      | Running or stopped instance |
| Read-only                     | Has writable layer          |
| Used to create containers     | Created from an image       |
| Stored locally or in registry | Runs on Docker Engine       |

Example:

```text id="a4nl1g"
Image: nginx:alpine
Container: web
```

Run a container from the image:

```bash id="jwah7k"
docker run -d --name web -p 8080:80 nginx:alpine
```

## Docker Image Name Format

Docker image names usually look like this:

```text id="m7to27"
image-name:tag
```

Example:

```text id="12yswq"
nginx:alpine
redis:7
python:3.12-slim
postgres:16-alpine
```

Full image format:

```text id="g29h0b"
registry/username/image-name:tag
```

Example:

```text id="pyp29v"
docker.io/library/nginx:alpine
```

## What Is a Docker Tag?

A **tag** identifies a specific image version.

Example:

```text id="13meul"
python:3.12
python:3.12-slim
python:3.11
python:latest
```

Same image name, different tags.

```text id="z45d87"
python → image name
3.12   → tag
```

## Why Tags Are Important

Tags help you control which image version you use.

Bad:

```text id="59h8jh"
nginx:latest
```

Better:

```text id="h4u3nf"
nginx:1.27-alpine
```

Using clear tags helps with:

```text id="m74g8q"
Repeatable builds
Stable deployments
Rollback
Debugging
Security updates
Production control
```

## The latest Tag

If you run an image without a tag, Docker uses `latest` by default.

This:

```bash id="ivx6l9"
docker pull nginx
```

is similar to:

```bash id="n120x7"
docker pull nginx:latest
```

But `latest` does not always mean newest stable version.

It is just a tag name.

## Why Avoid latest in Real Projects?

Using `latest` can be risky.

Example:

```text id="g7f9fy"
Today: nginx:latest points to version A
Tomorrow: nginx:latest points to version B
```

Your project may change without you noticing.

Better:

```text id="ggn5yc"
nginx:1.27-alpine
python:3.12-slim
postgres:16-alpine
redis:7-alpine
```

## Pull an Image

To download an image from a registry:

```bash id="g3e24x"
docker pull nginx:alpine
```

Pull Python image:

```bash id="rppfg2"
docker pull python:3.12-slim
```

Pull Redis image:

```bash id="ws3x16"
docker pull redis:7-alpine
```

## List Images

Show local images:

```bash id="uxarqd"
docker images
```

or:

```bash id="xsqoo7"
docker image ls
```

Example output:

```text id="ktpnod"
REPOSITORY   TAG          IMAGE ID       SIZE
nginx        alpine       abc123         48MB
python       3.12-slim    def456         130MB
redis        7-alpine     ghi789         41MB
```

## Image ID

Each image has an Image ID.

Example:

```text id="0gdvf7"
IMAGE ID: abc123
```

Docker uses this ID internally.

You usually work with the image name and tag:

```text id="fy7pmy"
nginx:alpine
```

## Run a Container from an Image

```bash id="i9z2jw"
docker run -d --name web -p 8080:80 nginx:alpine
```

This does:

```text id="obtf1q"
1. Looks for nginx:alpine locally
2. If not found, pulls it from registry
3. Creates a container
4. Starts the container
```

## Build a Custom Image

You can build your own image using a Dockerfile.

Example project:

```text id="40wd5p"
my-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

Example Dockerfile:

```dockerfile id="gxzfln"
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Build the image:

```bash id="c1z17l"
docker build -t my-flask-app:1.0.0 .
```

Meaning:

```text id="hqxhw3"
-t my-flask-app:1.0.0 → Image name and tag
.                       → Build context is current folder
```

## Tag an Image

You can add another tag to an existing image.

```bash id="3g9v8h"
docker tag my-flask-app:1.0.0 my-flask-app:latest
```

Now the same image has two tags:

```text id="9ds5qo"
my-flask-app:1.0.0
my-flask-app:latest
```

## Tag for Docker Hub

Docker Hub image format:

```text id="fxn0yu"
username/image-name:tag
```

Example:

```bash id="yw4542"
docker tag my-flask-app:1.0.0 aboodcs/my-flask-app:1.0.0
```

Push it:

```bash id="d4kkjw"
docker push aboodcs/my-flask-app:1.0.0
```

## Tag for GitHub Container Registry

GitHub Container Registry format:

```text id="w1f87z"
ghcr.io/username/image-name:tag
```

Example:

```bash id="agiu0n"
docker tag my-flask-app:1.0.0 ghcr.io/aboodcs/my-flask-app:1.0.0
```

Push it:

```bash id="kb2gie"
docker push ghcr.io/aboodcs/my-flask-app:1.0.0
```

## Image Versioning

Use meaningful tags.

Good examples:

```text id="9s22ob"
my-app:1.0.0
my-app:1.1.0
my-app:1.1.1
my-app:dev
my-app:staging
my-app:prod
```

Bad examples:

```text id="3dps85"
my-app:test
my-app:new
my-app:final
my-app:final2
my-app:latest-only
```

## Semantic Versioning with Images

Docker tags often follow Semantic Versioning.

```text id="m4jxc5"
MAJOR.MINOR.PATCH
```

Example:

```text id="uwg1ly"
my-app:1.0.0
```

Meaning:

```text id="l44hqz"
1 → Major
0 → Minor
0 → Patch
```

Simple rule:

```text id="olbxwy"
PATCH → Bug fix
MINOR → New feature
MAJOR → Breaking change
```

Examples:

```text id="aoklkf"
Bug fix         → my-app:1.0.1
New feature     → my-app:1.1.0
Breaking change → my-app:2.0.0
```

## Image Layers

Docker images are built from layers.

Each Dockerfile instruction can create a layer.

Example:

```dockerfile id="p61ylf"
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Simple idea:

```text id="h70a81"
Base image layer
Dependency layer
Application code layer
Command layer
```

Docker uses layers to make builds faster.

## Why Layer Order Matters

Better Dockerfile:

```dockerfile id="lwq6kh"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Why?

```text id="mqq2qu"
Dependencies change less often
Application code changes more often
Docker can reuse cached dependency layer
```

Bad Dockerfile:

```dockerfile id="mqcgqf"
COPY . .
RUN pip install -r requirements.txt
```

This can make builds slower because every code change may reinstall dependencies.

## Inspect an Image

Show image details:

```bash id="qi5gid"
docker image inspect nginx:alpine
```

Show image history:

```bash id="ytnkqq"
docker history nginx:alpine
```

This shows the layers used to build the image.

## Remove Images

Remove one image:

```bash id="ze58di"
docker rmi nginx:alpine
```

Remove unused images:

```bash id="fn2std"
docker image prune
```

Remove all unused images:

```bash id="gtk86w"
docker image prune -a
```

Be careful with cleanup commands.

## Dangling Images

A dangling image is an image without a name or tag.

It may appear like this:

```text id="gblw87"
<none>   <none>
```

Remove dangling images:

```bash id="or8xlv"
docker image prune
```

## Save and Load Images

You can save an image as a file.

Save:

```bash id="iuvoia"
docker save -o my-app.tar my-flask-app:1.0.0
```

Load:

```bash id="xsey3l"
docker load -i my-app.tar
```

This is useful when moving images without a registry.

## Docker Registry

A **registry** is a place where Docker images are stored.

Examples:

```text id="czdvdg"
Docker Hub
GitHub Container Registry
Oracle Container Registry
Amazon ECR
Azure Container Registry
Google Artifact Registry
```

Basic flow:

```text id="750pid"
docker build
    ↓
docker tag
    ↓
docker push
    ↓
docker pull
    ↓
docker run
```

## Build and Run Full Example

Create image:

```bash id="p23fkc"
docker build -t my-flask-app:1.0.0 .
```

Run container:

```bash id="tvpzzd"
docker run -d --name flask-app -p 5000:5000 my-flask-app:1.0.0
```

Check:

```bash id="dfqmp8"
docker ps
```

Open:

```text id="okhs3m"
http://localhost:5000
```

## Update Image Version

After changing your app, build a new version:

```bash id="kfczo8"
docker build -t my-flask-app:1.1.0 .
```

Stop old container:

```bash id="w3sbnh"
docker stop flask-app
docker rm flask-app
```

Run new version:

```bash id="l817ur"
docker run -d --name flask-app -p 5000:5000 my-flask-app:1.1.0
```

## Rollback Example

If version `1.1.0` has a problem, run the old version again.

```bash id="as2xfb"
docker stop flask-app
docker rm flask-app
docker run -d --name flask-app -p 5000:5000 my-flask-app:1.0.0
```

This is why clear tags are important.

## Common Beginner Mistakes

### Using latest Only

Bad:

```bash id="ls44ci"
docker run nginx
```

Better:

```bash id="ov931f"
docker run nginx:1.27-alpine
```

### Forgetting to Tag the Image

Bad:

```bash id="qdqebu"
docker build .
```

Better:

```bash id="flzb6v"
docker build -t my-app:1.0.0 .
```

### Confusing Image and Container

Image:

```text id="vze7xy"
nginx:alpine
```

Container:

```text id="eq3eqo"
web
```

Run:

```bash id="h5j29s"
docker run -d --name web nginx:alpine
```

### Removing Image While Container Uses It

If a container is using an image, Docker may not remove the image.

Check containers:

```bash id="v8bk4k"
docker ps -a
```

Remove container first:

```bash id="gi5ro2"
docker rm -f web
```

Then remove image:

```bash id="np0kii"
docker rmi nginx:alpine
```

### Bad Tag Names

Bad:

```text id="wykj8q"
my-app:final
my-app:done
my-app:new
```

Better:

```text id="n9ucuj"
my-app:1.0.0
my-app:1.1.0
my-app:2.0.0
```

## Useful Commands

Pull image:

```bash id="zp9pwn"
docker pull IMAGE:TAG
```

List images:

```bash id="06xrih"
docker images
```

Build image:

```bash id="650um0"
docker build -t IMAGE:TAG .
```

Tag image:

```bash id="se6xhe"
docker tag OLD_IMAGE:TAG NEW_IMAGE:TAG
```

Push image:

```bash id="m0vm1g"
docker push IMAGE:TAG
```

Run image:

```bash id="bcpmnc"
docker run IMAGE:TAG
```

Inspect image:

```bash id="n8hag6"
docker image inspect IMAGE:TAG
```

Show image layers:

```bash id="qv6j3h"
docker history IMAGE:TAG
```

Remove image:

```bash id="guix2q"
docker rmi IMAGE:TAG
```

Clean unused images:

```bash id="ptkwnl"
docker image prune
```

## Summary

```text id="5h7ca0"
Docker image → Template used to create containers
Docker tag   → Version or label of an image
latest       → Default tag, but not always safe for production
Registry     → Place where images are stored
docker pull  → Download image
docker build → Build custom image
docker tag   → Add another name/tag to image
docker push  → Upload image to registry
docker rmi   → Remove image
```

> Docker images are templates for containers, and tags help you control which version of the image you are using.

