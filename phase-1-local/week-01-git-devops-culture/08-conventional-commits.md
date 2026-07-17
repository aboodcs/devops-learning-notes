# Conventional Commits

**Conventional Commits** is a simple way to write clear Git commit messages.

It gives every commit a type, so people can quickly understand what changed.

```text
type: short message
```

Example:

```bash
git commit -m "feat: add login page"
```

## Why Do We Need Conventional Commits?

Normal commit messages can be unclear.

Bad examples:

```text
update
fix
changes
done
new stuff
```

Better examples:

```text
feat: add Docker Compose lab
fix: correct Kubernetes service port
docs: update README file
refactor: simplify Flask app structure
```

Conventional Commits help with:

```text
Clear project history
Better teamwork
Cleaner Pull Requests
Automatic changelogs
Versioning and releases
CI/CD pipelines
```

## Basic Format

```text
type: message
```

Example:

```text
docs: add Docker networking notes
```

The commit has two parts:

```text
docs     → type of change
message  → what changed
```

## Common Commit Types

```text
feat     → New feature
fix      → Bug fix
docs     → Documentation only
style    → Formatting changes
refactor → Code change without changing behavior
test     → Add or update tests
chore    → Maintenance task
ci       → CI/CD pipeline changes
build    → Build system or dependencies
perf     → Performance improvement
```

## 1. feat

Use `feat` when you add a new feature.

```bash
git commit -m "feat: add user login"
```

Examples:

```text
feat: add upload page
feat: add Redis visit counter
feat: add Kubernetes deployment file
```

## 2. fix

Use `fix` when you fix a bug.

```bash
git commit -m "fix: correct Redis connection host"
```

Examples:

```text
fix: correct Docker port mapping
fix: repair broken service selector
fix: handle missing environment variable
```

## 3. docs

Use `docs` when you change documentation only.

```bash
git commit -m "docs: add Docker networks notes"
```

Examples:

```text
docs: update README
docs: add Helm install guide
docs: explain Git branching workflow
```

## 4. style

Use `style` for formatting changes only.

This does not change the code logic.

```bash
git commit -m "style: format YAML files"
```

Examples:

```text
style: fix indentation
style: format Python code
style: clean markdown spacing
```

## 5. refactor

Use `refactor` when you improve code structure without changing behavior.

```bash
git commit -m "refactor: simplify Dockerfile structure"
```

Examples:

```text
refactor: reorganize Flask routes
refactor: clean Kubernetes manifests
refactor: improve Helm template names
```

## 6. test

Use `test` when you add or update tests.

```bash
git commit -m "test: add Flask health check test"
```

Examples:

```text
test: add API tests
test: update Docker build test
test: add Kubernetes manifest validation
```

## 7. chore

Use `chore` for maintenance tasks.

```bash
git commit -m "chore: update project folders"
```

Examples:

```text
chore: clean unused files
chore: update dependencies
chore: rename notes folder
```

## 8. ci

Use `ci` when changing CI/CD files.

```bash
git commit -m "ci: add GitHub Actions workflow"
```

Examples:

```text
ci: add Docker build pipeline
ci: run tests on pull request
ci: add Helm lint step
```

## 9. build

Use `build` for build system or dependency changes.

```bash
git commit -m "build: update Python base image"
```

Examples:

```text
build: add Dockerfile
build: update requirements.txt
build: change Node.js version
```

## 10. perf

Use `perf` for performance improvements.

```bash
git commit -m "perf: optimize Docker image size"
```

Examples:

```text
perf: reduce image layers
perf: improve database query speed
perf: cache Python dependencies
```

## Commit Message Examples

```text
feat: add Docker Compose app
fix: correct nginx service port
docs: add Kubernetes namespace notes
style: format markdown files
refactor: simplify Helm templates
test: add API health check test
chore: remove unused screenshots
ci: add GitHub Actions workflow
build: add multi-stage Dockerfile
perf: reduce Docker image size
```

## Commit with Scope

A scope explains which part of the project changed.

Format:

```text
type(scope): message
```

Examples:

```text
docs(docker): add networks notes
feat(k8s): add deployment manifest
fix(helm): correct service template
ci(github): add test workflow
```

This is useful in bigger projects.

## Breaking Change

A breaking change means the new change may break old behavior.

Use `!` after the type or scope:

```text
feat!: change API response format
```

Or:

```text
feat(api)!: remove old login endpoint
```

This usually means the major version should increase.

Example:

```text
1.4.2 → 2.0.0
```

## Conventional Commits and Semantic Versioning

Conventional Commits work well with Semantic Versioning.

```text
fix      → PATCH version
feat     → MINOR version
feat!    → MAJOR version
```

Example:

```text
fix: correct login bug        → 1.0.0 to 1.0.1
feat: add profile page        → 1.0.1 to 1.1.0
feat!: change authentication  → 1.1.0 to 2.0.0
```

## Good Commit Message Rules

A good commit message should be:

```text
Short
Clear
Specific
Written in present tense
Connected to one change
```

Bad:

```text
update
fix things
new files
final
```

Better:

```text
docs: add Docker security notes
fix: correct Redis service name
feat: add Flask upload endpoint
```

## Full Git Example

Create a branch:

```bash
git switch -c docs/conventional-commits
```

Edit your file.

Check changes:

```bash
git status
```

Add the file:

```bash
git add conventional-commits.md
```

Commit:

```bash
git commit -m "docs: add conventional commits notes"
```

Push:

```bash
git push -u origin docs/conventional-commits
```

## Common Mistakes

### Too Short

Bad:

```text
fix
```

Better:

```text
fix: correct Docker Compose port mapping
```

### Too General

Bad:

```text
docs: update
```

Better:

```text
docs: update Kubernetes service explanation
```

### Wrong Type

Bad:

```text
feat: fix typo in README
```

Better:

```text
docs: fix typo in README
```

### Too Many Changes in One Commit

Bad:

```text
feat: add Docker lab and fix Kubernetes service and update README
```

Better:

```text
feat: add Docker network lab
fix: correct Kubernetes service selector
docs: update README
```

## Useful Command Examples

Documentation change:

```bash
git commit -m "docs: add Helm values notes"
```

Bug fix:

```bash
git commit -m "fix: correct Kubernetes deployment label"
```

New feature:

```bash
git commit -m "feat: add Flask health endpoint"
```

CI/CD change:

```bash
git commit -m "ci: add GitHub Actions workflow"
```

Docker build change:

```bash
git commit -m "build: add optimized Dockerfile"
```

## Summary

```text
feat     → New feature
fix      → Bug fix
docs     → Documentation
style    → Formatting only
refactor → Code cleanup
test     → Tests
chore    → Maintenance
ci       → CI/CD
build    → Build or dependencies
perf     → Performance
```

> Conventional Commits make Git history clean, readable, and useful for releases.

