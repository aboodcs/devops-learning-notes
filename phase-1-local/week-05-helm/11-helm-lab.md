# 09 - Helm Lab

This lab will help you practice Helm by creating a simple Nginx Helm chart, installing it, upgrading it, checking history, rolling back, and uninstalling it.

## Lab Goal

By the end of this lab, you should understand:

```text
Create Helm chart
Edit values.yaml
Render templates
Install release
Upgrade release
Rollback release
Uninstall release
```

## 1. Create a Helm Chart

Create a new chart:

```bash
helm create nginx-chart
```

Enter the chart folder:

```bash
cd nginx-chart
```

Check the structure:

```bash
tree
```

You should see something like:

```text
nginx-chart/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
```

## 2. Edit values.yaml

Open `values.yaml`:

```bash
nano values.yaml
```

Change the important values:

```yaml
replicaCount: 2

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "alpine"

service:
  type: NodePort
  port: 80
```

This means:

```text
replicaCount: 2  → Run 2 Pods
image: nginx     → Use Nginx image
tag: alpine      → Use alpine version
service: NodePort → Expose app outside the cluster
port: 80         → Service port
```

Save and exit:

```text
Ctrl + O
Enter
Ctrl + X
```

## 3. Check the Chart

Run Helm lint:

```bash
helm lint .
```

Expected result:

```text
1 chart(s) linted, 0 chart(s) failed
```

This means the chart has no basic errors.

## 4. Render the YAML Before Installing

Run:

```bash
helm template hello-world .
```

This shows the final Kubernetes YAML that Helm will create.

This command does not install anything.

It only previews the result.

## 5. Install the Chart

Install the chart:

```bash
helm install hello-world .
```

Check Helm releases:

```bash
helm list
```

Check Kubernetes resources:

```bash
kubectl get all
```

You should see:

```text
deployment/hello-world-nginx-chart
service/hello-world-nginx-chart
pods created by the deployment
```

## 6. Check the Pods

```bash
kubectl get pods
```

You should see 2 Pods because `replicaCount` is `2`.

Example:

```text
hello-world-nginx-chart-xxxxx   1/1   Running
hello-world-nginx-chart-yyyyy   1/1   Running
```

## 7. Access the Application

Check the Service:

```bash
kubectl get svc
```

Because the Service type is `NodePort`, you can access it using Minikube:

```bash
minikube service hello-world-nginx-chart
```

Or get the URL:

```bash
minikube service hello-world-nginx-chart --url
```

Open the URL in the browser.

You should see the Nginx welcome page.

## 8. Upgrade the Release

Now change the number of replicas.

Open `values.yaml`:

```bash
nano values.yaml
```

Change:

```yaml
replicaCount: 2
```

to:

```yaml
replicaCount: 4
```

Upgrade the release:

```bash
helm upgrade hello-world .
```

Check the Pods:

```bash
kubectl get pods
```

Now you should see 4 Pods.

## 9. Upgrade Using --set

You can also upgrade without editing `values.yaml`.

```bash
helm upgrade hello-world . --set replicaCount=3
```

Check again:

```bash
kubectl get pods
```

Now you should see 3 Pods.

## 10. Check Helm History

View release history:

```bash
helm history hello-world
```

Example:

```text
REVISION  STATUS      DESCRIPTION
1         superseded  Install complete
2         superseded  Upgrade complete
3         deployed    Upgrade complete
```

Every install or upgrade creates a revision.

## 11. Rollback the Release

Rollback to revision 1:

```bash
helm rollback hello-world 1
```

Check history again:

```bash
helm history hello-world
```

Check Pods:

```bash
kubectl get pods
```

Rollback creates a new revision based on an old revision.

## 12. Check Release Details

View release status:

```bash
helm status hello-world
```

View values used by the release:

```bash
helm get values hello-world
```

View all values:

```bash
helm get values hello-world --all
```

View generated YAML:

```bash
helm get manifest hello-world
```

## 13. Install Same Chart Again

You can install the same chart again using another release name:

```bash
helm install hello-world-2 .
```

Check releases:

```bash
helm list
```

You should see:

```text
hello-world
hello-world-2
```

Same chart, different releases.

## 14. Uninstall Releases

Uninstall the first release:

```bash
helm uninstall hello-world
```

Uninstall the second release:

```bash
helm uninstall hello-world-2
```

Check:

```bash
helm list
kubectl get all
```

The releases should be removed.

## 15. Clean Up

Go back to the previous directory:

```bash
cd ..
```

Remove the chart folder if you no longer need it:

```bash
rm -rf nginx-chart
```

## Full Lab Commands

```bash
helm create nginx-chart
cd nginx-chart

helm lint .
helm template hello-world .

helm install hello-world .

helm list
kubectl get all
kubectl get pods
kubectl get svc

minikube service hello-world-nginx-chart --url

helm upgrade hello-world . --set replicaCount=4
kubectl get pods

helm history hello-world
helm rollback hello-world 1

helm status hello-world
helm get values hello-world
helm get manifest hello-world

helm uninstall hello-world
```

## Common Errors

### Release already exists

Error:

```text
cannot re-use a name that is still in use
```

Fix:

```bash
helm uninstall hello-world
```

Or use upgrade install:

```bash
helm upgrade --install hello-world .
```

### Pods not running

Check:

```bash
kubectl get pods
kubectl describe pod POD_NAME
kubectl logs POD_NAME
```

### Chart template error

Check:

```bash
helm lint .
helm template hello-world .
```

## Summary

```text
helm create      → Create chart
helm lint        → Check chart errors
helm template    → Preview Kubernetes YAML
helm install     → Install chart
helm upgrade     → Update release
helm history     → View revisions
helm rollback    → Return to older revision
helm uninstall   → Remove release
```

> This lab teaches the full Helm workflow: create, test, install, upgrade, rollback, and uninstall.

