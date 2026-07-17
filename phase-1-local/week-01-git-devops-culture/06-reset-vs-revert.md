# Reset vs Revert

In Git, **reset** and **revert** are used to undo changes.

But they work in different ways.

```text id="6978fr"
git reset  → moves history back
git revert → creates a new commit that undoes old changes
```

## Simple Difference

```text id="dhfwqk"
reset  → removes or moves commits from history
revert → keeps history and adds a new undo commit
```

## Example Situation

You have this Git history:

```text id="s4kzg2"
A---B---C
```

Commit `C` has a mistake.

You want to undo it.

You can use:

```bash id="vib6yr"
git reset
```

or:

```bash id="7b5tyt"
git revert
```

## 1. Git Reset

**Reset** moves your branch back to an older commit.

Example:

```bash id="h6bncv"
git reset --soft HEAD~1
```

or:

```bash id="kp4e27"
git reset --hard HEAD~1
```

Before reset:

```text id="zfmwvk"
A---B---C
```

After reset:

```text id="fezq4y"
A---B
```

Commit `C` is removed from the current branch history.

## Types of Reset

## Soft Reset

```bash id="rz02cb"
git reset --soft HEAD~1
```

This removes the last commit, but keeps the changes staged.

Meaning:

```text id="3uuiwi"
Commit removed
Files still staged
Changes not lost
```

Use it when you want to rewrite the last commit.

Example:

```bash id="zq81wl"
git reset --soft HEAD~1
git commit -m "better commit message"
```

## Mixed Reset

```bash id="kqsj0h"
git reset --mixed HEAD~1
```

This removes the last commit and unstages the changes.

Meaning:

```text id="rw18m2"
Commit removed
Files kept
Changes unstaged
```

This is the default reset type.

So this:

```bash id="49zngf"
git reset HEAD~1
```

is the same as:

```bash id="ahmg01"
git reset --mixed HEAD~1
```

## Hard Reset

```bash id="8ag3gp"
git reset --hard HEAD~1
```

This removes the last commit and deletes the file changes.

Meaning:

```text id="gjo41e"
Commit removed
Changes deleted
Very dangerous
```

Use it carefully.

If the changes are important, do not use `--hard`.

## 2. Git Revert

**Revert** creates a new commit that undoes another commit.

Example:

```bash id="e21n29"
git revert HEAD
```

Before revert:

```text id="1zf9rn"
A---B---C
```

After revert:

```text id="kh7xkr"
A---B---C---D
```

Commit `D` undoes the changes from commit `C`.

The history is not deleted.

## Why Revert Is Safer

Revert keeps the full history.

That means everyone can see:

```text id="r2e37s"
The bad commit happened
Then another commit fixed it
```

This is safer when the commit was already pushed to GitHub.

## Reset vs Revert Diagram

### Reset

```text id="3rxyuu"
Before:
A---B---C

After:
A---B
```

Reset moves the branch backward.

### Revert

```text id="r77km8"
Before:
A---B---C

After:
A---B---C---D
```

Revert adds a new commit that cancels the old one.

## Main Difference

| Reset                          | Revert                       |
| ------------------------------ | ---------------------------- |
| Moves history backward         | Adds a new undo commit       |
| Can remove commits             | Keeps all commits            |
| Dangerous with shared branches | Safe for shared branches     |
| Good for local mistakes        | Good after pushing to GitHub |
| `--hard` can delete work       | Does not delete history      |

## When to Use Reset

Use `reset` when:

```text id="dtrw68"
The commit is only local
You have not pushed it yet
You want to rewrite your last commit
You want to unstage files
```

Example:

```bash id="xgf4zh"
git reset --soft HEAD~1
```

Good for fixing your last local commit.

## When to Use Revert

Use `revert` when:

```text id="59m1xd"
The commit was already pushed
Other people may have pulled it
You want a safe undo
You want to keep history clean and honest
```

Example:

```bash id="gje4xi"
git revert HEAD
git push
```

Good for undoing a pushed commit safely.

## Common Examples

## Undo Last Local Commit but Keep Changes

```bash id="m5l2qg"
git reset --soft HEAD~1
```

Use this when you committed too early.

## Undo Last Local Commit and Unstage Changes

```bash id="abqw3y"
git reset HEAD~1
```

Use this when you want the files back as normal modified files.

## Delete Last Local Commit and Changes

```bash id="8vj3f7"
git reset --hard HEAD~1
```

Use carefully. This deletes the changes.

## Undo a Pushed Commit Safely

```bash id="2u623a"
git revert HEAD
git push
```

This is the safest way after pushing.

## Revert a Specific Commit

First, find the commit hash:

```bash id="vxckpx"
git log --oneline
```

Example output:

```text id="nyglax"
a1b2c3d add docker notes
e4f5g6h fix typo
```

Revert a specific commit:

```bash id="041mh3"
git revert a1b2c3d
```

## Reset to a Specific Commit

Find the commit:

```bash id="40fbju"
git log --oneline
```

Reset to it:

```bash id="wwsrhi"
git reset --hard a1b2c3d
```

This makes the branch point to that commit.

Be careful because commits after it may be removed from the branch history.

## Important Rule

```text id="ibv2mh"
If you already pushed the commit, prefer git revert.
If the commit is only local, git reset is okay.
```

## Dangerous Command

Be careful with:

```bash id="8hl7k7"
git reset --hard
```

It can delete uncommitted changes.

Before using it, check:

```bash id="zbcccz"
git status
```

## Recovery Tip

If you reset by mistake, Git may still know the old commit.

Use:

```bash id="od97y7"
git reflog
```

Then you can find the old commit and recover it.

Example:

```bash id="hc52iu"
git reset --hard OLD_COMMIT_HASH
```

## Reset vs Revert in Real Work

For your own local branch:

```text id="q1zs2f"
reset is okay
```

For a shared branch or GitHub branch:

```text id="m0re77"
revert is safer
```

## Useful Commands

View commit history:

```bash id="sv8nd5"
git log --oneline
```

Undo last commit but keep staged changes:

```bash id="j7ijsu"
git reset --soft HEAD~1
```

Undo last commit and unstage changes:

```bash id="94c2oc"
git reset HEAD~1
```

Delete last commit and changes:

```bash id="6yc42x"
git reset --hard HEAD~1
```

Safely undo last commit:

```bash id="r9f3zd"
git revert HEAD
```

Recover old history:

```bash id="rs1s95"
git reflog
```

## Summary

```text id="8s3fzk"
git reset --soft  → Remove commit, keep changes staged
git reset --mixed → Remove commit, keep changes unstaged
git reset --hard  → Remove commit and delete changes
git revert        → Add a new commit that undoes another commit
```

> Reset rewrites history. Revert preserves history. Use reset for local mistakes and revert for pushed commits.

