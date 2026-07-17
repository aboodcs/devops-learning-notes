# Merge vs Rebase

In Git, **merge** and **rebase** are used to bring changes from one branch into another branch.

They both help combine work, but they create different Git history.

```text
merge  → combines branches and keeps history
rebase → moves commits and makes history cleaner
```

## Example Situation

You have two branches:

```text
main
feature-login
```

While you were working on `feature-login`, someone added new commits to `main`.

Now your branch is behind `main`.

```text
main:           A---B---C
                 \
feature-login:   D---E
```

You need to update your feature branch with the latest changes from `main`.

You can use:

```text
git merge
```

or:

```text
git rebase
```

## 1. Git Merge

**Merge** combines two branches and creates a new merge commit.

Example:

```bash
git switch feature-login
git merge main
```

Result:

```text
main:           A---B---C
                 \     \
feature-login:   D---E---M
```

`M` is a merge commit.

It means:

```text
Git joined main and feature-login together.
```

## When to Use Merge

Use merge when you want to keep the full branch history.

Merge is good when:

```text
You are working with a team
You want to show exactly when branches joined
You do not want to rewrite commits
You want the safest option
```

## Merge Example Workflow

```bash
git switch main
git pull

git switch feature-login
git merge main
```

If there are conflicts, fix them, then:

```bash
git add .
git commit
```

## 2. Git Rebase

**Rebase** moves your branch commits on top of another branch.

Example:

```bash
git switch feature-login
git rebase main
```

Before rebase:

```text
main:           A---B---C
                 \
feature-login:   D---E
```

After rebase:

```text
main:           A---B---C
                         \
feature-login:           D'---E'
```

The commits `D` and `E` are replayed after `C`.

They become new commits:

```text
D' and E'
```

because Git rewrites the commit history.

## When to Use Rebase

Use rebase when you want a clean, straight history.

Rebase is good when:

```text
You are working on your own branch
You want to update your branch from main
You want history to look linear
You have not shared the branch with others yet
```

## Rebase Example Workflow

```bash
git switch main
git pull

git switch feature-login
git rebase main
```

If there are conflicts, fix them, then:

```bash
git add .
git rebase --continue
```

If you want to cancel the rebase:

```bash
git rebase --abort
```

## Merge vs Rebase Diagram

### Merge

```text
A---B---C main
 \       \
  D---E---M feature-login
```

Merge keeps the branch shape.

### Rebase

```text
A---B---C main
         \
          D'---E' feature-login
```

Rebase makes the history straight.

## Main Difference

| Merge                     | Rebase                       |
| ------------------------- | ---------------------------- |
| Combines branches         | Moves commits                |
| Creates a merge commit    | Rewrites commits             |
| Keeps full history        | Makes history cleaner        |
| Safer for shared branches | Better for personal branches |
| History can look messy    | History looks linear         |

## Important Rule

Do not rebase a shared branch that other people are using.

Bad idea:

```bash
git rebase main
git push --force
```

This can confuse other developers because rebase changes commit history.

Safe rule:

```text
Use merge for shared branches.
Use rebase for your own local branch.
```

## Pull with Merge

Normal pull usually does:

```text
git fetch + git merge
```

Command:

```bash
git pull
```

This may create a merge commit.

## Pull with Rebase

You can pull using rebase:

```bash
git pull --rebase
```

This updates your branch and keeps the history cleaner.

Example:

```bash
git switch feature-login
git pull --rebase origin main
```

## Conflict in Merge

If merge has a conflict:

```bash
git merge main
```

Git may show:

```text
CONFLICT
```

Fix the file, then:

```bash
git add .
git commit
```

## Conflict in Rebase

If rebase has a conflict:

```bash
git rebase main
```

Fix the file, then:

```bash
git add .
git rebase --continue
```

Cancel rebase:

```bash
git rebase --abort
```

## Simple Example

You are working on a feature branch:

```bash
git switch -c feature/docker-notes
```

You make commits:

```bash
git add .
git commit -m "add docker notes"
```

Later, `main` gets updated.

Update your branch using merge:

```bash
git switch feature/docker-notes
git merge main
```

Or update your branch using rebase:

```bash
git switch feature/docker-notes
git rebase main
```

## Which One Should I Use?

For beginners:

```text
Use merge when you are not sure.
Use rebase when you understand history rewriting.
```

In real teamwork:

```text
Before Pull Request  → rebase can make your branch clean
After branch is shared → merge is safer
```

## Common Commands

Merge main into your branch:

```bash
git switch feature-branch
git merge main
```

Rebase your branch on main:

```bash
git switch feature-branch
git rebase main
```

Continue rebase after conflict:

```bash
git add .
git rebase --continue
```

Cancel rebase:

```bash
git rebase --abort
```

Pull with rebase:

```bash
git pull --rebase
```

## Summary

```text
merge  → keeps history and creates a merge commit
rebase → rewrites history and makes commits look linear
```

> Merge is safer and keeps the full story. Rebase is cleaner but must be used carefully.

