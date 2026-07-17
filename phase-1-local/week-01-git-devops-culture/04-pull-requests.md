# Pull Requests

A **Pull Request** is a request to merge changes from one branch into another branch.

Usually, you create a Pull Request from a feature branch into the main branch.

```text id="py1p0d"
feature branch → Pull Request → main branch
```

## Why Do We Need Pull Requests?

Pull Requests help teams review code before it becomes part of the main project.

Without Pull Requests, someone may push broken code directly to `main`.

With Pull Requests, the team can:

```text id="m29gvb"
Review the changes
Discuss the code
Run tests
Fix problems
Approve the work
Merge safely
```

## Basic Pull Request Flow

```text id="3vs2li"
1. Create a new branch
2. Make changes
3. Commit the changes
4. Push the branch to GitHub
5. Open a Pull Request
6. Review and fix issues
7. Merge the Pull Request
```

## Example Scenario

You want to add Docker notes to your repository.

Do not work directly on `main`.

Create a new branch:

```bash id="ob6eiw"
git switch main
git pull
git switch -c docs/docker-notes
```

Now edit your files.

Check the changes:

```bash id="txrrh2"
git status
```

Add the files:

```bash id="bquyel"
git add .
```

Commit:

```bash id="ezgr84"
git commit -m "add docker notes"
```

Push the branch:

```bash id="ei7b9r"
git push -u origin docs/docker-notes
```

Now go to GitHub and open a Pull Request.

```text id="sz2u0e"
docs/docker-notes → main
```

## Pull Request Meaning

A Pull Request says:

```text id="l6jl3f"
I made changes in this branch.
Please review them.
If everything is good, merge them into the main branch.
```

## Pull Request Example

```text id="m8afh2"
Source branch: docs/docker-notes
Target branch: main
```

Meaning:

```text id="3zemvk"
Take my changes from docs/docker-notes
and merge them into main
```

## Good Pull Request Title

Bad title:

```text id="yxtqen"
update
```

Better title:

```text id="ylt6op"
Add Docker networking notes
```

Good Pull Request titles are clear and short.

Examples:

```text id="3a58dp"
Add Docker Compose lab
Fix Kubernetes service YAML
Update Helm README
Add Git branching notes
```

## Good Pull Request Description

A good Pull Request description explains what changed.

Example:

````md id="g59c7m"
## What changed?

- Added Docker networking notes
- Added custom bridge network example
- Added container-to-container communication commands

## How to test?

Run:

```bash
docker network create app-network
docker ps
````

````

## Check Pull Request Changes Locally

Before opening the Pull Request, check what changed:

```bash id="xkv6az"
git status
````

View changed files:

```bash id="n2d6zo"
git diff --name-only
```

View full changes:

```bash id="6qypf5"
git diff
```

View commits:

```bash id="j5cgv7"
git log --oneline
```

## Pull Request Review

After opening the Pull Request, another person can review it.

They may:

```text id="h2r8rx"
Approve it
Request changes
Leave comments
Ask questions
Run tests
```

If they request changes, edit the same branch again:

```bash id="fslomo"
# edit files

git add .
git commit -m "fix review comments"
git push
```

The Pull Request updates automatically.

## Merge the Pull Request

After approval, merge the Pull Request into `main`.

On GitHub, click:

```text id="rde1rn"
Merge pull request
```

Then update your local `main` branch:

```bash id="w0slxq"
git switch main
git pull
```

## Delete the Branch After Merge

After the Pull Request is merged, delete the local branch:

```bash id="5gjmki"
git branch -d docs/docker-notes
```

Delete the remote branch:

```bash id="mqxvay"
git push origin --delete docs/docker-notes
```

## Pull Request with GitHub CLI

You can also create a Pull Request from the terminal using `gh`.

Check if GitHub CLI is installed:

```bash id="bxv50p"
gh --version
```

Login:

```bash id="5bsxsl"
gh auth login
```

Create a Pull Request:

```bash id="dqje95"
gh pr create \
  --base main \
  --head docs/docker-notes \
  --title "Add Docker networking notes" \
  --body "Added Docker network notes and practical examples."
```

View Pull Requests:

```bash id="31pw2r"
gh pr list
```

View one Pull Request:

```bash id="muogzc"
gh pr view
```

Check Pull Request diff:

```bash id="3ah9c2"
gh pr diff
```

Merge a Pull Request:

```bash id="jka0w2"
gh pr merge
```

## Pull Request vs Commit

| Commit                          | Pull Request                   |
| ------------------------------- | ------------------------------ |
| Saves changes locally           | Requests to merge changes      |
| Happens inside a branch         | Happens between branches       |
| Created with `git commit`       | Created on GitHub or with `gh` |
| One PR can contain many commits | PR groups the work for review  |

## Pull Request vs Merge

| Pull Request                 | Merge                         |
| ---------------------------- | ----------------------------- |
| Review request               | Actual combining of branches  |
| Happens before merge         | Happens after approval        |
| Shows changes and discussion | Adds changes to target branch |

## Common Pull Request Mistakes

### Working Directly on main

Bad:

```bash id="iqamg5"
git switch main
# edit files directly
git push
```

Better:

```bash id="4dztds"
git switch -c feature/my-change
```

### Bad Branch Name

Bad:

```text id="2u1gol"
test
```

Better:

```text id="tobee3"
docs/add-docker-network-notes
```

### Bad Commit Message

Bad:

```text id="llm7bh"
fix
```

Better:

```text id="yvwoji"
fix docker network example
```

### Pull Request Is Too Big

A very large Pull Request is hard to review.

Better:

```text id="34yjcr"
One Pull Request = one clear task
```

## Full Pull Request Workflow

```bash id="zm5gm7"
git switch main
git pull

git switch -c docs/add-pull-request-notes

# edit files

git status
git add .
git commit -m "add pull request notes"

git push -u origin docs/add-pull-request-notes
```

Then open a Pull Request on GitHub:

```text id="8w133d"
docs/add-pull-request-notes → main
```

After merge:

```bash id="drsl95"
git switch main
git pull
git branch -d docs/add-pull-request-notes
```

## Useful Commands

Check current branch:

```bash id="l6yayk"
git branch
```

Create and switch branch:

```bash id="tpofnf"
git switch -c branch-name
```

Check changed files:

```bash id="b3gb4x"
git status
```

Stage files:

```bash id="8ls8v0"
git add .
```

Commit:

```bash id="yfbpd5"
git commit -m "message"
```

Push branch:

```bash id="cdhpqx"
git push -u origin branch-name
```

Update main:

```bash id="a0mpk3"
git switch main
git pull
```

Delete local branch:

```bash id="dazrbg"
git branch -d branch-name
```

Delete remote branch:

```bash id="y7oqp4"
git push origin --delete branch-name
```

## Summary

```text id="pjgml1"
Pull Request → Request to merge changes
Source branch → Branch that contains your changes
Target branch → Branch that receives the changes
Review → Someone checks your changes
Merge → Add the changes to the target branch
```

> A Pull Request lets you review and safely merge changes instead of pushing directly to the main branch.

