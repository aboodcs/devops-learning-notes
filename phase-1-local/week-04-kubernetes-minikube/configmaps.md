# Kubernetes ConfigMap

A **ConfigMap** is used to store normal application configuration outside the container image.

Examples of normal configuration:

```text
APP_MODE=production
APP_PORT=5000
DATABASE_HOST=postgres-service
DATABASE_PORT=5432
```

A ConfigMap is **not for passwords**.

Use ConfigMap for normal settings.
Use Secret for sensitive data.

## Why Do We Need ConfigMaps?

Without ConfigMap, you may write settings directly inside the application code or Docker image.

That is bad because every time you want to change a setting, you need to rebuild the image.

With ConfigMap, you can change the configuration without rebuilding the container image.

```text
Container Image → Application code
ConfigMap       → Application settings
```

## Simple Example

Create a file:

```text
configmap.yaml
```

Add:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config

data:
  APP_MODE: production
  APP_PORT: "5000"
  DATABASE_HOST: postgres-service
```

Apply it:

```bash
kubectl apply -f configmap.yaml
```

Check it:

```bash
kubectl get configmaps
```

Describe it:

```bash
kubectl describe configmap app-config
```

## Use ConfigMap as Environment Variables

Create a Pod that uses the ConfigMap:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod

spec:
  containers:
    - name: app
      image: nginx:alpine

      envFrom:
        - configMapRef:
            name: app-config
```

Apply it:

```bash
kubectl apply -f pod.yaml
```

Enter the Pod:

```bash
kubectl exec -it configmap-pod -- sh
```

Check the environment variables:

```bash
printenv APP_MODE
printenv APP_PORT
printenv DATABASE_HOST
```

Expected output:

```text
production
5000
postgres-service
```

## Use One Value from a ConfigMap

You can also use only one value from the ConfigMap:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: single-config-pod

spec:
  containers:
    - name: app
      image: nginx:alpine

      env:
        - name: MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
```

Inside the container, the variable will be:

```text
MODE=production
```

## Use ConfigMap as a File

Sometimes applications read configuration from files instead of environment variables.

Example ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config

data:
  default.conf: |
    server {
        listen 80;
        location / {
            return 200 "Hello from ConfigMap file!";
        }
    }
```

Mount it inside a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-config-pod

spec:
  containers:
    - name: nginx
      image: nginx:alpine

      volumeMounts:
        - name: config-volume
          mountPath: /etc/nginx/conf.d

  volumes:
    - name: config-volume
      configMap:
        name: nginx-config
```

Here, Kubernetes takes the ConfigMap data and places it as a file inside the container.

## ConfigMap with Deployment

In real projects, ConfigMaps are usually used with Deployments.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: my-app

  template:
    metadata:
      labels:
        app: my-app

    spec:
      containers:
        - name: app
          image: nginx:alpine

          envFrom:
            - configMapRef:
                name: app-config
```

This means every Pod created by the Deployment will receive the ConfigMap values.

## Important Notes

If you update a ConfigMap, the running Pod may not automatically reload the new values.

For environment variables, you usually need to restart the Pod:

```bash
kubectl delete pod configmap-pod
```

If the Pod is managed by a Deployment, Kubernetes will create a new Pod automatically.

For a Deployment, restart it with:

```bash
kubectl rollout restart deployment app-deployment
```

## Useful Commands

View ConfigMaps:

```bash
kubectl get configmaps
```

Short name:

```bash
kubectl get cm
```

Describe a ConfigMap:

```bash
kubectl describe configmap app-config
```

View ConfigMap YAML:

```bash
kubectl get configmap app-config -o yaml
```

Delete a ConfigMap:

```bash
kubectl delete configmap app-config
```

## ConfigMap vs Secret

| ConfigMap                   | Secret                     |
| --------------------------- | -------------------------- |
| Stores normal configuration | Stores sensitive data      |
| App mode, port, host        | Passwords, tokens, keys    |
| Safe for non-private values | Used for private values    |
| Example: `APP_MODE=dev`     | Example: `DB_PASSWORD=123` |

## Summary

```text
ConfigMap → Stores normal application configuration
Pod       → Uses the ConfigMap as environment variables or files
Deployment → Gives ConfigMap values to many Pods
```

> A ConfigMap separates application settings from the container image.

