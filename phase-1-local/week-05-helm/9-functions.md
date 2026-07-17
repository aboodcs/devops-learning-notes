# Helm Functions

**Helm functions** are used inside Helm templates to make Kubernetes YAML dynamic.

They help you:

```text
Change text
Add default values
Format YAML
Reuse names
Control conditions
Loop over lists
```

Helm templates use this style:

```yaml
{{ functionName value }}
```

Example:

```yaml
name: {{ .Release.Name }}
```

Helm replaces it with the release name.

## Where Do We Use Helm Functions?

Helm functions are used inside files in the `templates/` folder:

```text
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── _helpers.tpl
```

Example:

```yaml
metadata:
  name: {{ .Release.Name }}-app
```

If the release name is `web`, Helm will create:

```yaml
metadata:
  name: web-app
```

## 1. `default`

The `default` function gives a backup value if no value is provided.

Example:

```yaml
replicas: {{ .Values.replicaCount | default 1 }}
```

If `values.yaml` has:

```yaml
replicaCount: 3
```

The result will be:

```yaml
replicas: 3
```

If `replicaCount` is missing, the result will be:

```yaml
replicas: 1
```

## 2. `quote`

The `quote` function wraps a value in double quotes.

Example:

```yaml
appVersion: {{ .Values.appVersion | quote }}
```

If `values.yaml` has:

```yaml
appVersion: 1.0
```

The result becomes:

```yaml
appVersion: "1.0"
```

This is useful when you want to make sure the value is treated as text.

## 3. `upper` and `lower`

These functions change text case.

```yaml
name: {{ .Values.appName | upper }}
```

If:

```yaml
appName: nginx
```

Result:

```yaml
name: NGINX
```

Another example:

```yaml
name: {{ .Values.appName | lower }}
```

Result:

```yaml
name: nginx
```

## 4. `trunc`

The `trunc` function cuts long text.

Kubernetes names have length limits, so this is useful.

```yaml
name: {{ .Release.Name | trunc 20 }}
```

If the release name is too long, Helm keeps only the first 20 characters.

## 5. `include`

The `include` function is used to reuse templates from `_helpers.tpl`.

Example `_helpers.tpl`:

```yaml
{{- define "my-chart.name" -}}
{{ .Chart.Name }}
{{- end }}
```

Use it inside another template:

```yaml
name: {{ include "my-chart.name" . }}
```

This helps avoid repeating the same naming logic in many files.

## 6. `indent` and `nindent`

These functions fix YAML spacing.

YAML depends on correct indentation.

### `indent`

```yaml
labels:
{{ include "my-chart.labels" . | indent 2 }}
```

### `nindent`

```yaml
labels:
{{ include "my-chart.labels" . | nindent 2 }}
```

`nindent` means:

```text
new line + indent
```

It is very common in Helm templates.

## 7. `toYaml`

The `toYaml` function converts values from `values.yaml` into YAML format.

Example `values.yaml`:

```yaml
resources:
  limits:
    cpu: 500m
    memory: 256Mi
```

Template:

```yaml
resources:
{{ .Values.resources | toYaml | nindent 10 }}
```

Result:

```yaml
resources:
  limits:
    cpu: 500m
    memory: 256Mi
```

This is very useful for complex values.

## 8. `if`

The `if` statement adds something only when a condition is true.

Example:

```yaml
{{- if .Values.service.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-service
{{- end }}
```

If `values.yaml` has:

```yaml
service:
  enabled: true
```

Helm creates the Service.

If it is:

```yaml
service:
  enabled: false
```

Helm does not create it.

## 9. `eq`

The `eq` function checks if two values are equal.

Example:

```yaml
{{- if eq .Values.environment "production" }}
replicas: 3
{{- else }}
replicas: 1
{{- end }}
```

If:

```yaml
environment: production
```

Result:

```yaml
replicas: 3
```

If:

```yaml
environment: development
```

Result:

```yaml
replicas: 1
```

## 10. `range`

The `range` function loops over a list.

Example `values.yaml`:

```yaml
ports:
  - 80
  - 443
```

Template:

```yaml
ports:
{{- range .Values.ports }}
  - containerPort: {{ . }}
{{- end }}
```

Result:

```yaml
ports:
  - containerPort: 80
  - containerPort: 443
```

## 11. `required`

The `required` function forces the user to provide a value.

Example:

```yaml
image: {{ required "image.repository is required" .Values.image.repository }}
```

If `image.repository` is missing, Helm stops and shows an error.

This is useful for important values that must exist.

## 12. `with`

The `with` function makes templates cleaner when working with nested values.

Example `values.yaml`:

```yaml
image:
  repository: nginx
  tag: alpine
```

Template:

```yaml
{{- with .Values.image }}
image: "{{ .repository }}:{{ .tag }}"
{{- end }}
```

Result:

```yaml
image: "nginx:alpine"
```

Inside `with`, the dot `.` changes to the selected object.

## Function Pipeline

Helm commonly uses pipelines.

A pipeline sends the value from left to right.

Example:

```yaml
name: {{ .Values.appName | default "nginx" | quote }}
```

This means:

```text
Take appName
If missing, use nginx
Then add quotes
```

Result:

```yaml
name: "nginx"
```

## Common Helm Function Examples

### Safe App Name

```yaml
name: {{ .Release.Name | trunc 63 | quote }}
```

### Default Replica Count

```yaml
replicas: {{ .Values.replicaCount | default 1 }}
```

### Image Name

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

### Labels

```yaml
labels:
  app: {{ .Chart.Name }}
  release: {{ .Release.Name }}
```

### Resources

```yaml
resources:
{{ .Values.resources | toYaml | nindent 10 }}
```

## Useful Template Values

Helm gives you built-in objects:

```text
.Release.Name       → Release name
.Release.Namespace  → Namespace of the release
.Chart.Name         → Chart name
.Chart.Version      → Chart version
.Values             → Values from values.yaml
```

Example:

```yaml
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
```

## Test Helm Functions

Render the template without installing:

```bash
helm template web-app ./my-chart
```

Check for template errors:

```bash
helm lint ./my-chart
```

Install the chart:

```bash
helm install web-app ./my-chart
```

Upgrade after changes:

```bash
helm upgrade web-app ./my-chart
```

## Simple Example

`values.yaml`:

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine

service:
  enabled: true
  port: 80
```

`templates/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment

spec:
  replicas: {{ .Values.replicaCount | default 1 }}

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
            - containerPort: {{ .Values.service.port }}
```

Render it:

```bash
helm template web-app ./my-chart
```

## Summary

```text
default   → Use a backup value
quote     → Add quotes
upper     → Convert text to uppercase
lower     → Convert text to lowercase
trunc     → Cut long text
include   → Reuse templates
nindent   → Fix YAML indentation
toYaml    → Convert values into YAML
if        → Add logic
eq        → Compare values
range     → Loop over lists
required  → Force a value to exist
with      → Work with nested values
```

> Helm functions make templates dynamic, reusable, and easier to control.

