# Helm Named Templates

A **named template** is a reusable block of Helm template code.

It is usually written inside:

```text id="yavcnf"
templates/_helpers.tpl
```

Named templates help you avoid repeating the same code many times.

## Why Do We Need Named Templates?

In Helm charts, we often repeat names and labels in many files:

```text id="n5y5c5"
deployment.yaml
service.yaml
configmap.yaml
secret.yaml
```

Without named templates, you may repeat the same labels everywhere.

With named templates, you define the logic once and reuse it.

```text id="afv8jo"
_helpers.tpl → Define reusable template
deployment.yaml → Use it
service.yaml → Use it
```

## Basic Syntax

Define a named template:

```yaml id="mf20u7"
{{- define "my-chart.name" -}}
{{ .Chart.Name }}
{{- end }}
```

Use it:

```yaml id="0ts1hk"
{{ include "my-chart.name" . }}
```

## Important Keywords

```text id="080l7m"
define  → Creates the named template
include → Uses the named template
end     → Ends the template block
.       → Passes the current Helm context
```

## Example Chart Structure

```text id="5ukg78"
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    └── service.yaml
```

## 1. Create a Name Template

Inside `templates/_helpers.tpl`:

```yaml id="u62d24"
{{- define "my-chart.name" -}}
{{ .Chart.Name }}
{{- end }}
```

This creates a reusable template called:

```text id="jz38qj"
my-chart.name
```

Use it inside `deployment.yaml`:

```yaml id="syn50j"
metadata:
  name: {{ include "my-chart.name" . }}
```

If the chart name is:

```yaml id="o4z14w"
name: nginx-chart
```

The result becomes:

```yaml id="l3a2vs"
metadata:
  name: nginx-chart
```

## 2. Create a Full Name Template

Usually, we want the resource name to include the release name.

Inside `_helpers.tpl`:

```yaml id="lhbj5v"
{{- define "my-chart.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}
```

Use it:

```yaml id="31llri"
metadata:
  name: {{ include "my-chart.fullname" . }}
```

If:

```text id="v1yx54"
Release name: web
Chart name: nginx-chart
```

The result becomes:

```yaml id="liw3bw"
metadata:
  name: web-nginx-chart
```

## 3. Create Reusable Labels

Labels are repeated in many Kubernetes resources.

Inside `_helpers.tpl`:

```yaml id="z51p29"
{{- define "my-chart.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

Use it inside `deployment.yaml`:

```yaml id="htdcm6"
metadata:
  labels:
{{ include "my-chart.labels" . | nindent 4 }}
```

The `nindent 4` means:

```text id="5r52o3"
new line + 4 spaces indentation
```

This is important because YAML depends on correct spacing.

## 4. Use Named Template in Deployment

Example `templates/deployment.yaml`:

```yaml id="5mecb9"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-chart.fullname" . }}
  labels:
{{ include "my-chart.labels" . | nindent 4 }}

spec:
  replicas: {{ .Values.replicaCount }}

  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Chart.Name }}
      app.kubernetes.io/instance: {{ .Release.Name }}

  template:
    metadata:
      labels:
{{ include "my-chart.labels" . | nindent 8 }}

    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: 80
```

## 5. Use Named Template in Service

Example `templates/service.yaml`:

```yaml id="akhb9o"
apiVersion: v1
kind: Service
metadata:
  name: {{ include "my-chart.fullname" . }}
  labels:
{{ include "my-chart.labels" . | nindent 4 }}

spec:
  type: {{ .Values.service.type }}

  selector:
    app.kubernetes.io/name: {{ .Chart.Name }}
    app.kubernetes.io/instance: {{ .Release.Name }}

  ports:
    - port: {{ .Values.service.port }}
      targetPort: 80
```

Now both Deployment and Service use the same name and labels from `_helpers.tpl`.

## Complete `_helpers.tpl` Example

```yaml id="5t4qol"
{{- define "my-chart.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "my-chart.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}

{{- define "my-chart.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## Why the Dot `.` Is Important

When using `include`, we pass the dot:

```yaml id="g1etv1"
{{ include "my-chart.labels" . }}
```

The dot gives the named template access to:

```text id="53jhea"
.Chart
.Values
.Release
.Capabilities
```

Without the dot, the named template may not know the release name, chart name, or values.

## Test the Output

Render the chart without installing it:

```bash id="gvu4sl"
helm template web-app ./my-chart
```

Check for errors:

```bash id="3hc2bm"
helm lint ./my-chart
```

Install the chart:

```bash id="gci6ik"
helm install web-app ./my-chart
```

## Common Mistake

Bad indentation:

```yaml id="e3c2vu"
labels:
  {{ include "my-chart.labels" . }}
```

Better:

```yaml id="46muo7"
labels:
{{ include "my-chart.labels" . | nindent 2 }}
```

Because the named template already returns YAML lines, `nindent` places them correctly.

## Summary

```text id="g6bbwd"
define       → Creates a named template
include      → Reuses a named template
_helpers.tpl → Stores reusable template blocks
nindent      → Fixes YAML indentation
.            → Passes the current Helm context
```

> A named template is reusable Helm code that keeps chart names, labels, and repeated YAML clean and consistent.

