# GitHub Basics

**GitHub** is a platform used to store Git repositories online.

Git runs on your computer.
GitHub stores your project on the internet.

```text id="3rcfdz"
Git     → Local version control tool
GitHub  → Online platform for Git repositories
```

## Why Do We Use GitHub?

GitHub helps developers:

```text id="w2o7jy"
Store code online
Share projects
Work with teams
Review code
Create Pull Requests
Track issues
Run CI/CD pipelines
```

## Git vs GitHub

| Git                             | GitHub                                  |
| ------------------------------- | --------------------------------------- |
| Tool installed on your computer | Website/platform online                 |
| Tracks file changes             | Hosts Git repositories                  |
| Works locally                   | Works remotely                          |
| Uses commands like `git commit` | Provides Pull Requests, Issues, Actions |

## Repository

A **repository** is a project folder tracked by Git.

A repository can contain:

```text id="gos88a"
Code files
Markdown notes
Images
Dockerfiles
Kubernetes YAML
README file
```

Example repository:

```text id="ndy00m"
devops-learning-notes
```

## Local Repository vs Remote Repository

### Local Repository

This is the repository on your laptop.

Example:

```text id="heayj6"
/home/abood/devops-learning-notes
```

### Remote Repository

This is the repository on GitHub.

Example:

```text id="8pp9pv"
https://github.com/aboodcs/devops-learning-notes
```

## Basic GitHub Flow

```text id="fg57o0"
Local project
   │
   ▼
git add
   │
   ▼
git commit
   │
   ▼
git push
   │
   ▼
GitHub repository
```

## Create a Repository on GitHub

On GitHub:

```text id="vwzs4l"
1. Click New repository
2. Choose repository name
3. Choose Public or Private
4. Click Create repository
```

Example repository name:

```text id="bpywte"
devops-learning-notes
```

## Clone a Repository

Cloning means downloading a GitHub repository to your computer.

```bash id="xxwu0y"
git clone https://github.com/username/repository-name.git
```

Example:

```bash id="jt4a2k"
git clone https://github.com/aboodcs/devops-learning-notes.git
```

Enter the project:

```bash id="akl6p4"
cd devops-learning-notes
```

## Check Repository Status

```bash id="e4f41j"
git status
```

This shows:

```text id="arlh6y"
Changed files
New files
Deleted files
Current branch
```

## Add Files

Add one file:

```bash id="g0nff7"
git add README.md
```

Add all changed files:

```bash id="y43pux"
git add .
```

## Commit Changes

A commit saves your changes locally.

```bash id="dqwys7"
git commit -m "docs: add GitHub basics notes"
```

A good commit message should explain what changed.

Good examples:

```text id="4u8e23"
docs: add Docker notes
fix: correct Kubernetes service
feat: add Flask health endpoint
```

## Push Changes to GitHub

Push sends your local commits to GitHub.

```bash id="q3bpkr"
git push
```

If this is a new branch:

```bash id="rclnsa"
git push -u origin branch-name
```

Example:

```bash id="ja6pl8"
git push -u origin docs/github-basics
```

## Pull Changes from GitHub

Pull downloads the latest changes from GitHub.

```bash id="nxjja9"
git pull
```

Use this before starting new work:

```bash id="3gr5zj"
git switch main
git pull
```

## Branches

A branch is a separate line of work.

```text id="jqodjl"
main branch     → stable code
feature branch  → new work
docs branch     → documentation update
```

Create and switch to a new branch:

```bash id="o6sus8"
git switch -c docs/github-basics
```

Check branches:

```bash id="fuayav"
git branch
```

## Pull Request

A **Pull Request** is a request to merge your branch into another branch.

Example:

```text id="s8oxz2"
docs/github-basics → main
```

A Pull Request allows others to:

```text id="73v6ve"
Review changes
Leave comments
Approve work
Run tests
Merge safely
```

## README.md

`README.md` is the main description file of a GitHub repository.

It usually contains:

```text id="6spgs9"
Project name
Project description
Installation steps
Usage commands
Screenshots
Technologies used
```

Example:

```md id="a2efrs"
# DevOps Learning Notes

This repository contains my DevOps learning notes and labs.
```

## Issues

GitHub Issues are used to track tasks, bugs, or ideas.

Examples:

```text id="qrkfb5"
Add Docker Compose lab
Fix Kubernetes README
Update Helm examples
```

Issues help organize work.

## GitHub Actions

**GitHub Actions** is used for CI/CD.

It can automatically run tasks when you push code.

Examples:

```text id="v1cryv"
Run tests
Build Docker image
Check code quality
Deploy application
Run Helm lint
```

Example workflow location:

```text id="xg61y3"
.github/workflows/ci.yml
```

## .gitignore

`.gitignore` tells Git which files not to track.

Example:

```text id="cqntvd"
.env
__pycache__/
node_modules/
venv/
*.log
```

Do not upload secrets or environment files to GitHub.

Bad:

```text id="ehl39y"
.env file with passwords
```

Better:

```text id="gp498h"
Add .env to .gitignore
```

## Common GitHub Workflow

```bash id="9ol35t"
git switch main
git pull

git switch -c docs/github-basics

# edit files

git status
git add github-basics.md
git commit -m "docs: add GitHub basics notes"

git push -u origin docs/github-basics
```

Then open a Pull Request on GitHub:

```text id="9q1k9p"
docs/github-basics → main
```

## Useful Commands

Clone repository:

```bash id="rf70gh"
git clone REPOSITORY_URL
```

Check status:

```bash id="qzn6n6"
git status
```

Add files:

```bash id="5gzh2r"
git add .
```

Commit:

```bash id="f403w0"
git commit -m "message"
```

Push:

```bash id="7zj7fb"
git push
```

Pull:

```bash id="pnw4gg"
git pull
```

Create branch:

```bash id="q0bs2z"
git switch -c branch-name
```

View remote:

```bash id="kjhjww"
git remote -v
```

## Common Mistakes

### Working Directly on main

Bad:

```bash id="p2atzp"
git switch main
# edit files
git push
```

Better:

```bash id="hpn6lv"
git switch -c docs/update-notes
```

### Bad Commit Message

Bad:

```text id="nd0lsm"
update
```

Better:

```text id="4laaxj"
docs: update GitHub basics notes
```

### Forgetting to Pull

Before starting work:

```bash id="gx8op8"
git switch main
git pull
```

### Uploading Secrets

Do not upload:

```text id="c4q3gg"
.env
passwords
API keys
private keys
```

Add them to `.gitignore`.

## Summary

```text id="27etex"
GitHub      → Online platform for Git repositories
Repository  → Project stored on GitHub
Clone       → Download repository
Commit      → Save changes locally
Push        → Upload commits to GitHub
Pull        → Download latest changes
Branch      → Separate line of work
Pull Request → Request to merge changes
README.md   → Main project documentation file
```

> GitHub helps you store projects online, work with branches, open Pull Requests, and collaborate safely.

