# Git Flow

**Git Flow** is a branching strategy used to organize work in a Git project.

It gives every type of work its own branch.

```text
main      → production-ready code
develop   → latest development code
feature   → new features
release   → prepare a new version
hotfix    → urgent fix for production
```

## Why Do We Need Git Flow?

Without a clear branching strategy, the project can become messy.

People may push unfinished work to the main branch, and that can break the project.

Git Flow helps keep the project organized:

```text
New feature  → feature branch
Testing      → develop branch
Release prep → release branch
Production   → main branch
Urgent fix   → hotfix branch
```

## Main Git Flow Branches

## 1. main Branch

The `main` branch contains stable production code.

This branch should always be safe.

```text
main = production-ready version
```

Usually, you do not work directly on `main`.

## 2. develop Branch

The `develop` branch contains the latest development work.

New features are merged into `develop` first.

```text
develop = testing and integration branch
```

When the code in `develop` is ready, it can be prepared for release.

## 3. feature Branch

A `feature` branch is used to build a new feature.

Example:

```bash
git switch develop
git pull
git switch -c feature/login-page
```

Work on your files:

```bash
git add .
git commit -m "add login page"
```

Push the branch:

```bash
git push -u origin feature/login-page
```

Then open a Pull Request into `develop`.

```text
feature/login-page → develop
```

## 4. release Branch

A `release` branch is used when the next version is almost ready.

Example:

```bash
git switch develop
git pull
git switch -c release/v1.0.0
```

This branch is used for:

```text
final testing
bug fixes
version update
documentation update
```

When ready, merge it into `main` and `develop`.

```text
release/v1.0.0 → main
release/v1.0.0 → develop
```

## 5. hotfix Branch

A `hotfix` branch is used to fix an urgent problem in production.

It starts from `main`.

Example:

```bash
git switch main
git pull
git switch -c hotfix/fix-login-error
```

After fixing:

```bash
git add .
git commit -m "fix login error"
```

Merge it into both `main` and `develop`.

```text
hotfix/fix-login-error → main
hotfix/fix-login-error → develop
```

This keeps production fixed and also keeps development updated.

## Git Flow Diagram

```text
main:     ●──────────────●──────────────●
           \              \              \
release:    \────●────●────\              \
              \             \              \
develop:  ●────●────●────●────●────●────●
             \      \         \
feature:      ●──────●         \
                         hotfix ●──●
```

## Simple Git Flow Lifecycle

```text
1. Create feature branch from develop
2. Work on the feature
3. Merge feature into develop
4. Create release branch from develop
5. Test and fix release branch
6. Merge release into main
7. Merge release back into develop
8. Use hotfix branch if production breaks
```

## Example Workflow

Create `develop` branch:

```bash
git switch main
git pull
git switch -c develop
git push -u origin develop
```

Create a feature branch:

```bash
git switch develop
git pull
git switch -c feature/docker-notes
```

Commit your work:

```bash
git add .
git commit -m "add docker notes"
```

Push it:

```bash
git push -u origin feature/docker-notes
```

Open a Pull Request:

```text
feature/docker-notes → develop
```

Prepare a release:

```bash
git switch develop
git pull
git switch -c release/v1.0.0
```

Merge release into main:

```bash
git switch main
git pull
git merge release/v1.0.0
git tag v1.0.0
git push origin main --tags
```

Merge release back into develop:

```bash
git switch develop
git merge release/v1.0.0
git push origin develop
```

Delete the release branch:

```bash
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

## Branch Naming Examples

```text
feature/add-login
feature/docker-compose
feature/kubernetes-service

release/v1.0.0
release/v2.1.0

hotfix/fix-env-error
hotfix/security-patch
```

## Git Flow vs Simple Branching

| Simple Branching          | Git Flow                                |
| ------------------------- | --------------------------------------- |
| main + feature branches   | main, develop, feature, release, hotfix |
| Easier for small projects | Better for larger projects              |
| Faster workflow           | More organized workflow                 |
| Less structure            | More control                            |

## When Should You Use Git Flow?

Use Git Flow when:

```text
The project has many developers
The project has production releases
You need release versions
You need hotfix branches
You want organized teamwork
```

For small personal projects, simple branching may be enough.

## Summary

```text
main     → Stable production code
develop  → Latest development code
feature  → New feature work
release  → Prepare a version for production
hotfix   → Emergency production fix
```

> Git Flow organizes branches so teams can build features, prepare releases, and fix production safely.

