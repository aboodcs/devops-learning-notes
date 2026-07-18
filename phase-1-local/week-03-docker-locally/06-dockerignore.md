# 06 - Dockerignore

A **.dockerignore** file tells Docker which files and folders should not be copied into the Docker image during build.

It works like `.gitignore`, but for Docker builds.

```text id="q1av65"
.gitignore     → Ignore files from Git
.dockerignore  → Ignore files from Docker build context
```

## Why Do We Need .dockerignore?

When you run:

```bash id="xz4k71"
docker build -t my-app:1.0.0 .
```

Docker sends the current folder to the Docker engine as the **build context**.

If your project has many unnecessary files, Docker may send all of them.

This can make the build:

```text id="s2ub33"
Slower
Larger
Less secure
Harder to cache
```

A `.dockerignore` file prevents unnecessary files from entering the Docker build context.

## Simple Explanation

Without `.dockerignore`:

```text id="jp5kr4"
Project folder
├── app.py
├── requirements.txt
├── Dockerfile
├── .env
├── .git/
├── screenshots/
├── venv/
└── __pycache__/

Docker may send everything to the build context.
```

With `.dockerignore`:

```text id="nj9s4d"
Docker ignores:
.env
.git/
venv/
__pycache__/
screenshots/
```

Only important files are used for building the image.

## Build Context

The **build context** is the folder Docker uses during image build.

Example:

```bash id="f17tk8"
docker build -t my-app:1.0.0 .
```

The dot `.` means:

```text id="tg3bq1"
Use the current folder as the build context.
```

Docker can only copy files from the build context.

Example:

```dockerfile id="ytxq6h"
COPY . .
```

This copies files from the build context into the image.

So if the build context has unnecessary files, they may be copied too.

## Example Project

```text id="pnr2ke"
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── venv/
├── __pycache__/
├── .git/
└── README.md
```

We want Docker to use:

```text id="tlwolb"
app.py
requirements.txt
Dockerfile
```

We do not want Docker to include:

```text id="su4w74"
.env
venv/
__pycache__/
.git/
```

## Basic .dockerignore Example

Create a file named:

```text id="mf8blo"
.dockerignore
```

Add:

```text id="teec2h"
.git
.gitignore
.env
venv/
__pycache__/
*.pyc
*.log
README.md
```

## What This Means

```text id="z177qj"
.git         → Do not copy Git history
.gitignore   → Not needed inside image
.env         → Do not copy secrets
venv/        → Do not copy local Python environment
__pycache__/ → Do not copy Python cache files
*.pyc        → Do not copy compiled Python files
*.log        → Do not copy log files
README.md    → Usually not needed inside runtime image
```

## Why Ignoring .env Is Important

`.env` files often contain secrets.

Example:

```text id="rganfo"
DATABASE_PASSWORD=secret123
API_KEY=abcd1234
TOKEN=private-token
```

Do not copy secrets into Docker images.

Bad:

```dockerfile id="xqp2dh"
COPY . .
```

without `.dockerignore`.

This may copy `.env` into the image.

Better:

```text id="j233d3"
Add .env to .dockerignore
```

## Common Files to Ignore

```text id="z24exy"
.git
.gitignore
.dockerignore
.env
.env.*
*.log
__pycache__/
*.pyc
venv/
node_modules/
dist/
build/
coverage/
.pytest_cache/
.cache/
.idea/
.vscode/
.DS_Store
README.md
screenshots/
```

## Python Project Example

For a Python or Flask app:

```text id="divml3"
.git
.gitignore
.env
.env.*
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
htmlcov/
*.log
README.md
```

Example project:

```text id="i1tc61"
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

Good `.dockerignore`:

```text id="pi35pj"
.git
.env
venv/
__pycache__/
*.pyc
.pytest_cache/
*.log
README.md
```

## Node.js Project Example

For a Node.js app:

```text id="kaezgj"
.git
.env
node_modules/
npm-debug.log
coverage/
dist/
build/
.cache/
README.md
```

Why ignore `node_modules/`?

Because dependencies should be installed inside the image using:

```dockerfile id="r5c8fh"
RUN npm install
```

or:

```dockerfile id="vaxfp6"
RUN npm ci
```

## Dockerfile Example with .dockerignore

Project:

```text id="uvzscg"
my-flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

Dockerfile:

```dockerfile id="pprkrm"
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

`.dockerignore`:

```text id="m4dgdw"
.git
.env
venv/
__pycache__/
*.pyc
*.log
README.md
```

Build:

```bash id="ocvh9t"
docker build -t my-flask-app:1.0.0 .
```

Run:

```bash id="xfrq1h"
docker run -d --name flask-app -p 5000:5000 my-flask-app:1.0.0
```

## .dockerignore vs .gitignore

| .gitignore                          | .dockerignore                              |
| ----------------------------------- | ------------------------------------------ |
| Used by Git                         | Used by Docker                             |
| Prevents files from being committed | Prevents files from entering build context |
| Protects repository                 | Protects Docker image build                |
| Example: ignore `.env` from Git     | Example: ignore `.env` from Docker image   |

You usually need both files.

Example:

```text id="cjfwlj"
.gitignore
.dockerignore
```

## Important Rule

`.dockerignore` affects the build context.

It does not delete files from your computer.

It only tells Docker:

```text id="wg789m"
Do not send these files to the build.
```

## Example Without .dockerignore

Bad situation:

```text id="u5danr"
docker build -t app .
```

Docker sends:

```text id="ygrjxu"
.git/
venv/
node_modules/
screenshots/
.env
logs/
```

Problems:

```text id="lmtve9"
Build is slower
Image may contain secrets
Build context is too large
Docker cache may break more often
```

## Example With .dockerignore

Good situation:

```text id="fq62or"
docker build -t app .
```

Docker ignores:

```text id="yc64t4"
.git/
venv/
node_modules/
.env
logs/
```

Benefits:

```text id="b8qcy0"
Faster build
Smaller build context
Better security
Cleaner Docker image
Better caching
```

## Check Build Context Size

When you build an image, Docker may show context size.

Example:

```text id="rhp7gw"
Sending build context to Docker daemon  300MB
```

After adding `.dockerignore`, it may become:

```text id="ghg1p4"
Sending build context to Docker daemon  20kB
```

This means Docker is sending fewer unnecessary files.

## Pattern Examples

Ignore one file:

```text id="vfy5bf"
.env
```

Ignore a folder:

```text id="ded5md"
venv/
```

Ignore all log files:

```text id="g8ch4w"
*.log
```

Ignore all `.pyc` files:

```text id="w3ge5t"
*.pyc
```

Ignore files inside any cache folder:

```text id="ui1n6m"
**/__pycache__/
```

Ignore all environment files:

```text id="llv84q"
.env.*
```

## Negation Pattern

You can ignore many files, but allow one file back using `!`.

Example:

```text id="ffkf53"
*.md
!README.md
```

Meaning:

```text id="m4mdem"
Ignore all Markdown files
But do not ignore README.md
```

Another example:

```text id="cn7kg5"
.env.*
!.env.example
```

Meaning:

```text id="a3s0mv"
Ignore real environment files
Keep .env.example
```

This is useful because `.env.example` does not contain real secrets.

## Best Practice for .env.example

You should not include real secrets.

Bad `.env`:

```text id="gl4r00"
DATABASE_PASSWORD=my-real-password
```

Good `.env.example`:

```text id="sanidp"
DATABASE_PASSWORD=change-me
```

Then in `.dockerignore`:

```text id="vqowyi"
.env
.env.*
!.env.example
```

## Common Beginner Mistakes

### Forgetting .dockerignore

Bad:

```text id="fqg89z"
No .dockerignore file
```

Docker may send everything to the build context.

### Copying Secrets

Bad:

```text id="tmo1za"
.env copied into image
```

Better:

```text id="gy59kh"
.env in .dockerignore
```

### Copying Local Virtual Environment

Bad:

```text id="iztx8d"
venv/ copied into image
```

Better:

```text id="wfyeig"
venv/ in .dockerignore
```

Docker should install dependencies inside the image.

### Copying Git History

Bad:

```text id="at7est"
.git/ copied into image
```

Better:

```text id="nk32by"
.git in .dockerignore
```

### Ignoring Files Needed by Dockerfile

Bad:

```text id="insylh"
requirements.txt
```

inside `.dockerignore` while Dockerfile has:

```dockerfile id="z96xy5"
COPY requirements.txt .
```

This will break the build.

Docker cannot copy a file that was ignored.

## How to Test .dockerignore

Build the image:

```bash id="dy75ej"
docker build -t test-app .
```

Run the container:

```bash id="p4hkng"
docker run -it --rm test-app sh
```

Check files inside the container:

```bash id="iev7x4"
ls -la
```

Make sure ignored files are not inside the image.

## Practical Lab

Create a test folder:

```bash id="u1hi41"
mkdir dockerignore-lab
cd dockerignore-lab
```

Create files:

```bash id="bzwso3"
touch app.py requirements.txt Dockerfile .env README.md app.log
mkdir venv __pycache__ screenshots
```

Create `.dockerignore`:

```bash id="w1nk2x"
nano .dockerignore
```

Add:

```text id="x5o26n"
.env
venv/
__pycache__/
*.log
screenshots/
README.md
```

Create simple Dockerfile:

```dockerfile id="z3zsvv"
FROM python:3.12-slim

WORKDIR /app

COPY . .

CMD ["ls", "-la"]
```

Build:

```bash id="e2aum2"
docker build -t dockerignore-lab .
```

Run:

```bash id="lytt31"
docker run --rm dockerignore-lab
```

You should not see:

```text id="ufgh6p"
.env
venv/
__pycache__/
app.log
screenshots/
README.md
```

## Recommended .dockerignore for DevOps Notes Repo

For a notes or learning repo, you can use:

```text id="uzpi8f"
.git
.gitignore
.env
.env.*
*.pem
*.key
*.log
__pycache__/
*.pyc
venv/
node_modules/
.terraform/
*.tfstate
*.tfstate.backup
.DS_Store
.cache/
screenshots/
```

This is useful if the repo contains Docker, Terraform, and DevOps labs.

## Useful Commands

Build image:

```bash id="brgcyc"
docker build -t my-app:1.0.0 .
```

Check images:

```bash id="tagvba"
docker images
```

Run container:

```bash id="jmez5h"
docker run --rm my-app:1.0.0
```

Enter container:

```bash id="zgnyp3"
docker run -it --rm my-app:1.0.0 sh
```

Check files inside container:

```bash id="rxwpjh"
ls -la
```

## Summary

```text id="x9yk28"
.dockerignore → Excludes files from Docker build context
Build context → Files sent to Docker during build
.env          → Should usually be ignored
.git          → Should be ignored
venv/         → Should be ignored
node_modules/ → Should be ignored
*.log         → Should be ignored
```

> A `.dockerignore` file makes Docker builds faster, cleaner, and safer by keeping unnecessary files and secrets out of the build context.

