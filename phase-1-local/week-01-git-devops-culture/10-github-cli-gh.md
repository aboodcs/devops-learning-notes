# GitHub CLI - gh

**GitHub CLI** is a command-line tool that lets you use GitHub from the terminal.

The command name is:

```bash
gh
```

With `gh`, you can:

```text
Login to GitHub
Create repositories
Clone repositories
Create Pull Requests
View Pull Requests
Create issues
Check GitHub Actions
Open GitHub pages from terminal
```

## Why Do We Use GitHub CLI?

Normally, you use GitHub from the browser.

With GitHub CLI, you can do many GitHub tasks directly from the terminal.

Example:

```bash
gh pr create
```

This creates a Pull Request without opening GitHub manually.

## Check if gh Is Installed

```bash
gh --version
```

If it shows a version, it is installed.

Example:

```text
gh version 2.x.x
```

## Login to GitHub

Before using GitHub CLI, login:

```bash
gh auth login
```

Follow the steps:

```text
GitHub.com
HTTPS
Login with browser
Authorize GitHub CLI
```

Check login status:

```bash
gh auth status
```

## Clone a Repository

```bash
gh repo clone username/repository-name
```

Example:

```bash
gh repo clone aboodcs/devops-learning-notes
```

This downloads the repository to your machine.

## Create a New Repository

Create a repository from the terminal:

```bash
gh repo create my-repo
```

Create a public repository:

```bash
gh repo create my-repo --public
```

Create a private repository:

```bash
gh repo create my-repo --private
```

Create repository and push current folder:

```bash
gh repo create my-repo --public --source=. --remote=origin --push
```

## View Repository in Browser

Open the current repository on GitHub:

```bash
gh repo view --web
```

## Pull Requests

A Pull Request is a request to merge one branch into another.

Example:

```text
feature branch → Pull Request → main
```

## Create a Pull Request

First create a branch:

```bash
git switch -c docs/github-cli-notes
```

Edit files, then commit:

```bash
git add .
git commit -m "docs: add GitHub CLI notes"
```

Push the branch:

```bash
git push -u origin docs/github-cli-notes
```

Create the Pull Request:

```bash
gh pr create \
  --base main \
  --head docs/github-cli-notes \
  --title "Add GitHub CLI notes" \
  --body "Added notes explaining basic GitHub CLI usage."
```

Meaning:

```text
--base   → target branch
--head   → source branch
--title  → Pull Request title
--body   → Pull Request description
```

## View Pull Requests

List Pull Requests:

```bash
gh pr list
```

View current Pull Request:

```bash
gh pr view
```

View Pull Request in browser:

```bash
gh pr view --web
```

View Pull Request diff:

```bash
gh pr diff
```

View changed files only:

```bash
gh pr diff --name-only
```

## Checkout a Pull Request

If you want to test a Pull Request locally:

```bash
gh pr checkout PR_NUMBER
```

Example:

```bash
gh pr checkout 3
```

This switches your local repo to the Pull Request branch.

## Merge a Pull Request

Merge using GitHub CLI:

```bash
gh pr merge
```

Merge with squash:

```bash
gh pr merge --squash
```

Merge and delete branch:

```bash
gh pr merge --squash --delete-branch
```

## Issues

GitHub Issues are used to track tasks, bugs, or ideas.

List issues:

```bash
gh issue list
```

Create an issue:

```bash
gh issue create \
  --title "Add Docker notes" \
  --body "Create beginner notes for Docker images, containers, and volumes."
```

View issue:

```bash
gh issue view ISSUE_NUMBER
```

Example:

```bash
gh issue view 5
```

Close issue:

```bash
gh issue close ISSUE_NUMBER
```

## GitHub Actions

GitHub Actions are used for CI/CD pipelines.

View workflow runs:

```bash
gh run list
```

View one run:

```bash
gh run view RUN_ID
```

Watch a workflow run:

```bash
gh run watch
```

View logs:

```bash
gh run view --log
```

Re-run a failed workflow:

```bash
gh run rerun RUN_ID
```

## Useful gh Commands

Check login:

```bash
gh auth status
```

Login:

```bash
gh auth login
```

Clone repo:

```bash
gh repo clone owner/repo
```

View repo:

```bash
gh repo view
```

Open repo in browser:

```bash
gh repo view --web
```

Create Pull Request:

```bash
gh pr create
```

List Pull Requests:

```bash
gh pr list
```

View Pull Request:

```bash
gh pr view
```

View Pull Request diff:

```bash
gh pr diff
```

Merge Pull Request:

```bash
gh pr merge
```

List issues:

```bash
gh issue list
```

Create issue:

```bash
gh issue create
```

View GitHub Actions runs:

```bash
gh run list
```

## Full Example Workflow

```bash
git switch main
git pull

git switch -c docs/github-cli-gh

# edit files

git status
git add github-cli-gh.md
git commit -m "docs: add GitHub CLI notes"

git push -u origin docs/github-cli-gh

gh pr create \
  --base main \
  --head docs/github-cli-gh \
  --title "Add GitHub CLI notes" \
  --body "Added beginner notes for using GitHub CLI."
```

After creating the Pull Request:

```bash
gh pr view --web
```

## Common Mistakes

### Not Logged In

Error:

```text
You are not logged into any GitHub hosts
```

Fix:

```bash
gh auth login
```

### Creating PR Before Pushing Branch

Bad:

```bash
gh pr create
```

before pushing the branch.

Better:

```bash
git push -u origin branch-name
gh pr create
```

### Wrong Base Branch

If your Pull Request should go to `main`, use:

```bash
gh pr create --base main
```

If your team uses `develop`, use:

```bash
gh pr create --base develop
```

### Not Inside a Git Repository

If you see an error, make sure you are inside a Git project:

```bash
git status
```

## Git vs GitHub CLI

| Git                       | GitHub CLI                           |
| ------------------------- | ------------------------------------ |
| Manages local Git history | Manages GitHub actions from terminal |
| `git commit`              | `gh pr create`                       |
| `git push`                | `gh pr view`                         |
| `git branch`              | `gh issue list`                      |
| Works with Git            | Works with GitHub                    |

## Summary

```text
gh auth login  → Login to GitHub
gh repo clone  → Clone a repository
gh repo create → Create a repository
gh pr create   → Create a Pull Request
gh pr list     → List Pull Requests
gh pr view     → View Pull Request details
gh pr diff     → View Pull Request changes
gh pr merge    → Merge Pull Request
gh issue       → Manage GitHub Issues
gh run         → Manage GitHub Actions runs
```

> GitHub CLI lets you control GitHub from the terminal without leaving your workflow.

