# Kubernetes Secret

A **Secret** is used to store sensitive information in Kubernetes.

Examples of sensitive information:

```text
DATABASE_USERNAME=abood
DATABASE_PASSWORD=123abood
API_KEY=abcd1234
TOKEN=secret-token
SSH_PRIVATE_KEY=private-key
```

A Secret keeps sensitive values outside:

* Application code
* Docker image
* Kubernetes Pod YAML
* GitHub repository

## Why Do We Need Secrets?

Without Secrets, you may write passwords directly inside the Pod or Deployment file.

Bad example:

```yaml
env:
  - name: DATABASE_PASSWORD
    value: "123abood"
```

This is bad because the password is written directly in the YAML file.

With a Secret, the password is stored separately, and the Pod reads it when it starts.

```text
Secret      → Stores sensitive values
Pod         → Reads the Secret
Application → Uses the value
```

## Important Note

Kubernetes Secrets are not plain text in the YAML output. They are usually stored as **base64 encoded** values.

Base64 is not real encryption.

So do not upload real Secret files to GitHub.

Use Secrets for practice, but in production also use proper access control and secret management.

## Simple Secret Example

Create a file:

```text
secret.yaml
```

Add:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-secret

type: Opaque

stringData:
  DATABASE_USER: abood
  DATABASE_PASSWORD: 123abood
```

Apply it:

```bash
kubectl apply -f secret.yaml
```

Check it:

```bash
kubectl get secrets
```

Describe it:

```bash
kubectl describe secret database-secret
```

## `stringData` vs `data`

### `stringData`

With `stringData`, you write normal readable values:

```yaml
stringData:
  DATABASE_PASSWORD: 123abood
```

Kubernetes will encode the value automatically.

### `data`

With `data`, you must write the value in base64:

```yaml
data:
  DATABASE_PASSWORD: MTIzYWJvb2Q=
```

For beginners, `stringData` is easier.

## Use Secret as Environment Variables

Create a Pod that uses the Secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod

spec:
  containers:
    - name: app
      image: alpine
      command: ["sleep", "3600"]

      envFrom:
        - secretRef:
            name: database-secret
```

Apply it:

```bash
kubectl apply -f pod.yaml
```

Enter the Pod:

```bash
kubectl exec -it secret-pod -- sh
```

Check the variables:

```bash
printenv DATABASE_USER
printenv DATABASE_PASSWORD
```

Expected output:

```text
abood
123abood
```

Exit the Pod:

```bash
exit
```

## Use One Value from a Secret

You can also use only one value from the Secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: single-secret-pod

spec:
  containers:
    - name: app
      image: alpine
      command: ["sleep", "3600"]

      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: DATABASE_PASSWORD
```

Inside the container, the variable will be:

```text
DB_PASSWORD=123abood
```

## Use Secret as a File

Sometimes applications read secrets from files.

Create this Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret

type: Opaque

stringData:
  username: abood
  password: 123abood
```

Mount it inside a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-file-pod

spec:
  containers:
    - name: app
      image: alpine
      command: ["sleep", "3600"]

      volumeMounts:
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true

  volumes:
    - name: secret-volume
      secret:
        secretName: app-secret
```

Apply it:

```bash
kubectl apply -f secret-file-pod.yaml
```

Enter the Pod:

```bash
kubectl exec -it secret-file-pod -- sh
```

Check the mounted files:

```bash
ls /etc/secrets
```

You should see:

```text
username
password
```

Read the values:

```bash
cat /etc/secrets/username
cat /etc/secrets/password
```

## Secret with Deployment

In real projects, Secrets are usually used with Deployments.

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
          image: alpine
          command: ["sleep", "3600"]

          envFrom:
            - secretRef:
                name: database-secret
```

This means every Pod created by the Deployment will receive the Secret values.

## Create Secret from Command Line

You can create a Secret without writing YAML:

```bash
kubectl create secret generic database-secret \
  --from-literal=DATABASE_USER=abood \
  --from-literal=DATABASE_PASSWORD=123abood
```

Check it:

```bash
kubectl get secrets
```

View it as YAML:

```bash
kubectl get secret database-secret -o yaml
```

## Decode a Secret Value

Get the encoded password:

```bash
kubectl get secret database-secret \
  -o jsonpath="{.data.DATABASE_PASSWORD}"
```

Decode it:

```bash
kubectl get secret database-secret \
  -o jsonpath="{.data.DATABASE_PASSWORD}" | base64 -d
```

Expected output:

```text
123abood
```

## Important Security Rules

Do not upload real Secret YAML files to GitHub.

Add them to `.gitignore`:

```text
secret.yaml
*.secret.yaml
.env
```

Do not hardcode passwords inside:

* Dockerfile
* Pod YAML
* Deployment YAML
* Application code
* GitHub repository

Use Secrets for sensitive data and ConfigMaps for normal configuration.

## ConfigMap vs Secret

| ConfigMap                   | Secret                          |
| --------------------------- | ------------------------------- |
| Stores normal configuration | Stores sensitive data           |
| App mode, port, host        | Passwords, tokens, keys         |
| Not for private values      | Used for private values         |
| Example: `APP_MODE=dev`     | Example: `DB_PASSWORD=123abood` |

## Useful Commands

View Secrets:

```bash
kubectl get secrets
```

Describe a Secret:

```bash
kubectl describe secret database-secret
```

View Secret YAML:

```bash
kubectl get secret database-secret -o yaml
```

Delete a Secret:

```bash
kubectl delete secret database-secret
```

Check Secret values inside a Pod:

```bash
kubectl exec -it secret-pod -- printenv
```

## Summary

```text
Secret     → Stores sensitive information
Pod        → Uses Secret values as environment variables or files
Deployment → Gives Secret values to multiple Pods
```

> A Secret separates passwords and sensitive values from the application code and container image.

