# Helm Templates

A **Helm template** is a Kubernetes YAML file that contains dynamic values.

Normal Kubernetes YAML is static.

Helm templates are dynamic because they can read values from:

```text id="l9k7do"
values.yaml
Chart.yaml
Release information
Helm built-in objects
```

## Why Do We Need Templates?

Without templates, you may write different YAML files for every environment:

```text id="s1p45b"
deployment-dev.yaml
deployment-test.yaml
deployment-prod.yaml
```

With Helm templates, you write one reusable file and change only the values.

```text id="myeq17"
template + values.yaml = final Kubernetes YAML
```

## Template Location

Templates are stored inside the `templates/` directory:

```text id="cf590g"
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    └── secret.yaml
```

## Basic Template Example

Normal Kubernetes YAML:

```yaml id="bqlqqp"
replicas: 2
```

Helm template:

```yaml id="9esgux"
replicas: {{ .Values.replicaCount }}
```

If `values.yaml` contains:

```yaml id="olbgv7"
replicaCount: 2
```

Helm generates:

```yaml id="tvwf5j"
replicas: 2
```

## Common Helm Template Objects

```text id="2x9ggu"
.Values        → Reads values from values.yaml
.Release.Name  → Gets the release name
.Chart.Name    → Gets the chart name
.Chart.Version → Gets the chart version
```

Example:

```yaml id="v4xa05"
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
```

If:

```text id="5b9mgh"
Release name: web
Chart name: nginx-chart
```

The result becomes:

```yaml id="wo7vss"
metadata:
  name: web-nginx-chart
```

## Example values.yaml

```yaml id="lmgeue"
replicaCount: 2

image:
  repository: nginx
  tag: alpine

service:
  type: NodePort
  port: 80
```

## Deployment Template

Create:

```text id="w2xw15"
templates/deployment.yaml
```

Add:

```yaml id="yq95dx"
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

          ports:
            - containerPort: 80
```

## Service Template

Create:

```text id="jqaaqo"
templates/service.yaml
```

Add:

```yaml id="1vf0s1"
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

## Render Templates

Before installing the chart, check the final YAML:

```bash id="tm1w6v"
helm template web-app ./my-chart
```

This command does not install anything.

It only shows what Kubernetes YAML Helm will generate.

## Install the Chart

```bash id="o976vm"
helm install web-app ./my-chart
```

Check resources:

```bash id="pkk5ub"
kubectl get all
```

## Template with Default Value

Use `default` when you want a backup value:

```yaml id="ith2gw"
replicas: {{ .Values.replicaCount | default 1 }}
```

If `replicaCount` is missing, Helm uses:

```yaml id="qp4pbj"
replicas: 1
```

## Template with Quote

Use `quote` to make a value a string:

```yaml id="u8rj0n"
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

Another example:

```yaml id="dxwoyj"
appVersion: {{ .Chart.AppVersion | quote }}
```

## Template with If Condition

Use `if` to create something only when it is enabled.

Example `values.yaml`:

```yaml id="0hogei"
service:
  enabled: true
```

Template:

```yaml id="vpqnxs"
{{- if .Values.service.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-service
{{- end }}
```

If `enabled` is `true`, Helm creates the Service.

If `enabled` is `false`, Helm skips it.

## Template with Range Loop

Use `range` to loop over a list.

Example `values.yaml`:

```yaml id="lg49ig"
ports:
  - 80
  - 443
```

Template:

```yaml id="0vriym"
ports:
{{- range .Values.ports }}
  - containerPort: {{ . }}
{{- end }}
```

Result:

```yaml id="qcu7wz"
ports:
  - containerPort: 80
  - containerPort: 443
```

## Template with toYaml and nindent

`toYaml` converts values into YAML.

`nindent` fixes spacing.

Example `values.yaml`:

```yaml id="im5vg7"
resources:
  limits:
    cpu: 500m
    memory: 256Mi
```

Template:

```yaml id="5ispgo"
resources:
{{ .Values.resources | toYaml | nindent 10 }}
```

This is useful for complex YAML blocks.

## Common Mistake

Bad YAML indentation can break the chart.

Bad:

```yaml id="hfp0rv"
labels:
  {{ include "my-chart.labels" . }}
```

Better:

```yaml id="thogw4"
labels:
{{ include "my-chart.labels" . | nindent 2 }}
```

Helm templates must generate valid Kubernetes YAML.

## Useful Commands

Render templates:

```bash id="rs9bnj"
helm template web-app ./my-chart
```

Check chart errors:

```bash id="t6rhn1"
helm lint ./my-chart
```

Install chart:

```bash id="7funer"
helm install web-app ./my-chart
```

Upgrade after editing templates:

```bash id="bxjnh7"
helm upgrade web-app ./my-chart
```

View generated YAML from an installed release:

```bash id="w6g2yv"
helm get manifest web-app
```

## Summary

```text id="f9uzz4"
Template      → Dynamic Kubernetes YAML file
.Values       → Reads from values.yaml
.Release.Name → Uses the Helm release name
if            → Adds logic
range         → Loops over values
default       → Adds fallback values
toYaml        → Converts values to YAML
nindent       → Fixes YAML spacing
```

> Helm templates turn reusable YAML files into final Kubernetes resources using values and functions.

