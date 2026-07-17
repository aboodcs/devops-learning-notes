# Helm Chart Structure

A **Helm Chart** is a folder that contains everything needed to deploy an application to Kubernetes.

It usually contains:

```text
Chart.yaml   → Chart information
values.yaml  → Default configuration
templates/   → Kubernetes YAML templates
charts/      → Extra chart dependencies
```

## Basic Chart Structure

When you create a chart:

```bash
helm create my-chart
```

Helm creates this structure:

```text
my-chart/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── serviceaccount.yaml
    ├── hpa.yaml
    ├── NOTES.txt
    └── _helpers.tpl
```

For beginners, focus on these files first:

```text
Chart.yaml
values.yaml
templates/deployment.yaml
templates/service.yaml
templates/_helpers.tpl
```

## 1. Chart.yaml

`Chart.yaml` contains information about the chart.

Example:

```yaml
apiVersion: v2
name: my-chart
description: A simple Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.0"
```

Explanation:

```text
apiVersion   → Helm chart API version
name         → Chart name
description  → Short explanation about the chart
type         → Chart type
version      → Chart version
appVersion   → Application version
```

Important difference:

```text
version     → Version of the Helm chart
appVersion  → Version of the application
```

Example:

```text
Chart version: 0.1.0
App version: 1.25.0
```

## 2. values.yaml

`values.yaml` contains the default configuration for the chart.

Example:

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
```

These values are used inside the template files.

Example:

```yaml
replicas: {{ .Values.replicaCount }}
```

This line gets the value from:

```yaml
replicaCount: 2
```

So the final Kubernetes YAML becomes:

```yaml
replicas: 2
```

## 3. templates/ Directory

The `templates/` directory contains Kubernetes YAML files.

But these files are not normal YAML only.

They are **Helm templates**.

Example:

```text
templates/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
└── secret.yaml
```

Helm reads these templates and combines them with `values.yaml`.

```text
templates/ + values.yaml = final Kubernetes YAML
```

## 4. deployment.yaml

The Deployment template creates the application Pods.

Example:

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
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}

          ports:
            - containerPort: 80
```

Important template values:

```text
{{ .Release.Name }}              → Release name from helm install
{{ .Chart.Name }}                → Chart name from Chart.yaml
{{ .Values.replicaCount }}       → Value from values.yaml
{{ .Values.image.repository }}   → Image name from values.yaml
{{ .Values.image.tag }}          → Image tag from values.yaml
```

## 5. service.yaml

The Service template exposes the application inside the cluster.

Example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-service

spec:
  type: {{ .Values.service.type }}

  selector:
    app: {{ .Release.Name }}

  ports:
    - port: {{ .Values.service.port }}
      targetPort: 80
```

If `values.yaml` contains:

```yaml
service:
  type: ClusterIP
  port: 80
```

Then Helm generates:

```yaml
type: ClusterIP
port: 80
```

## 6. _helpers.tpl

`_helpers.tpl` stores reusable template code.

It helps avoid repeating names and labels many times.

Example:

```yaml
{{- define "my-chart.name" -}}
{{ .Chart.Name }}
{{- end }}
```

You can use it in other templates like this:

```yaml
name: {{ include "my-chart.name" . }}
```

For beginners, you do not need to master `_helpers.tpl` immediately.

Just understand that it is used to make templates cleaner and reusable.

## 7. charts/ Directory

The `charts/` directory stores chart dependencies.

Example:

```text
my-chart/
└── charts/
    └── redis/
```

If your application needs Redis, PostgreSQL, or another service, Helm can install it as a dependency.

For beginners, this folder is usually empty.

## 8. NOTES.txt

`NOTES.txt` displays a message after installing the chart.

Example:

```text
Thank you for installing this chart.

To access your application, run:
kubectl get svc
```

After running:

```bash
helm install web-app ./my-chart
```

Helm prints the content of `NOTES.txt`.

## How Helm Builds the Final YAML

Helm takes:

```text
Chart.yaml
values.yaml
templates/
```

Then it renders the final Kubernetes YAML.

```text
values.yaml
     │
     ▼
templates/
     │
     ▼
Final Kubernetes YAML
     │
     ▼
Kubernetes Cluster
```

## Render Templates Without Installing

Use this command to see the final YAML before applying it:

```bash
helm template web-app ./my-chart
```

This is very useful for debugging.

## Check Chart Problems

Run:

```bash
helm lint ./my-chart
```

This checks if the chart has common mistakes.

## Install the Chart

```bash
helm install web-app ./my-chart
```

Check the release:

```bash
helm list
```

Check Kubernetes resources:

```bash
kubectl get all
```

## Upgrade the Chart

After editing `values.yaml` or templates:

```bash
helm upgrade web-app ./my-chart
```

## Uninstall the Chart

```bash
helm uninstall web-app
```

## Simple Custom Chart Structure

For learning, you can start with a smaller structure:

```text
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    └── service.yaml
```

This is enough to deploy a simple application.

## Example values.yaml

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 80
```

## Example Final Workflow

```bash
helm create my-chart
helm lint ./my-chart
helm template web-app ./my-chart
helm install web-app ./my-chart
kubectl get all
helm upgrade web-app ./my-chart
helm uninstall web-app
```

## Summary

```text
Chart.yaml   → Information about the chart
values.yaml  → Default configuration values
templates/   → Kubernetes YAML templates
_helpers.tpl → Reusable template functions
charts/      → Chart dependencies
NOTES.txt    → Message shown after install
```

> A Helm chart is a structured folder that turns reusable templates and values into Kubernetes YAML.

