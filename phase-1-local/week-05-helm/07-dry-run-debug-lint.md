# Helm Dry Run, Debug, and Lint

Before installing or upgrading a Helm chart, you should test it first.

The three most useful commands are:

```text
helm lint      → Check chart mistakes
helm template  → Render YAML without installing
helm --dry-run → Simulate install or upgrade
helm --debug   → Show more details
```

## Why Do We Need These Commands?

Helm charts use templates.

That means small mistakes can break the final Kubernetes YAML.

Examples of common mistakes:

```text
Wrong indentation
Missing values
Wrong template syntax
Invalid Kubernetes YAML
Wrong image value
Wrong service port
```

So before running:

```bash
helm install web-app ./my-chart
```

it is safer to test the chart first.

## 1. helm lint

`helm lint` checks the chart for common problems.

```bash
helm lint ./my-chart
```

Example output if everything is okay:

```text
==> Linting ./my-chart
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

This means the chart passed the basic checks.

Example output with an error:

```text
[ERROR] templates/deployment.yaml: unable to parse YAML
```

This usually means there is a YAML or template problem.

## When to Use helm lint

Use it before:

```text
Installing a chart
Upgrading a chart
Pushing changes to GitHub
Running CI/CD pipeline
```

Basic workflow:

```bash
helm lint ./my-chart
```

## 2. helm template

`helm template` shows the final Kubernetes YAML that Helm will generate.

It does not install anything.

```bash
helm template web-app ./my-chart
```

Example:

```text
templates + values.yaml → final Kubernetes YAML
```

This is useful because you can see what Kubernetes will receive.

## Example

If `values.yaml` contains:

```yaml
replicaCount: 2
```

And the template contains:

```yaml
replicas: {{ .Values.replicaCount }}
```

Then:

```bash
helm template web-app ./my-chart
```

will show:

```yaml
replicas: 2
```

## Render with Custom Values

```bash
helm template web-app ./my-chart -f values-dev.yaml
```

Override one value:

```bash
helm template web-app ./my-chart --set replicaCount=3
```

This helps you check the final YAML before applying it.

## 3. helm install --dry-run

`--dry-run` simulates the install.

It checks what Helm would do, but it does not create resources in Kubernetes.

```bash
helm install web-app ./my-chart --dry-run
```

Use it with debug:

```bash
helm install web-app ./my-chart --dry-run --debug
```

This shows:

```text
Chart path
Release name
Computed values
Generated manifests
Template errors
```

## 4. helm upgrade --dry-run

Before upgrading an existing release, test the upgrade:

```bash
helm upgrade web-app ./my-chart --dry-run
```

With debug:

```bash
helm upgrade web-app ./my-chart --dry-run --debug
```

Use this when you changed:

```text
values.yaml
Deployment template
Service template
Ingress template
ConfigMap
Secret
image tag
replica count
```

## 5. --debug

`--debug` gives more detailed output.

Example:

```bash
helm install web-app ./my-chart --debug
```

More useful with dry run:

```bash
helm install web-app ./my-chart --dry-run --debug
```

For upgrade:

```bash
helm upgrade web-app ./my-chart --dry-run --debug
```

## Best Testing Order

Use this order before installing:

```bash
helm lint ./my-chart
helm template web-app ./my-chart
helm install web-app ./my-chart --dry-run --debug
helm install web-app ./my-chart
```

For upgrade:

```bash
helm lint ./my-chart
helm template web-app ./my-chart
helm upgrade web-app ./my-chart --dry-run --debug
helm upgrade web-app ./my-chart
```

## Example Full Workflow

```bash
helm lint ./nginx-chart

helm template hello-world ./nginx-chart

helm install hello-world ./nginx-chart --dry-run --debug

helm install hello-world ./nginx-chart

helm list

kubectl get all
```

## Debug a Template Error

Example error:

```text
Error: parse error at (my-chart/templates/deployment.yaml:15)
```

This means the problem is probably inside:

```text
templates/deployment.yaml
```

Go to the line mentioned in the error and check:

```text
Template brackets
YAML indentation
Missing values
Wrong function usage
```

Common bad syntax:

```yaml
replicas: {{ .Values.replicaCount }
```

Correct:

```yaml
replicas: {{ .Values.replicaCount }}
```

## Debug a Missing Value

Example template:

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

If `values.yaml` is missing `image.tag`, the output may be wrong.

Check values:

```bash
helm template web-app ./my-chart
```

Better template:

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default "latest" }}"
```

Now if `image.tag` is missing, Helm uses:

```text
latest
```

## Debug YAML Indentation

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

YAML depends on spacing, so `nindent` is very important in Helm.

## Check Installed Release

After install, check Helm:

```bash
helm list
helm status web-app
helm history web-app
```

Check Kubernetes:

```bash
kubectl get all
kubectl get pods
kubectl describe pod POD_NAME
kubectl logs POD_NAME
```

## Useful Commands

Lint chart:

```bash
helm lint ./my-chart
```

Render YAML:

```bash
helm template web-app ./my-chart
```

Dry run install:

```bash
helm install web-app ./my-chart --dry-run
```

Dry run install with debug:

```bash
helm install web-app ./my-chart --dry-run --debug
```

Dry run upgrade:

```bash
helm upgrade web-app ./my-chart --dry-run
```

Dry run upgrade with debug:

```bash
helm upgrade web-app ./my-chart --dry-run --debug
```

Install for real:

```bash
helm install web-app ./my-chart
```

Upgrade for real:

```bash
helm upgrade web-app ./my-chart
```

## Summary

```text
helm lint                 → Checks chart quality and common errors
helm template             → Shows final Kubernetes YAML
helm install --dry-run    → Tests install without creating resources
helm upgrade --dry-run    → Tests upgrade without changing resources
--debug                   → Shows detailed Helm output
```

> Always test your Helm chart before installing or upgrading it. Lint checks the chart, template shows the YAML, and dry run simulates the action safely.

