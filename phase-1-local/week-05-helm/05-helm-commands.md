# Helm Cheat Sheet

## Core Concepts

| Term | Meaning |
|---|---|
| **Chart** | A Helm package — a bundle of YAML templates that describe an app |
| **Release** | An installed *instance* of a chart in your cluster. You can install the same chart multiple times under different release names |
| **Repository (repo)** | A place where charts are stored (like a website hosting packages) |
| **Values** | Configuration settings you pass in to customize a chart (env vars, replica count, image tag, etc.) |

---

## Repositories

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami   # add a repo (nickname + URL)
helm repo update                                            # refresh chart lists from all added repos
helm repo list                                               # show all repos you've added
helm repo remove bitnami                                     # remove a repo
```

## Searching for Charts

```bash
helm search hub wordpress     # search Artifact Hub (all public charts, across the internet)
helm search repo wordpress    # search only within the repos you've added locally
```

## Installing a Chart

```bash
helm install my-release bitnami/wordpress
```
Syntax is always: `helm install <release-name> <repo>/<chart-name>`

## Listing & Removing Releases

```bash
helm list                        # releases in current namespace
helm list --all-namespaces       # releases across every namespace
helm list --uninstalled          # include uninstalled releases
helm list --superseded           # include old/superseded revisions

helm uninstall my-release        # remove a release
```

---

## Customizing Installs with Values

You can override values three ways:

```bash
# 1. Inline, one value at a time (--set flag)
helm install my-release bitnami/wordpress --set wordpressBlogName="Helm Tutorial"
helm install my-release bitnami/wordpress --set wordpressEmail="you@example.com"

# 2. From a custom values file
helm install my-release bitnami/wordpress --values custom-values.yaml
```
> ⚠️ Tip: `--set` and `--values` go **after** the release name and chart, e.g.
> `helm install <release> <chart> --set key=value` — keeping flags after the two required args avoids confusion.

## Previewing Before You Install

```bash
helm template bitnami/wordpress                          # render the final YAML, no install
helm install my-release bitnami/wordpress --dry-run --debug   # simulate a real install, nothing is created
helm install my-release ./nginx-chart --dry-run=client   # client-side-only simulation (no cluster contact)
```

## Upgrading & Rolling Back

```bash
helm upgrade my-release bitnami/wordpress -f myvalues.yaml   # apply new settings to an existing release
                                                                # (note: it's "upgrade", not "update")

helm history nginx-release        # see all past revisions of a release
helm rollback nginx-release 1     # revert back to revision 1 — great when an upgrade breaks something
```

---

## Editing a Chart's Default values.yaml

If you want to inspect/edit the values a public chart ships with:

```bash
helm pull --untar bitnami/wordpress   # step 1: download + unpack the chart locally
# step 2: edit the values.yaml inside the unpacked folder, then install from that local path
helm install amaze-surf bitnami/apache
```

---

## Building & Testing Your Own Local Chart

```bash
helm create mychart                    # scaffold a new chart folder structure

helm lint ./nginx-chart/               # check the chart for syntax/config errors
helm template ./nginx-chart --debug    # render the templates locally to inspect the output

helm install hello-world-1 ./nginx-chart --set replicaCount=2 --set image=nginx
helm install hello-world-1 ./nginx-chart --dry-run=client
```

---

## Worked Example: Finding the Image Tag a Chart Will Deploy

> **Scenario:** You have a chart at `/root/webapp`. What tag will the deployed container image use?

**Step 1 — check `values.yaml`:**
```bash
cat values.yaml
```
Look for:
```yaml
image:
  tag: ""
```
If `tag` is empty, Helm falls back to `Chart.yaml`.

**Step 2 — check `Chart.yaml`:**
```bash
cat Chart.yaml
```
Look for:
```yaml
appVersion: "1.16.0"
```
👉 When `image.tag` is blank, most charts default to using `appVersion` from `Chart.yaml` as the image tag.

---

## Full Beginner Workflow (installing from a public repo)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx
helm install my-nginx bitnami/nginx
helm list
kubectl get all              # confirm the actual Kubernetes resources were created
helm status my-nginx
helm uninstall my-nginx
```

## Full Beginner Workflow (building your own chart)

```bash
helm create mychart                                  # scaffold new chart
# edit mychart/values.yaml and templates/ as needed
helm template test ./mychart                         # preview generated YAML
helm lint ./mychart                                  # check for errors

helm install myapp ./mychart --dry-run --debug       # dry run — shows what WOULD be created, installs nothing
helm install myapp ./mychart -f custom-values.yaml   # install for real — actually deploys

helm list                                             # confirm it's running
helm upgrade myapp ./mychart --set replicaCount=3     # change something later
helm uninstall myapp                                  # tear it down
```

> ✅ **Golden rule:** always `helm lint` + `--dry-run --debug` **before** installing anything in production. Catch mistakes on paper before they touch a real cluster.
