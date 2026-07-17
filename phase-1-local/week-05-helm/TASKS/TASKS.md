# Helm Practical Tasks

## General Rules

* Every task must be solved in a new empty directory.
* Every task must include a Helm chart.
* Every task must run successfully on Minikube.
* Do not reuse old Helm releases, namespaces, images, charts, PVCs, or Kubernetes resources.
* Do not use the `default` Namespace.
* Do not hardcode configuration directly inside templates.
* Use `values.yaml` for configurable values.
* Use `templates/` for Kubernetes manifests.
* Use `helm lint` before installing.
* Use `helm template` or `helm install --dry-run --debug` before real installation.
* Every task must include a `README.md`.
* Every task must include screenshots for proof.
* Every task must document the Helm commands used.
* Do not use the `latest` image tag.

Each task must test at least some of the following:

```text
Helm chart structure
Chart.yaml
values.yaml
templates/
_helpers.tpl
Named templates
Helm functions
helm install
helm upgrade
helm uninstall
helm lint
helm template
helm dry-run
helm history
helm rollback
Helm values override
Ingress
HPA
PVC
ConfigMap
Secret
```

---

# Easy Level

---

## Easy Helm Task 1: Package a Simple Flask App with Helm

### Scenario

Create a simple Flask application and deploy it to Minikube using a custom Helm chart.

The goal is to understand the basic Helm chart structure and how Helm templates generate Kubernetes YAML files.

### Required Endpoints

```text
GET /
GET /health
GET /config
```

### Your Tasks

1. Create a simple Flask application.

2. Write a Dockerfile for the application.

3. Build the Docker image using a fixed tag:

```text
flask-helm:v1
```

4. Load the image into Minikube.

5. Create a Helm chart called:

```text
flask-chart
```

6. The chart must create:

```text
Namespace
Deployment
Service
ConfigMap
```

7. Use `values.yaml` for:

```text
image.repository
image.tag
replicaCount
service.type
service.port
appName
appEnv
```

8. The application must read `APP_NAME` and `APP_ENV` from a ConfigMap.

9. The Service must be `NodePort`.

10. Install the chart with:

```bash
helm install flask-release ./flask-chart
```

11. Access the app using:

```bash
minikube service
```

12. Change `replicaCount` from 1 to 2 using `values.yaml`.

13. Upgrade the release.

14. Confirm that 2 Pods are running.

15. Uninstall the release.

### Required Deliverables

```text
easy-helm-01-flask-basic-chart/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── flask-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── README.md
└── screenshots/
    ├── helm-lint.png
    ├── helm-install.png
    ├── kubectl-get-pods.png
    ├── app-working.png
    └── helm-uninstall.png
```

### Validation

The examiner must be able to run:

```bash
helm lint ./flask-chart
helm install flask-release ./flask-chart
kubectl get all -n <namespace>
```

The application must be reachable through Minikube.

---

## Easy Helm Task 2: Helm Values Override

### Scenario

Create a Helm chart for a simple web application and prove that the same chart can deploy different environments by changing values.

You must deploy the same chart twice: one release for development and one release for production.

### Required Environments

```text
development
production
```

### Your Tasks

1. Create a simple web app using Python or Node.js.

2. Create a Dockerfile.

3. Build and load the image into Minikube.

4. Create one Helm chart called:

```text
environment-chart
```

5. Create two values files:

```text
values-dev.yaml
values-prod.yaml
```

6. The dev release must use:

```text
APP_ENV=development
replicaCount=1
```

7. The prod release must use:

```text
APP_ENV=production
replicaCount=3
```

8. Install the dev release in a Namespace called:

```text
dev-env
```

9. Install the prod release in a Namespace called:

```text
prod-env
```

10. Confirm that both releases use the same chart.

11. Confirm that dev has 1 replica.

12. Confirm that prod has 3 replicas.

13. Confirm that each app shows the correct environment.

14. Uninstall both releases.

### Required Deliverables

```text
easy-helm-02-values-override/
├── app/
│   ├── source files
│   └── Dockerfile
├── environment-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── README.md
└── screenshots/
    ├── dev-release.png
    ├── prod-release.png
    ├── dev-pods.png
    └── prod-pods.png
```

### Validation

The examiner must be able to install two different releases from the same chart using different values files.

---

## Easy Helm Task 3: Helm Dry Run, Debug, and Template Output

### Scenario

Create a Helm chart and test it before installation using Helm debugging commands.

The focus of this task is not only deploying the app, but proving that you know how to inspect what Helm will create before applying it to the cluster.

### Your Tasks

1. Create a simple web application.

2. Create a Dockerfile and image.

3. Create a Helm chart called:

```text
debug-chart
```

4. The chart must include:

```text
Deployment
Service
ConfigMap
Secret
```

5. Store normal config in ConfigMap.

6. Store sensitive config in Secret.

7. Use `values.yaml` for all configurable values.

8. Run:

```bash
helm lint ./debug-chart
```

9. Run:

```bash
helm template debug-release ./debug-chart
```

10. Save the rendered output into a file:

```text
rendered-output.yaml
```

11. Run:

```bash
helm install debug-release ./debug-chart --dry-run --debug
```

12. Fix any template errors.

13. Install the release for real.

14. Confirm the app works.

15. Uninstall the release.

### Required Deliverables

```text
easy-helm-03-dry-run-debug/
├── app/
│   ├── source files
│   └── Dockerfile
├── debug-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── configmap.yaml
│       ├── secret.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── rendered-output.yaml
├── README.md
└── screenshots/
    ├── helm-lint.png
    ├── helm-template.png
    ├── helm-dry-run-debug.png
    └── app-working.png
```

### Validation

The examiner must see proof that the chart was checked with lint, template rendering, and dry-run before installation.

---

# Hard Level

---

## Hard Helm Task 1: Helm Chart with Named Templates and Helper Functions

### Scenario

Create a Helm chart that uses `_helpers.tpl` to avoid repeated names and labels.

The goal is to write cleaner Helm templates using named templates and Helm functions.

### Required Application

```text
Web API with config and health endpoints
```

### Required Endpoints

```text
GET /
GET /health
GET /config
```

### Your Tasks

1. Create a small API using Python or Node.js.

2. Create a Dockerfile.

3. Build and load the image into Minikube.

4. Create a Helm chart called:

```text
helper-chart
```

5. Create a `_helpers.tpl` file.

6. Add named templates for:

```text
chart name
full name
common labels
selector labels
service account name
```

7. Use helper templates inside:

```text
Deployment
Service
ConfigMap
```

8. Use Helm functions such as:

```text
include
default
quote
toYaml
nindent
trunc
trimSuffix
```

9. Use `values.yaml` for:

```text
replicaCount
image
service
resources
env
```

10. Install the chart.

11. Confirm labels are correctly generated.

12. Upgrade values and confirm the rendered labels remain consistent.

13. Uninstall the chart.

### Required Deliverables

```text
hard-helm-01-named-templates/
├── app/
│   ├── source files
│   └── Dockerfile
├── helper-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── README.md
└── screenshots/
    ├── helm-template-labels.png
    ├── helm-install.png
    ├── kubectl-labels.png
    └── helm-upgrade.png
```

### Validation

The chart must use `_helpers.tpl`, and labels must be generated through named templates instead of being repeated manually in every file.

---

## Hard Helm Task 2: Helm Ingress and HPA Chart

### Scenario

Create a Helm chart that deploys an application with Ingress and Horizontal Pod Autoscaler.

The application must be accessible through a custom hostname and must scale when CPU usage increases.

### Required Endpoints

```text
GET /
GET /health
GET /cpu
```

### Your Tasks

1. Create a CPU-test web application.

2. Create a Dockerfile.

3. Build and load the image into Minikube.

4. Enable Minikube addons:

```bash
minikube addons enable ingress
minikube addons enable metrics-server
```

5. Create a Helm chart called:

```text
ingress-hpa-chart
```

6. The chart must template:

```text
Deployment
Service
Ingress
HPA
ConfigMap
```

7. Use `values.yaml` to enable or disable Ingress.

8. Use `values.yaml` to enable or disable HPA.

9. Create an Ingress host:

```text
helm-app.local.test
```

10. Add the host to `/etc/hosts`.

11. Configure HPA values:

```text
minReplicas
maxReplicas
targetCPUUtilizationPercentage
```

12. Install the chart.

13. Generate CPU load using `/cpu`.

14. Watch HPA scale the app.

15. Disable HPA using values and upgrade the release.

16. Confirm HPA is removed or disabled.

17. Uninstall the release.

### Required Deliverables

```text
hard-helm-02-ingress-hpa/
├── app/
│   ├── source files
│   └── Dockerfile
├── ingress-hpa-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── hpa.yaml
├── README.md
└── screenshots/
    ├── ingress-working.png
    ├── hpa-before.png
    ├── hpa-after.png
    ├── helm-upgrade-disable-hpa.png
    └── helm-uninstall.png
```

### Validation

The app must work through Ingress, and HPA must be controlled by Helm values.

---

## Hard Helm Task 3: Helm Chart with Persistent Storage

### Scenario

Create a Helm chart for a file upload application that stores uploaded files using a PersistentVolumeClaim.

The chart must allow storage size and mount path to be configured from `values.yaml`.

### Required Endpoints

```text
GET /
POST /
GET /health
```

### Your Tasks

1. Create a file upload app using Python or Node.js.

2. Create a Dockerfile.

3. Store uploaded files inside:

```text
/app/uploads
```

4. Create a Helm chart called:

```text
upload-chart
```

5. The chart must include:

```text
Deployment
Service
ConfigMap
PersistentVolumeClaim
```

6. The PVC size must come from `values.yaml`.

7. The upload directory must come from `values.yaml`.

8. Mount the PVC inside the container at the upload directory.

9. Install the chart.

10. Upload at least two files.

11. Delete the Pod manually.

12. Confirm that uploaded files still exist after the Pod is recreated.

13. Upgrade the chart and change the app version.

14. Confirm that the uploaded files still exist after upgrade.

15. Uninstall the release.

16. Document whether the PVC is deleted or kept after uninstall.

### Required Deliverables

```text
hard-helm-03-pvc-upload-chart/
├── app/
│   ├── source files
│   └── Dockerfile
├── upload-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── pvc.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── README.md
└── screenshots/
    ├── helm-install.png
    ├── files-uploaded.png
    ├── pvc-created.png
    ├── pod-deleted-files-still-exist.png
    └── helm-upgrade-persistence.png
```

### Validation

Uploaded files must survive Pod recreation and Helm upgrade.

---

# Impossible Level

---

## Impossible Helm Task 1: Helm Chart with PostgreSQL Dependency

### Scenario

Create an application that stores data in PostgreSQL and package it with Helm.

The PostgreSQL database must be installed as a Helm dependency or subchart, while your application is installed from your own chart.

### Required Endpoints

```text
GET /
GET /health
POST /items
GET /items
```

### Your Tasks

1. Create an API using Python or Node.js.

2. Create a Dockerfile.

3. Build and load the image into Minikube.

4. Create a Helm chart called:

```text
api-postgres-chart
```

5. Add PostgreSQL as a chart dependency.

6. Configure PostgreSQL values through the parent chart.

7. Store database credentials using Kubernetes Secrets.

8. The API must connect to PostgreSQL using the database Service name.

9. Add a readiness probe so the API does not receive traffic before it can connect to the database.

10. Add a PVC for PostgreSQL data.

11. Install the chart.

12. Create at least two items.

13. Delete the API Pod.

14. Confirm the API Pod is recreated.

15. Delete the PostgreSQL Pod.

16. Confirm data still exists after PostgreSQL comes back.

17. Upgrade the chart and change the API image tag.

18. Confirm data still exists after upgrade.

19. Roll back to the previous release revision.

20. Confirm the app still works.

### Required Deliverables

```text
impossible-helm-01-postgres-dependency/
├── app/
│   ├── source files
│   └── Dockerfile
├── api-postgres-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── charts/
│   └── templates/
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── secret.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── README.md
└── screenshots/
    ├── helm-dependency-build.png
    ├── helm-install.png
    ├── items-created.png
    ├── postgres-persistence.png
    ├── helm-history.png
    └── helm-rollback.png
```

### Validation

The app and PostgreSQL must be installed with Helm, and PostgreSQL data must survive Pod recreation, chart upgrade, and rollback.

---

## Impossible Helm Task 2: Multi-Environment Helm Deployment

### Scenario

Create one Helm chart that can deploy the same application to three different environments.

Each environment must have different replica counts, resource limits, hostnames, and configuration values.

### Required Environments

```text
dev
staging
production
```

### Your Tasks

1. Create a web application.

2. Create a Dockerfile.

3. Build and load the image into Minikube.

4. Create one reusable Helm chart.

5. Create separate values files:

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

6. Dev must use:

```text
replicaCount=1
small resources
NodePort or simple Ingress
```

7. Staging must use:

```text
replicaCount=2
Ingress enabled
medium resources
```

8. Production must use:

```text
replicaCount=4
Ingress enabled
HPA enabled
larger resources
```

9. Use different hostnames:

```text
dev.helm.local.test
staging.helm.local.test
prod.helm.local.test
```

10. Install all three releases at the same time.

11. Confirm that each environment works independently.

12. Upgrade only staging.

13. Confirm dev and production are not affected.

14. Roll back staging.

15. Uninstall only dev.

16. Confirm staging and production continue running.

### Required Deliverables

```text
impossible-helm-02-multi-env/
├── app/
│   ├── source files
│   └── Dockerfile
├── multi-env-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── hpa.yaml
├── README.md
└── screenshots/
    ├── three-releases.png
    ├── dev-working.png
    ├── staging-working.png
    ├── prod-working.png
    ├── staging-rollback.png
    └── dev-uninstalled.png
```

### Validation

One Helm chart must successfully manage three separate environments without conflict.

---

## Impossible Helm Task 3: Final Helm Boss — Full App Lifecycle

### Scenario

Create a complete Helm-based application lifecycle project.

You must build an app, package it with Helm, validate the chart, install it, upgrade it, break it, recover it, roll it back, and uninstall it cleanly.

### Required Endpoints

```text
GET /
GET /health
GET /ready
GET /config
GET /secret
GET /version
GET /cpu
```

### Your Tasks

1. Create a web application.

2. Create a multi-stage Dockerfile.

3. Run the app as a non-root user.

4. Create a Helm chart called:

```text
final-helm-chart
```

5. The chart must include:

```text
Namespace
ConfigMap
Secret
Deployment
Service
Ingress
HPA
ServiceAccount
```

6. Use `_helpers.tpl` for names and labels.

7. Use values to enable or disable:

```text
Ingress
HPA
ServiceAccount
resources
probes
```

8. Add liveness and readiness probes.

9. Add CPU and memory requests and limits.

10. Install the chart.

11. Confirm the app works through Ingress.

12. Upgrade the app version.

13. Check Helm history.

14. Break the app by upgrading to a wrong image tag.

15. Confirm Pods fail.

16. Recover using Helm rollback.

17. Generate CPU load.

18. Confirm HPA scales the Deployment.

19. Run `helm template` and save the rendered manifests.

20. Run `helm package` to package the chart.

21. Uninstall the chart.

22. Confirm all resources are removed.

### Required Deliverables

```text
impossible-helm-03-final-boss/
├── app/
│   ├── source files
│   └── Dockerfile
├── final-helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── namespace.yaml
│       ├── serviceaccount.yaml
│       ├── configmap.yaml
│       ├── secret.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── hpa.yaml
├── rendered-output.yaml
├── packaged-chart.tgz
├── REPORT.md
└── screenshots/
    ├── helm-lint.png
    ├── helm-template.png
    ├── helm-install.png
    ├── ingress-working.png
    ├── helm-upgrade.png
    ├── broken-image.png
    ├── helm-rollback.png
    ├── hpa-scaling.png
    └── helm-uninstall.png
```

### REPORT.md Must Include

```text
1. How the Docker image was built
2. How the Helm chart is structured
3. What values.yaml controls
4. How templates use _helpers.tpl
5. How the chart was tested before install
6. How the chart was installed
7. How the app was upgraded
8. What was broken
9. How rollback fixed it
10. How HPA was tested
11. How the chart was packaged
12. Screenshots
13. Commands used
14. What was learned
```

### Validation

The examiner must be able to run:

```bash
helm lint ./final-helm-chart
helm install final-helm ./final-helm-chart
helm upgrade final-helm ./final-helm-chart
helm rollback final-helm <revision>
helm uninstall final-helm
```

The app must complete the full Helm lifecycle successfully.

---

## Important Notes

Do not delete the Minikube cluster before taking screenshots.

Do not uninstall a Helm release before checking:

```bash
helm history <release-name>
```

Do not use:

```text
latest
```

as an image tag.

> The goal is not only to install an application with Helm. The goal is to understand how Helm manages Kubernetes manifests, values, releases, upgrades, rollbacks, and reusable charts.

