# Semantic Versioning

**Semantic Versioning** is a way to number software versions clearly.

It uses this format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.4.2
```

Meaning:

```text
1 → MAJOR
4 → MINOR
2 → PATCH
```

## Why Do We Need Semantic Versioning?

Version numbers help developers understand what changed in the application.

Instead of using random numbers like:

```text
version 1
version 2
version 3
```

Semantic Versioning tells us if the change is:

```text
breaking change
new feature
bug fix
```

## Version Format

```text
MAJOR.MINOR.PATCH
```

Example:

```text
2.5.1
```

Explanation:

```text
2 → Major version
5 → Minor version
1 → Patch version
```

## 1. PATCH Version

Increase the **PATCH** number when you fix a bug without changing how the application works.

Example:

```text
1.0.0 → 1.0.1
```

Use PATCH for:

```text
Bug fixes
Small fixes
Security fixes
Typo fixes
```

Example:

```text
Fix login button not working

1.0.0 → 1.0.1
```

## 2. MINOR Version

Increase the **MINOR** number when you add a new feature without breaking old functionality.

Example:

```text
1.0.1 → 1.1.0
```

Use MINOR for:

```text
New feature
New endpoint
New option
New page
```

Example:

```text
Add user profile page

1.0.1 → 1.1.0
```

Old users can still use the app normally.

## 3. MAJOR Version

Increase the **MAJOR** number when you make a breaking change.

A breaking change means old code or old users may need to change something.

Example:

```text
1.1.0 → 2.0.0
```

Use MAJOR for:

```text
Breaking API change
Removing old feature
Changing important behavior
Changing database structure in a breaking way
```

Example:

```text
Remove old login API and replace it with a new one

1.1.0 → 2.0.0
```

## Simple Rule

```text
PATCH → Fix
MINOR → Add
MAJOR → Break
```

## Version Examples

| Change          | Old Version | New Version |
| --------------- | ----------: | ----------: |
| Fix small bug   |       1.0.0 |       1.0.1 |
| Add new feature |       1.0.1 |       1.1.0 |
| Breaking change |       1.1.0 |       2.0.0 |

## Real Example

You have this version:

```text
1.2.3
```

If you fix a bug:

```text
1.2.3 → 1.2.4
```

If you add a new feature:

```text
1.2.3 → 1.3.0
```

If you make a breaking change:

```text
1.2.3 → 2.0.0
```

## Pre-release Versions

Sometimes the version is not stable yet.

Examples:

```text
1.0.0-alpha
1.0.0-beta
1.0.0-rc.1
```

Meaning:

```text
alpha → early testing version
beta  → testing version before stable
rc    → release candidate, almost ready
```

## Version Tags in Git

In Git, versions are often saved as tags.

Example:

```bash
git tag v1.0.0
```

Push the tag to GitHub:

```bash
git push origin v1.0.0
```

List tags:

```bash
git tag
```

Delete a local tag:

```bash
git tag -d v1.0.0
```

Delete a remote tag:

```bash
git push origin --delete v1.0.0
```

## Example Git Release Workflow

```bash
git switch main
git pull

git tag v1.0.0
git push origin v1.0.0
```

This marks the current code as version `v1.0.0`.

## Semantic Versioning in DevOps

Semantic Versioning is useful in DevOps because it helps with:

```text
Docker image tags
Helm chart versions
Application releases
CI/CD pipelines
Rollback decisions
Production deployments
```

Example Docker image:

```text
my-app:1.0.0
my-app:1.1.0
my-app:2.0.0
```

Example Helm chart:

```yaml
version: 0.1.0
appVersion: "1.0.0"
```

## Common Mistakes

### Using `latest` Only

Bad:

```text
my-app:latest
```

Better:

```text
my-app:1.0.0
```

Using clear versions makes rollback easier.

### Changing Major Version for Small Fixes

Bad:

```text
1.0.0 → 2.0.0
```

for a small typo fix.

Better:

```text
1.0.0 → 1.0.1
```

### Adding Feature as Patch

Bad:

```text
1.0.0 → 1.0.1
```

for a new feature.

Better:

```text
1.0.0 → 1.1.0
```

## Summary

```text
MAJOR → Breaking change
MINOR → New feature
PATCH → Bug fix
```

Example:

```text
1.2.3
│ │ │
│ │ └── PATCH
│ └──── MINOR
└────── MAJOR
```

> Semantic Versioning makes software releases clear, predictable, and easier to manage.

