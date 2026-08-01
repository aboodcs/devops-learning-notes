# Kubernetes Namespace

A **Namespace** is used to organize resources inside a Kubernetes cluster.

It helps separate applications, teams, or environments.

Example:

```text id="hh8g8e"
Kubernetes Cluster
├── development namespace
├── testing namespace
└── production namespace
```

Each namespace can contain its own:

```text id="qtq8ib"
Pods
Deployments
Services
ConfigMaps
Secrets
```

## Why Do We Need Namespaces?

Without namespaces, all resources are created in the same default area.

This can become messy when you have many applications.

Namespaces help you organize the cluster.

Example:

```text id="v49m6l"
development → For testing new changes
staging     → For testing before production
production  → For real users
```

## Check Existing Namespaces

```bash id="p4dg9b"
kubectl get namespaces
```

Short command:

```bash id="vofcdf"
kubectl get ns
```

You may see:

```text id="j148gs"
default
kube-system
kube-public
kube-node-lease
```

## Common Default Namespaces

### `default`

This is where resources are created if you do not choose another namespace.

### `kube-system`

This contains Kubernetes system components.

Do not delete resources from this namespace unless you know what you are doing.

### `kube-public`

This is used for public cluster information.

### `kube-node-lease`

This is used by Kubernetes nodes to report health information.

## Create a Namespace

Create a namespace directly:

```bash id="0f4s55"
kubectl create namespace development
```

Check it:

```bash id="qgw39h"
kubectl get namespaces
```

## Create Namespace Using YAML

Create a file:

```text id="nn8wug"
namespace.yaml
```

Add:

```yaml id="bd6c9n"
apiVersion: v1
kind: Namespace
metadata:
  name: development
```

Apply it:

```bash id="t8e051"
kubectl apply -f namespace.yaml
```

## Create Resources Inside a Namespace

Create a Pod in the `development` namespace:

```yaml id="tgmt61"
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  namespace: development

spec:
  containers:
    - name: nginx
      image: nginx:alpine
```

Apply it:

```bash id="p5q02e"
kubectl apply -f pod.yaml
```

Check Pods inside the namespace:

```bash id="8hvls7"
kubectl get pods -n development
```

## Create a Deployment Inside a Namespace

```yaml id="hz99k8"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: development

spec:
  replicas: 2

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
```

Apply it:

```bash id="vsykku"
kubectl apply -f deployment.yaml
```

Check it:

```bash id="v4ai4r"
kubectl get deployments -n development
```

Check Pods:

```bash id="3bxvt5"
kubectl get pods -n development
```

## Create a Service Inside a Namespace

```yaml id="pzsg0p"
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: development

spec:
  selector:
    app: nginx

  ports:
    - port: 80
      targetPort: 80

  type: ClusterIP
```

Apply it:

```bash id="htmx1s"
kubectl apply -f service.yaml
```

Check Services:

```bash id="zjzkam"
kubectl get services -n development
```

## View All Resources in a Namespace

```bash id="v0zlg8"
kubectl get all -n development
```

This shows:

```text id="fg5d62"
Pods
Services
Deployments
ReplicaSets
```

## Use Namespace with Commands

Instead of writing the namespace inside YAML, you can use `-n`.

Example:

```bash id="yknbxm"
kubectl get pods -n development
```

```bash id="74u8kq"
kubectl describe pod nginx-pod -n development
```

```bash id="8n4mab"
kubectl logs pod-name -n development
```

```bash id="kba6pu"
kubectl delete pod nginx-pod -n development
```

## Set a Default Namespace

If you do not want to write `-n development` every time, set it as the default namespace:

```bash id="zjltcb"
kubectl config set-context --current --namespace=development
```

Now this command:

```bash id="9080sl"
kubectl get pods
```

will show Pods from the `development` namespace.

Check the current namespace:

```bash id="6old8z"
kubectl config view --minify | grep namespace
```

Return to the default namespace:

```bash id="0gm84l"
kubectl config set-context --current --namespace=default
```

## Same Resource Name in Different Namespaces

You can have the same resource name in different namespaces.

Example:

```text id="jp889s"
development/nginx-deployment
production/nginx-deployment
```

They are separate resources.

This helps teams use the same names without conflicts.

## Namespace Example Structure

```text id="bwi4by"
development namespace
├── nginx-deployment
├── nginx-service
└── app-config

production namespace
├── nginx-deployment
├── nginx-service
└── app-config
```

The resources are separated even if they have the same names.

## Delete a Namespace

Delete the namespace:

```bash id="rvn0su"
kubectl delete namespace development
```

Important:

```text id="3cojs9"
Deleting a namespace deletes all resources inside it.
```

So if `development` contains Pods, Deployments, Services, ConfigMaps, and Secrets, they will all be deleted.

## Useful Commands

View namespaces:

```bash id="v7u1od"
kubectl get namespaces
```

Create namespace:

```bash id="v9u9jb"
kubectl create namespace development
```

View resources inside namespace:

```bash id="52ogus"
kubectl get all -n development
```

Describe namespace:

```bash id="s3t2bd"
kubectl describe namespace development
```

Set default namespace:

```bash id="a6p56e"
kubectl config set-context --current --namespace=development
```

Delete namespace:

```bash id="qj3g9j"
kubectl delete namespace development
```

## Summary

```text id="b7w8ju"
Namespace → Separates resources inside one Kubernetes cluster
default   → The namespace used when no namespace is selected
-n        → Short option to choose a namespace
```

> A Namespace is like a folder inside Kubernetes. It keeps resources organized and separated.

