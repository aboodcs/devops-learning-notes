# Helm Install, Upgrade, and Uninstall

Helm is used to manage Kubernetes applications through **releases**.

The main lifecycle is:

```text
install → upgrade → rollback → uninstall
```

## 1. Install a Helm Chart

The `helm install` command installs a chart into the Kubernetes cluster.

Basic syntax:

```bash
helm install RELEASE_NAME CHART_PATH
```

Example:

```bash
helm install web-app ./my-chart
```

Here:

```text
web-app    → Release name
./my-chart → Chart location
```

Check installed releases:

```bash
helm list
```

Check Kubernetes resources:

```bash
kubectl get all
```

## Install with Custom Values

You can install a chart using another values file:

```bash
helm install web-app ./my-chart -f values-dev.yaml
```

You can also override one value from the command line:

```bash
helm install web-app ./my-chart --set replicaCount=3
```

Example with image tag:

```bash
helm install web-app ./my-chart --set image.tag=alpine
```

## Install in a Namespace

Create a namespace:

```bash
kubectl create namespace development
```

Install the chart inside it:

```bash
helm install web-app ./my-chart -n development
```

Create namespace automatically if it does not exist:

```bash
helm install web-app ./my-chart -n development --create-namespace
```

Check releases in that namespace:

```bash
helm list -n development
```

## 2. Upgrade a Helm Release

The `helm upgrade` command updates an existing release.

Basic syntax:

```bash
helm upgrade RELEASE_NAME CHART_PATH
```

Example:

```bash
helm upgrade web-app ./my-chart
```

Use this after changing:

```text
values.yaml
templates/deployment.yaml
templates/service.yaml
image tag
replica count
service type
```

## Upgrade with New Values

```bash
helm upgrade web-app ./my-chart -f values-prod.yaml
```

Override a value:

```bash
helm upgrade web-app ./my-chart --set replicaCount=5
```

Upgrade image tag:

```bash
helm upgrade web-app ./my-chart --set image.tag=v2
```

Check the result:

```bash
helm status web-app
kubectl get all
```

## Install or Upgrade Together

Sometimes you want one command that installs the chart if it does not exist, or upgrades it if it already exists.

Use:

```bash
helm upgrade --install web-app ./my-chart
```

This is very useful in CI/CD pipelines.

With namespace:

```bash
helm upgrade --install web-app ./my-chart \
  -n development \
  --create-namespace
```

## 3. Check Release Status

View release status:

```bash
helm status web-app
```

View release history:

```bash
helm history web-app
```

View values used by the release:

```bash
helm get values web-app
```

View all values:

```bash
helm get values web-app --all
```

View generated Kubernetes YAML:

```bash
helm get manifest web-app
```

## 4. Rollback a Release

If an upgrade breaks the application, you can rollback to an older revision.

Check history:

```bash
helm history web-app
```

Example output:

```text
REVISION  UPDATED                  STATUS      CHART
1         2026-07-01 10:00:00      superseded  my-chart-0.1.0
2         2026-07-01 10:10:00      deployed    my-chart-0.1.0
```

Rollback to revision 1:

```bash
helm rollback web-app 1
```

Check status:

```bash
helm status web-app
```

Check Pods:

```bash
kubectl get pods
```

## 5. Uninstall a Helm Release

The `helm uninstall` command removes a release from the cluster.

```bash
helm uninstall web-app
```

Check that it was removed:

```bash
helm list
kubectl get all
```

If the release is inside a namespace:

```bash
helm uninstall web-app -n development
```

## Important Note About Uninstall

When you uninstall a release, Helm removes the Kubernetes resources created by that release.

Example:

```text
Deployment
Service
ConfigMap
Secret
Ingress
```

But some resources may remain depending on the chart, especially persistent data like:

```text
PersistentVolume
PersistentVolumeClaim
Database data
```

Always check:

```bash
kubectl get all,pvc -n development
```

## 6. Dry Run Before Installing or Upgrading

Use `--dry-run` to test without applying changes:

```bash
helm install web-app ./my-chart --dry-run
```

For upgrade:

```bash
helm upgrade web-app ./my-chart --dry-run
```

You can also render the final YAML:

```bash
helm template web-app ./my-chart
```

This helps you find errors before touching the cluster.

## 7. Debug Helm Commands

Use `--debug` to show more details:

```bash
helm install web-app ./my-chart --debug
```

With dry run:

```bash
helm install web-app ./my-chart --dry-run --debug
```

For upgrade:

```bash
helm upgrade web-app ./my-chart --dry-run --debug
```

## Full Example Workflow

```bash
helm lint ./my-chart

helm template web-app ./my-chart

helm install web-app ./my-chart

helm list

kubectl get all

helm upgrade web-app ./my-chart --set replicaCount=3

helm history web-app

helm rollback web-app 1

helm uninstall web-app
```

## Common Problems

### Release Already Exists

Error:

```text
cannot re-use a name that is still in use
```

Fix:

```bash
helm upgrade --install web-app ./my-chart
```

Or uninstall the old release:

```bash
helm uninstall web-app
```

### Release Not Found

Error:

```text
release: not found
```

Check releases:

```bash
helm list
helm list -A
```

Maybe the release is in another namespace.

### Chart Has Template Error

Check with:

```bash
helm lint ./my-chart
helm template web-app ./my-chart
```

### Pods Not Running After Install

Check Kubernetes resources:

```bash
kubectl get pods
kubectl describe pod POD_NAME
kubectl logs POD_NAME
```

## Useful Commands

Install:

```bash
helm install web-app ./my-chart
```

Install in namespace:

```bash
helm install web-app ./my-chart -n development --create-namespace
```

Upgrade:

```bash
helm upgrade web-app ./my-chart
```

Install or upgrade:

```bash
helm upgrade --install web-app ./my-chart
```

Rollback:

```bash
helm rollback web-app 1
```

Uninstall:

```bash
helm uninstall web-app
```

List releases:

```bash
helm list
```

List all namespaces:

```bash
helm list -A
```

View status:

```bash
helm status web-app
```

View history:

```bash
helm history web-app
```

## Summary

```text
helm install           → Install a chart as a release
helm upgrade           → Update an existing release
helm upgrade --install → Install if missing, upgrade if existing
helm rollback          → Return to an older revision
helm uninstall         → Remove the release
helm list              → Show installed releases
helm status            → Show release details
helm history           → Show release revisions
```

> Helm install creates the application, upgrade changes it, rollback fixes broken updates, and uninstall removes it.

