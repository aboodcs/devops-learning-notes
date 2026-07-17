# GitHub Actions Intro

**GitHub Actions** is a CI/CD tool built into GitHub.

It helps you automate tasks when something happens in your repository.

Examples:

```text id="m81jcu"
Run tests
Build Docker image
Check code quality
Run security checks
Deploy application
Lint Kubernetes YAML
Lint Helm chart
```

## What Is CI/CD?

### CI - Continuous Integration

CI means automatically checking your code when you push changes.

Example:

```text id="obpg88"
Developer pushes code
        ↓
GitHub Actions runs tests
        ↓
If tests pass, code is safer to merge
```

### CD - Continuous Delivery / Deployment

CD means automatically preparing or deploying the application.

Example:

```text id="nzocvx"
Push code
   ↓
Build Docker image
   ↓
Push image to registry
   ↓
Deploy to server or Kubernetes
```

## Why Do We Use GitHub Actions?

Without GitHub Actions, you must run checks manually.

With GitHub Actions, GitHub can run them automatically.

```text id="dojfbv"
Manual work:
Run tests yourself
Build image yourself
Check files yourself

Automated work:
GitHub Actions does it after push or pull request
```

## Main GitHub Actions Concepts

```text id="9c24ko"
Workflow → Automation file
Event    → What starts the workflow
Job      → Group of steps
Step     → One command or action
Action   → Reusable task
Runner   → Machine that runs the workflow
```

## 1. Workflow

A **workflow** is an automation file.

Workflow files are stored inside:

```text id="y555p4"
.github/workflows/
```

Example:

```text id="ei7r77"
.github/workflows/ci.yml
```

A repository can have many workflows:

```text id="q19alu"
ci.yml
docker-build.yml
deploy.yml
helm-lint.yml
```

## 2. Event

An **event** is what starts the workflow.

Examples:

```text id="igjysb"
push
pull_request
workflow_dispatch
schedule
```

Example:

```yaml id="m0it69"
on:
  push:
    branches:
      - main
```

This means:

```text id="5fkvr3"
Run the workflow when code is pushed to main.
```

Another example:

```yaml id="txq4rp"
on:
  pull_request:
    branches:
      - main
```

This means:

```text id="dwqham"
Run the workflow when someone opens a Pull Request to main.
```

## 3. Job

A **job** is a group of steps that run together.

Example:

```yaml id="dshgqc"
jobs:
  test:
    runs-on: ubuntu-latest
```

Here:

```text id="kbepbk"
test → Job name
ubuntu-latest → Runner machine
```

## 4. Runner

A **runner** is the machine that runs the workflow.

Common runner:

```yaml id="fdm2q9"
runs-on: ubuntu-latest
```

This means GitHub will create a temporary Ubuntu machine to run the job.

Other examples:

```text id="i8rrzh"
ubuntu-latest
windows-latest
macos-latest
```

## 5. Step

A **step** is one task inside a job.

A step can run a command:

```yaml id="hro4m7"
- name: Print message
  run: echo "Hello from GitHub Actions"
```

A job can have many steps:

```text id="h7a2m0"
Step 1 → Checkout code
Step 2 → Install dependencies
Step 3 → Run tests
Step 4 → Build application
```

## 6. Action

An **action** is a reusable task made by GitHub or the community.

Example:

```yaml id="ytv63k"
- name: Checkout code
  uses: actions/checkout@v4
```

This downloads your repository code into the runner.

Without checkout, the runner will not have your project files.

## Basic Workflow Example

Create this file:

```text id="h9abxv"
.github/workflows/ci.yml
```

Add:

```yaml id="u8850b"
name: CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Print message
        run: echo "GitHub Actions is working"
```

## Explanation

```yaml id="0510tu"
name: CI
```

This is the workflow name.

```yaml id="0zrrx6"
on:
  push:
  pull_request:
```

This means the workflow runs on push and Pull Request.

```yaml id="w86cq5"
jobs:
  test:
```

This creates a job named `test`.

```yaml id="wqxrnw"
runs-on: ubuntu-latest
```

This tells GitHub to run the job on an Ubuntu machine.

```yaml id="38xhb4"
uses: actions/checkout@v4
```

This downloads the repository code into the runner.

```yaml id="x893jx"
run: echo "GitHub Actions is working"
```

This runs a terminal command.

## Python CI Example

If your project is Python, your workflow can install dependencies and run tests.

```yaml id="gr0vjj"
name: Python CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest
```

This workflow:

```text id="xq1ip3"
Downloads the code
Installs Python
Installs dependencies
Runs tests
```

## Docker Build Example

If your project has a Dockerfile, you can test if the image builds.

```yaml id="l52rcn"
name: Docker Build

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  docker-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t my-app .
```

This checks that your Dockerfile works.

## Helm Lint Example

If your project has a Helm chart:

```yaml id="u0h9w9"
name: Helm Lint

on:
  pull_request:
    branches:
      - main

jobs:
  helm-lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Helm
        uses: azure/setup-helm@v4

      - name: Lint Helm chart
        run: helm lint ./nginx-chart
```

This checks the Helm chart before merging.

## Manual Workflow

Sometimes you want to run the workflow manually.

Use:

```yaml id="p8xkuq"
on:
  workflow_dispatch:
```

Example:

```yaml id="kh49hm"
name: Manual Workflow

on:
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest

    steps:
      - name: Say hello
        run: echo "This workflow was started manually"
```

After pushing this file, you can run it from the GitHub Actions tab.

## Full Beginner CI Workflow

```yaml id="dhnpxw"
name: Beginner CI

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

  workflow_dispatch:

jobs:
  checks:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Show current folder
        run: pwd

      - name: List files
        run: ls -la

      - name: Print success message
        run: echo "CI checks completed successfully"
```

## Where to See Workflow Results

On GitHub:

```text id="uk4z40"
Repository → Actions tab → Select workflow run
```

You can see:

```text id="ar2t85"
Workflow status
Job logs
Failed commands
Passed checks
Execution time
```

## Workflow Status

Common statuses:

```text id="0580l6"
green check  → workflow passed
red x        → workflow failed
yellow dot   → workflow running
gray icon    → workflow skipped
```

## Common Mistakes

### Wrong Folder

Workflow files must be inside:

```text id="lsmkmy"
.github/workflows/
```

Bad:

```text id="g9udlj"
.github/ci.yml
```

Good:

```text id="rkxol0"
.github/workflows/ci.yml
```

### Wrong YAML Indentation

Bad indentation can break the workflow.

YAML depends on spaces.

Bad:

```yaml id="9el8cm"
jobs:
test:
runs-on: ubuntu-latest
```

Good:

```yaml id="hhyb94"
jobs:
  test:
    runs-on: ubuntu-latest
```

### Forgetting Checkout

If your workflow needs project files, use:

```yaml id="ym2z2v"
- uses: actions/checkout@v4
```

### Wrong File Name

Use `.yml` or `.yaml`.

Example:

```text id="e4cdvn"
ci.yml
ci.yaml
```

## Useful Git Commands

Create workflow folder:

```bash id="a83fs2"
mkdir -p .github/workflows
```

Create workflow file:

```bash id="rtgpye"
nano .github/workflows/ci.yml
```

Add and commit:

```bash id="hbgf8v"
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
```

Push:

```bash id="gd3u96"
git push
```

## Summary

```text id="ya12xv"
GitHub Actions → Automation tool inside GitHub
Workflow       → YAML automation file
Event          → Trigger that starts the workflow
Job            → Group of steps
Step           → One command or reusable action
Action         → Reusable workflow task
Runner         → Machine that runs the workflow
CI             → Automatically test code
CD             → Automatically deliver or deploy code
```

> GitHub Actions helps you test, build, and deploy projects automatically from GitHub.

