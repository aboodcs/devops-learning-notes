# values.yaml

`values.yaml` is the main configuration file in a Helm chart.

It stores the default values that Helm uses inside the templates.

```text
values.yaml + templates/ = final Kubernetes YAML
```

## Why Do We Need values.yaml?

Without `values.yaml`, you would need to edit Kubernetes YAML files every time you want to change something.

Example changes:

```text
replica count
image name
image tag
service type
service port
environment variables
resources
```

With `values.yaml`, you change the configuration in one place.

## Example Chart Structure

```text
my-chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    └── service.yaml
```

## Basic values.yaml Example

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 80
```

## How Templates Use values.yaml

In `values.yaml`:

```yaml
replicaCount: 2
```

In `templates/deployment.yaml`:

```yaml
replicas: {{ .Values.replicaCount }}
```

Final Kubernetes YAML:

```yaml
replicas: 2
```

## Image Values

In `values.yaml`:

```yaml
image:
  repository: nginx
  tag: alpine
  pullPolicy: IfNotPresent
```

In the Deployment template:

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
imagePullPolicy: {{ .Values.image.pullPolicy }}
```

Final result:

```yaml
image: "nginx:alpine"
imagePullPolicy: IfNotPresent
```

## Service Values

In `values.yaml`:

```yaml
service:
  type: NodePort
  port: 80
  targetPort: 80
```

In `templates/service.yaml`:

```yaml
spec:
  type: {{ .Values.service.type }}

  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
```

Final result:

```yaml
spec:
  type: NodePort

  ports:
    - port: 80
      targetPort: 80
```

## Environment Variables

In `values.yaml`:

```yaml
env:
  APP_MODE: production
  APP_PORT: "5000"
```

In the Deployment template:

```yaml
env:
  - name: APP_MODE
    value: {{ .Values.env.APP_MODE | quote }}

  - name: APP_PORT
    value: {{ .Values.env.APP_PORT | quote }}
```

Final result:

```yaml
env:
  - name: APP_MODE
    value: "production"

  - name: APP_PORT
    value: "5000"
```

## Resource Values

In `values.yaml`:

```yaml
resources:
  requests:
    cpu: 250m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

In the Deployment template:

```yaml
resources:
{{ .Values.resources | toYaml | nindent 12 }}
```

This keeps the template clean and lets `values.yaml` control the resource limits.

## Ingress Values

In `values.yaml`:

```yaml
ingress:
  enabled: true
  host: app.local
  path: /
```

In the template:

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ingress

spec:
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: {{ .Values.ingress.path }}
            pathType: Prefix
{{- end }}
```

If `enabled` is `true`, Helm creates the Ingress.

If `enabled` is `false`, Helm skips it.

## Override Values from the Command Line

You can change values without editing `values.yaml`.

```bash
helm install web-app ./my-chart --set replicaCount=4
```

This changes:

```yaml
replicaCount: 4
```

Another example:

```bash
helm upgrade web-app ./my-chart --set image.tag=latest
```

This changes the image tag.

## Use Different Values Files

You can create separate values files for different environments:

```text
values-dev.yaml
values-prod.yaml
```

Example `values-dev.yaml`:

```yaml
replicaCount: 1

image:
  tag: dev

service:
  type: NodePort
```

Example `values-prod.yaml`:

```yaml
replicaCount: 3

image:
  tag: stable

service:
  type: LoadBalancer
```

Install with dev values:

```bash
helm install web-dev ./my-chart -f values-dev.yaml
```

Install with prod values:

```bash
helm install web-prod ./my-chart -f values-prod.yaml
```

## Values Priority

Helm uses values in this order:

```text
values.yaml              lowest priority
-f values-dev.yaml
--set key=value          highest priority
```

Example:

```bash
helm install web-app ./my-chart \
  -f values-dev.yaml \
  --set replicaCount=5
```

Here, `replicaCount=5` wins.

## Check the Final Output

Render the final Kubernetes YAML:

```bash
helm template web-app ./my-chart
```

Check chart problems:

```bash
helm lint ./my-chart
```

View values used by an installed release:

```bash
helm get values web-app
```

View all values:

```bash
helm get values web-app --all
```

## Common Mistakes

### Missing Value

Bad:

```yaml
replicas: {{ .Values.replicaCount }}
```

Better:

```yaml
replicas: {{ .Values.replicaCount | default 1 }}
```

### Forgetting Quotes

Bad:

```yaml
value: {{ .Values.env.APP_PORT }}
```

Better:

```yaml
value: {{ .Values.env.APP_PORT | quote }}
```

### Wrong Indentation

Bad:

```yaml
resources:
  {{ .Values.resources | toYaml }}
```

Better:

```yaml
resources:
{{ .Values.resources | toYaml | nindent 12 }}
```

## Summary

```text
values.yaml  → Stores chart configuration
.Values      → Reads values inside templates
-f           → Uses another values file
--set        → Overrides values from command line
default      → Provides backup value
quote        → Converts value to string
toYaml       → Converts values into YAML format
nindent      → Fixes YAML indentation
```

> `values.yaml` is the control file of a Helm chart. It lets you change the application configuration without editing the templates.

