# Helm History and Rollback

Helm keeps a history for every installed release.

This history is useful because if an upgrade breaks the application, you can return to an older working version.

```text id="xqt59z"
install → revision 1
upgrade → revision 2
upgrade → revision 3
rollback → return to older revision
```

## What Is a Helm Revision?

A **revision** is a version of a Helm release.

Every time you install or upgrade a release, Helm creates a new revision.

Example:

```text id="sk973b"
Revision 1 → First install
Revision 2 → First upgrade
Revision 3 → Second upgrade
```

## Check Installed Releases

```bash id="bmj2hn"
helm list
```

Example output:

```text id="gw4k6d"
NAME      NAMESPACE  REVISION  STATUS    CHART
web-app   default    3         deployed  nginx-chart-0.1.0
```

This means the release `web-app` is currently on revision `3`.

## View Release History

```bash id="noo1ui"
helm history web-app
```

Example output:

```text id="sc2f6g"
REVISION  UPDATED                  STATUS      CHART              DESCRIPTION
1         2026-07-01 10:00:00      superseded  nginx-chart-0.1.0  Install complete
2         2026-07-01 10:15:00      superseded  nginx-chart-0.1.0  Upgrade complete
3         2026-07-01 10:30:00      deployed    nginx-chart-0.1.0  Upgrade complete
```

Meaning:

```text id="nb1wk8"
superseded → Old revision
deployed   → Current active revision
```

## Upgrade Example

Change a value:

```bash id="3zhm7i"
helm upgrade web-app ./nginx-chart --set replicaCount=4
```

Check history again:

```bash id="d0k6k9"
helm history web-app
```

Now Helm creates a new revision.

## Rollback to an Older Revision

If the new version has a problem, rollback:

```bash id="sryfte"
helm rollback web-app 2
```

This returns the release to revision `2`.

Check status:

```bash id="olxt1m"
helm status web-app
```

Check Pods:

```bash id="i1s51x"
kubectl get pods
```

Check history:

```bash id="c75r5s"
helm history web-app
```

Important: rollback also creates a new revision.

Example:

```text id="cmevjh"
Revision 1 → Install
Revision 2 → Upgrade
Revision 3 → Bad upgrade
Revision 4 → Rollback to revision 2
```

So rollback does not delete history. It adds a new revision based on an old one.

## Rollback to the Previous Revision

If you want to rollback to the previous working version, first check history:

```bash id="rutxbc"
helm history web-app
```

Then choose the revision number:

```bash id="ldix97"
helm rollback web-app 2
```

## Check What Changed

View the current values:

```bash id="n3lw3o"
helm get values web-app
```

View all values:

```bash id="pkkskj"
helm get values web-app --all
```

View the generated YAML:

```bash id="anxy92"
helm get manifest web-app
```

These commands help you understand what Helm applied to Kubernetes.

## Rollback in a Namespace

If the release is inside a namespace, add `-n`.

```bash id="kvn437"
helm history web-app -n development
```

Rollback:

```bash id="wjcd2l"
helm rollback web-app 2 -n development
```

Check:

```bash id="237amo"
helm status web-app -n development
```

## Common Rollback Scenario

Imagine you installed an app:

```bash id="9q3ixs"
helm install web-app ./nginx-chart
```

Then upgraded it:

```bash id="u1v22u"
helm upgrade web-app ./nginx-chart --set image.tag=wrong-version
```

Pods start failing.

Check Pods:

```bash id="vfqx2j"
kubectl get pods
```

Check history:

```bash id="zixbik"
helm history web-app
```

Rollback:

```bash id="2102uj"
helm rollback web-app 1
```

Check again:

```bash id="wef9y6"
kubectl get pods
helm status web-app
```

## Useful Commands

List releases:

```bash id="dugonz"
helm list
```

View release history:

```bash id="xfce8g"
helm history web-app
```

View release status:

```bash id="ux9xca"
helm status web-app
```

Rollback to revision 1:

```bash id="4je6qr"
helm rollback web-app 1
```

Rollback in namespace:

```bash id="yhq7vu"
helm rollback web-app 1 -n development
```

View current values:

```bash id="3ltu1x"
helm get values web-app
```

View generated YAML:

```bash id="u0w4yp"
helm get manifest web-app
```

## Summary

```text id="yf8k47"
helm history  → Shows all release revisions
revision      → Version of a Helm release
deployed      → Current active revision
superseded    → Old revision
helm rollback → Returns to an older revision
```

> Helm history shows what happened to a release, and rollback helps you recover when an upgrade breaks the application.

