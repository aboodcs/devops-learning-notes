# Helm Core Concepts

**Helm** is a package manager for Kubernetes.

It helps you install and manage Kubernetes applications using something called a **Chart**.

```text
Helm Chart → Kubernetes YAML → Kubernetes Cluster
```

Without Helm, you write many YAML files manually:

```text
deployment.yaml
service.yaml
configmap.yaml
secret.yaml
ingress.yaml
```

With Helm, you put them inside one reusable package.

## Main Helm Concepts

```text
Chart       → Package of Kubernetes files
Release     → Installed copy of a chart
Values      → Configuration for the chart
Templates   → Dynamic Kubernetes YAML files
Repository  → Place where charts are stored
```

## 1. Chart

A **Chart** is a Helm package.

It contains Kubernetes YAML templates and configuration files.

Example chart structure:

```text
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

A chart is like a ready application package.

Example:

```text
nginx chart
mysql chart
redis chart
flask app chart
```

## 2. Release

A **Release** is an installed chart inside Kubernetes.

Example:

```bash
helm install web-app ./my-chart
```

Here:

```text
web-app     → Release name
./my-chart  → Chart location
```

You can install the same chart many times with different release names:

```bash
helm install dev-web ./my-chart
helm install prod-web ./my-chart
```

Same chart, different releases.

## 3. Values

**Values** are configuration settings for a chart.

They are usually written inside:

```text
values.yaml
```

Example:

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine

service:
  type: NodePort
  port: 80
```

Values allow you to change the application behavior without editing the Kubernetes templates directly.

Example:

```text
Change replicas from 2 to 4
Change image tag
Change service type
Change port
```

## 4. Templates

**Templates** are Kubernetes YAML files that use Helm variables.

Example template:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment

spec:
  replicas: {{ .Values.replicaCount }}

  selector:
    matchLabels:
      app: {{ .Release.Name }}

  template:
    metadata:
      labels:
        app: {{ .Release.Name }}

    spec:
      containers:
        - name: nginx
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

This part:

```text
{{ .Values.replicaCount }}
```

gets the value from `values.yaml`.

This part:

```text
{{ .Release.Name }}
```

gets the release name from the Helm command.

## 5. Chart.yaml

`Chart.yaml` contains information about the chart.

Example:

```yaml
apiVersion: v2
name: my-chart
description: A simple Kubernetes application chart
type: application
version: 0.1.0
appVersion: "1.0"
```

Important fields:

```text
name        → Chart name
description → Short explanation
version     → Chart version
appVersion  → Application version
```

## 6. values.yaml

`values.yaml` contains the default configuration.

Example:

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine

service:
  type: ClusterIP
  port: 80
```

The templates read these values and generate the final Kubernetes YAML.

## 7. Helm Repository

A **Helm repository** is a place where charts are stored.

Example:

```text
Bitnami Helm Repository
Prometheus Helm Repository
Nginx Helm Repository
```

Add a repository:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Update repositories:

```bash
helm repo update
```

Search for charts:

```bash
helm search repo nginx
```

## Helm Workflow

```text
1. Create or download a chart
2. Edit values.yaml
3. Render the templates
4. Install the chart
5. Upgrade when needed
6. Roll back if something breaks
7. Uninstall when finished
```

## Important Helm Commands

Create a chart:

```bash
helm create my-chart
```

Render templates without installing:

```bash
helm template web-app ./my-chart
```

Install a chart:

```bash
helm install web-app ./my-chart
```

List installed releases:

```bash
helm list
```

Upgrade a release:

```bash
helm upgrade web-app ./my-chart
```

Check release status:

```bash
helm status web-app
```

View release history:

```bash
helm history web-app
```

Rollback:

```bash
helm rollback web-app 1
```

Uninstall:

```bash
helm uninstall web-app
```

## Helm vs Normal Kubernetes YAML

| Normal YAML         | Helm                 |
| ------------------- | -------------------- |
| Many separate files | One reusable chart   |
| Manual changes      | Change values.yaml   |
| Harder to reuse     | Easy to reuse        |
| No release history  | Has release history  |
| Rollback is manual  | Rollback is built in |

## Simple Example

Normal Kubernetes way:

```text
deployment.yaml
service.yaml
configmap.yaml
```

Helm way:

```text
my-chart/
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

Then install everything with:

```bash
helm install web-app ./my-chart
```

## Summary

```text
Helm        → Package manager for Kubernetes
Chart       → Package containing Kubernetes templates
Release     → Installed chart in the cluster
Values      → Configuration for the chart
Templates   → Dynamic YAML files
Chart.yaml  → Chart information
values.yaml → Default chart configuration
Repository  → Online place for charts
```

> Helm makes Kubernetes YAML reusable, configurable, and easier to manage.

