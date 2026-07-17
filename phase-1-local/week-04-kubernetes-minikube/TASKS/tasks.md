# Kubernetes Practical Exams

## General Rules

* Each exam must be solved independently.
* Start every exam in a new empty directory.
* Do not reuse Kubernetes manifests, Docker images, Namespaces, volumes, or resources from another exam.
* Every application must be containerized with Docker before being deployed to Kubernetes.
* Do not use the `latest` image tag.
* Do not hardcode passwords, tokens, or secrets inside application code or committed YAML files.
* Use `.env.example` for example environment variables.
* Create real Kubernetes Secrets manually or with `kubectl create secret`.
* Use Kubernetes Service names for communication between Pods.
* Do not use `localhost` or hardcoded Pod IP addresses for Pod-to-Pod communication.
* Every exam must run successfully on Minikube.
* Every project must include a `README.md`.
* Clean up unused resources between exams using:

```bash
kubectl delete -f .
```

or, for Helm-based projects:

```bash
helm uninstall <release-name>
```

Each exam should test some of the following skills:

```text
Docker image build
Docker image load into Minikube
Pods
Deployments
Services
ConfigMaps
Secrets
Namespaces
kubectl daily commands
Ingress
Horizontal Pod Autoscaler
Helm charts
PersistentVolumeClaims
Rolling updates
Rollbacks
Debugging
```

---

# Easy Exams

---

## Easy Exam 1: Python Visit Counter on Kubernetes

### Scenario

Create a simple Python web application that displays a welcome message and counts how many times users visit the website.

The visit counter must be stored in Redis. The application must be containerized with Docker, loaded into Minikube, and deployed using Kubernetes manifests.

### Required Services

```text
web
redis
```

### Required Kubernetes Objects

```text
Namespace
ConfigMap
Redis Deployment
Redis Service
Web Deployment
Web Service
```

### Your Tasks

1. Build a Python web application.

2. Write a custom Dockerfile for the web application.

3. Build the Docker image.

4. Load the image into Minikube using:

```bash
minikube image load
```

or push the image to a local registry.

5. Create a Namespace called:

```text
easy-exam-01
```

6. Create a Deployment for the web application.

7. Create a Deployment for Redis.

8. Create a ClusterIP Service for Redis.

9. Create a NodePort Service for the web application.

10. Store Redis connection values in a ConfigMap:

```text
REDIS_HOST
REDIS_PORT
```

11. Inject the ConfigMap values into the web application as environment variables.

12. Expose the web application using:

```bash
minikube service web -n easy-exam-01
```

13. Scale the web Deployment to 2 replicas:

```bash
kubectl scale deployment web --replicas=2 -n easy-exam-01
```

14. Delete the Redis Pod manually.

15. Confirm that Kubernetes recreates the Redis Pod automatically.

16. Confirm that the visit counter still works after the Redis Pod is recreated.

17. In `README.md`, explain:

```text
What is a Pod?
What is a Deployment?
What is the difference between a Pod and a Deployment?
What is a Kubernetes Service?
Why do we need a Service?
What is the difference between a container and a VM?
```

### Required Deliverables

```text
easy-exam-01/
├── app/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   ├── web-deployment.yaml
│   └── web-service.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The application must be reachable through Minikube.

The visit counter must continue working after the Redis Pod is deleted and recreated.

---

## Easy Exam 2: Node.js Notes Application on Kubernetes

### Scenario

Create a simple Node.js API for storing personal notes.

The notes must be stored in MongoDB. The API must be containerized using Docker and deployed to Minikube using Kubernetes manifests.

### Required Endpoints

```text
GET  /notes
POST /notes
GET  /health
```

### Required Services

```text
api
mongo
```

### Your Tasks

1. Build a Node.js notes API.

2. Write a Dockerfile from scratch for the API.

3. Create a Namespace called:

```text
easy-exam-02
```

4. Deploy MongoDB using a Deployment.

5. Expose MongoDB using a ClusterIP Service.

6. Do not expose MongoDB using NodePort.

7. Deploy the API using a Deployment.

8. Expose the API using a NodePort Service.

9. Store the MongoDB connection string inside a Kubernetes Secret.

10. Do not store credentials inside a ConfigMap.

11. Add liveness and readiness probes to the API using:

```text
/health
```

12. Create at least two notes through the API.

13. Delete the MongoDB Pod.

14. Confirm that the MongoDB Pod is recreated automatically.

15. Attach a PersistentVolumeClaim to MongoDB.

16. Confirm that the notes still exist after the MongoDB Pod is recreated.

17. In `README.md`, explain the difference between:

```text
kubectl apply
kubectl create
```

18. Explain why MongoDB does not need a NodePort Service.

### Required Deliverables

```text
easy-exam-02/
├── app/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── mongo-pvc.yaml
│   ├── mongo-deployment.yaml
│   ├── mongo-service.yaml
│   ├── api-deployment.yaml
│   └── api-service.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The API must be reachable through Minikube.

The notes must remain available after the MongoDB Pod is deleted and recreated.

---

## Easy Exam 3: File Upload Application with Persistent Storage

### Scenario

Create a small web application where users can upload files and view the names of uploaded files.

Uploaded files must be stored in persistent Kubernetes storage so they survive Pod recreation.

### Required Endpoints

```text
GET /
POST /
GET /health
```

### Your Tasks

1. Build the application using Python or Node.js.

2. Write a custom Dockerfile.

3. Store uploaded files inside the container at:

```text
/app/uploads
```

4. Create a Namespace called:

```text
easy-exam-03
```

5. Create a PersistentVolumeClaim.

6. Mount the PVC inside the Deployment at:

```text
/app/uploads
```

7. Expose the application using a NodePort Service.

8. The application must listen on container port:

```text
8080
```

9. Store the upload directory path in a ConfigMap.

10. Inject the upload directory path into the app as an environment variable.

11. Upload at least two files through the application.

12. Delete the Pod manually.

13. Let the Deployment recreate the Pod.

14. Confirm that the uploaded files still exist.

15. Run a temporary debug Pod using:

```bash
kubectl run --rm -it
```

16. Inspect the contents of the PersistentVolumeClaim from the debug Pod.

17. In `README.md`, explain the difference between:

```text
Container writable layer
Kubernetes emptyDir volume
Kubernetes PersistentVolumeClaim
```

### Required Deliverables

```text
easy-exam-03/
├── app/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── pvc.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The application must be reachable through Minikube.

Uploaded files must still exist after the Pod is deleted and recreated.

---

# Medium Exams

---

## Medium Exam 1: URL Shortener Behind an Ingress

### Scenario

Create a URL shortener application.

The application receives a long URL, generates a short code, stores it in PostgreSQL, and redirects users from the short code to the original URL.

The full stack must be reachable through a single Ingress hostname.

### Required Endpoints

```text
POST /shorten
GET  /:code
GET  /health
```

### Required Resources

```text
api       → Deployment + ClusterIP Service
database  → Deployment or StatefulSet + ClusterIP Service + PVC
adminer   → Deployment + ClusterIP Service
ingress   → Routes traffic to API and Adminer
```

### Your Tasks

1. Build the API using Python or Node.js.

2. Write a Dockerfile for the API from scratch.

3. Enable the Minikube Ingress addon:

```bash
minikube addons enable ingress
```

4. Create a Namespace called:

```text
medium-exam-01
```

5. Store database credentials in a Secret.

6. Store non-sensitive configuration in a ConfigMap.

7. Create PostgreSQL with persistent storage using a PVC.

8. Add an init container or readiness probe so the API waits until PostgreSQL is ready.

9. Create Adminer for database inspection.

10. Create a single Ingress resource that routes:

```text
/         → API Service
/adminer  → Adminer Service
```

11. Add the Ingress hostname to your local `/etc/hosts`.

12. Access the application using a hostname, not a raw IP address.

13. Reject invalid URLs in the API.

14. Confirm that a generated short code redirects to the original URL.

15. Delete the database Pod.

16. Confirm that shortened URLs remain stored after the database Pod is recreated.

17. In `README.md`, explain:

```text
Why the database Pod is not a virtual machine
Why Ingress is better than exposing every Service with NodePort
```

### Required Deliverables

```text
medium-exam-01/
├── api/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── configmap.yaml
│   ├── db-pvc.yaml
│   ├── db-deployment.yaml
│   ├── db-service.yaml
│   ├── adminer-deployment.yaml
│   ├── adminer-service.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   └── ingress.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The application must work through Ingress.

PostgreSQL data must survive Pod recreation.

---

## Medium Exam 2: Background Job Processor with Manual and Auto Scaling

### Scenario

Create a background job processing system.

An API receives jobs, stores them in Redis, and a separate worker processes the queued jobs. The worker must be scalable manually and automatically using HPA.

### Required Job Statuses

```text
queued
processing
completed
failed
```

### Required Services

```text
api
worker
redis
```

### Your Tasks

1. Build one Docker image used by both the API and the worker.

2. Run the API as a Deployment.

3. Expose the API using a Kubernetes Service.

4. Run the worker as a separate Deployment.

5. Use a different container command or args for the worker.

6. Create a Namespace called:

```text
medium-exam-02
```

7. Store Redis connection settings in a ConfigMap.

8. Add liveness probes for the API and Redis.

9. Submit at least five jobs through the API.

10. Watch worker logs while jobs are processed:

```bash
kubectl logs -f deployment/worker -n medium-exam-02
```

11. Scale the worker Deployment manually to 3 replicas:

```bash
kubectl scale deployment/worker --replicas=3 -n medium-exam-02
```

12. Confirm that multiple workers process jobs at the same time.

13. Add a Horizontal Pod Autoscaler to the worker Deployment.

14. Generate artificial CPU load to trigger HPA scale-up.

15. Scale the worker Deployment down to 0.

16. Submit a new job.

17. Confirm that the job remains in the `queued` state.

18. Scale the worker back up.

19. Confirm that the queued job is processed.

20. In `README.md`, explain:

```text
Manual scaling with kubectl scale
Automatic scaling with HPA
Difference between an image and multiple containers created from the same image
```

### Required Deliverables

```text
medium-exam-02/
├── app/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── worker-deployment.yaml
│   └── worker-hpa.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

Jobs must remain queued when workers are unavailable.

Workers must process queued jobs when they are scaled back up.

---

## Medium Exam 3: Inventory API with Namespace Isolation

### Scenario

Create an inventory API that stores product data in MySQL.

The API must be exposed through Ingress, while the database must live in a separate isolated Namespace.

### Required Endpoints

```text
GET    /products
POST   /products
PUT    /products/:id
DELETE /products/:id
GET    /health
```

### Required Namespaces

```text
inventory-app
inventory-data
```

### Your Tasks

1. Build the API using Python or Node.js.

2. Write a custom Dockerfile.

3. Create two Namespaces:

```text
inventory-app
inventory-data
```

4. Deploy the API Deployment and Service inside:

```text
inventory-app
```

5. Deploy MySQL Deployment, Service, and PVC inside:

```text
inventory-data
```

6. Connect the API to MySQL using the fully qualified Service name:

```text
mysql.inventory-data.svc.cluster.local
```

7. Create an Ingress resource in `inventory-app`.

8. Expose only the API through Ingress.

9. Store database credentials in a Secret inside `inventory-data`.

10. Copy the required Secret into `inventory-app`.

11. Explain in `README.md` why Kubernetes Secrets are Namespace-scoped.

12. Confirm that the API cannot be reached directly from outside the cluster using a Pod IP.

13. Delete the MySQL Pod.

14. Confirm that product data survives the MySQL Pod restart.

15. Explain why splitting resources into multiple Namespaces is safer than putting everything in `default`.

### Required Deliverables

```text
medium-exam-03/
├── api/
├── Dockerfile
├── k8s/
│   ├── namespaces.yaml
│   ├── data/
│   │   ├── secret.yaml
│   │   ├── mysql-pvc.yaml
│   │   ├── mysql-deployment.yaml
│   │   └── mysql-service.yaml
│   └── app/
│       ├── secret.yaml
│       ├── api-deployment.yaml
│       ├── api-service.yaml
│       └── ingress.yaml
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The API must work through Ingress.

MySQL data must survive Pod recreation.

---

# Hard Exams

---

## Hard Exam 1: Authentication System with Probes and Rolling Updates

### Scenario

Create an authentication API where users can register, log in, log out, and access a protected profile route.

PostgreSQL must store users. Redis must store active sessions or temporary login data.

The system must include probes, resource limits, rolling updates, and rollback testing.

### Required Endpoints

```text
POST /register
POST /login
POST /logout
GET  /profile
GET  /health
```

### Required Services

```text
api
postgres
redis
```

### Your Tasks

1. Write a multi-stage Dockerfile that creates a minimal final image.

2. Run the application container as a non-root user.

3. Hash passwords before storing them.

4. Create a Namespace called:

```text
hard-exam-01
```

5. Store all credentials in Kubernetes Secrets.

6. Do not store credentials in ConfigMaps or plain YAML.

7. Add liveness and readiness probes to:

```text
API
PostgreSQL
Redis
```

8. Set CPU and memory requests and limits on every Deployment.

9. Use a specific pinned image tag.

10. Do not use `latest`.

11. Create a PVC for PostgreSQL.

12. Create a separate PVC for Redis.

13. Register and log in a test user through the API.

14. Trigger a rolling update by changing the API image tag:

```bash
kubectl set image deployment/api api=myapi:v2 -n hard-exam-01
```

15. Watch the rollout:

```bash
kubectl rollout status deployment/api -n hard-exam-01
```

16. Confirm zero downtime using a continuous `curl` loop during the update.

17. Intentionally deploy a broken image version.

18. Roll back using:

```bash
kubectl rollout undo deployment/api -n hard-exam-01
```

19. Stop Redis and document what happens to active sessions.

20. In `README.md`, explain the security difference between container isolation and full VM isolation.

### Required Deliverables

```text
hard-exam-01/
├── api/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── redis-pvc.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   ├── api-deployment.yaml
│   └── api-service.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

Registration, login, protected profile access, rolling update, and rollback must work.

---

## Hard Exam 2: Mini E-Commerce Microservices on Kubernetes

### Scenario

Create a small e-commerce system using two separate microservices: product service and order service.

Each service must have its own database. The order service must not directly access the product database. Instead, it must communicate with the product service through a Kubernetes Service.

The entire system must be exposed through one Ingress gateway.

### Required Resources

```text
Ingress gateway
Product service
Product database
Order service
Order database
```

### Product Endpoints

```text
GET  /products
POST /products
GET  /products/:id
```

### Order Endpoints

```text
GET  /orders
POST /orders
GET  /orders/:id
```

### Your Tasks

1. Write a separate Dockerfile for each service.

2. Create a Namespace called:

```text
hard-exam-02
```

3. Deploy each service as a Deployment.

4. Deploy each database as a Deployment or StatefulSet.

5. Create ClusterIP Services for all internal services.

6. Do not expose services with NodePort.

7. Expose the system only through Ingress.

8. Route traffic as follows:

```text
/api/products → product-service
/api/orders   → order-service
```

9. Give each service its own PVC-backed database.

10. Do not allow the order service to read the product database directly.

11. When creating an order, the order service must call the product service to confirm that the product exists.

12. Store each database credential set in its own Secret.

13. Add readiness probes so traffic is not routed to a service before its database connection is ready.

14. Create an order for an existing product.

15. Confirm that the order succeeds.

16. Create an order for a missing product.

17. Confirm that the order is rejected with a controlled error.

18. Scale the product-service Deployment down to 0.

19. Confirm that the order service returns a controlled error instead of crashing.

20. Restart every Deployment.

21. Confirm that both databases retain their data.

22. In `README.md`, explain why each microservice should have its own database.

### Required Deliverables

```text
hard-exam-02/
├── product-service/
├── order-service/
├── k8s/
│   ├── namespace.yaml
│   ├── ingress.yaml
│   ├── product/
│   └── order/
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
kubectl apply -f k8s/
```

The product and order APIs must work through a single Ingress.

Each database must persist data after restarts.

---

## Hard Exam 3: Monitoring Stack Deployed with Helm

### Scenario

Create an application and monitor it using Prometheus and Grafana.

Prometheus and Grafana must be installed using Helm charts. The application must expose metrics, and Grafana must show dashboards for request rate, errors, response time, and total requests.

### Required Resources

```text
app
load-generator
prometheus
grafana
```

### Required Application Endpoints

```text
GET /
GET /health
GET /metrics
GET /slow
GET /error
```

### Your Tasks

1. Build the application container.

2. Build a separate load-generator container.

3. Create a Namespace called:

```text
hard-exam-03
```

4. Install `kube-prometheus-stack` using Helm.

5. Create a `values.yaml` override file.

6. Customize Grafana admin password using a Secret.

7. Customize the Prometheus scrape interval.

8. Configure Prometheus to scrape the app’s `/metrics` endpoint using either:

```text
ServiceMonitor
scrape annotations
```

9. Add an HPA to the app Deployment based on CPU usage.

10. Document how HPA could be driven by custom metrics such as requests per second.

11. Run the load generator to produce:

```text
Normal requests
Slow requests
Failed requests
```

12. Create Grafana dashboards for:

```text
Request rate
Error rate
Response time
Total requests
```

13. Scale the application down to 0.

14. Confirm that Prometheus reports the target as unavailable.

15. Upgrade the Helm release after changing a value.

16. Confirm that Grafana data persists after the upgrade because of its PVC.

17. In `README.md`, explain:

```text
Application logs vs application metrics
Raw Kubernetes manifests vs Helm charts
```

### Required Deliverables

```text
hard-exam-03/
├── app/
├── load-generator/
├── helm-values/
│   └── monitoring-values.yaml
├── k8s/
│   ├── namespace.yaml
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   ├── app-hpa.yaml
│   └── servicemonitor.yaml
└── README.md
```

### Validation

The examiner must be able to install the monitoring stack with Helm and confirm that Prometheus scrapes the app metrics.

Grafana dashboards must remain available after a Helm upgrade.

---

# Expert Exams

These exams are harder than all previous exams.

---

## Expert Exam 1: Blue-Green Deployment on Kubernetes

### Scenario

Create two versions of the same application and switch live traffic between them by changing a single Kubernetes Service selector.

The application must store data in PostgreSQL. Switching traffic from blue to green must not delete or lose application data.

### Required Resources

```text
app-blue
app-green
app-service
database
ingress
```

### Required Endpoints

```text
GET  /version
GET  /health
GET  /records
POST /records
```

### Your Tasks

1. Build one Docker image.

2. The image must read its version from an environment variable.

3. Create a Namespace called:

```text
expert-exam-01
```

4. Deploy `app-blue` and `app-green` as two separate Deployments from the same image.

5. Use different environment values:

```text
VERSION=blue
VERSION=green
```

6. Give each Deployment a different label:

```text
version: blue
version: green
```

7. Create one Service called:

```text
app-service
```

8. Configure the Service selector to initially send traffic to blue.

9. Expose the Service through Ingress.

10. Store records in PostgreSQL using a PVC.

11. Add liveness and readiness probes to both blue and green.

12. Confirm that `/version` returns:

```text
blue
```

13. Switch traffic to green by patching only the Service selector:

```bash
kubectl patch service app-service -n expert-exam-01 -p '{"spec":{"selector":{"version":"green"}}}'
```

14. Confirm that `/version` now returns:

```text
green
```

15. Confirm that records created before the switch still exist.

16. Scale `app-blue` to 0 after green is stable.

17. Take a PostgreSQL backup using a one-off command with `kubectl exec` and `pg_dump`.

18. Store the backup using a PVC-backed backup Job.

19. Delete the database PVC.

20. Recreate the database.

21. Restore the backup.

22. Confirm that records return after restore.

23. In `README.md`, explain how Kubernetes Services make blue-green deployments easier than doing the same thing with full virtual machines.

### Required Deliverables

```text
expert-exam-01/
├── app/
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── db-pvc.yaml
│   ├── db-statefulset.yaml
│   ├── db-service.yaml
│   ├── app-blue-deployment.yaml
│   ├── app-green-deployment.yaml
│   ├── app-service.yaml
│   ├── ingress.yaml
│   └── backup-job.yaml
├── .env.example
└── README.md
```

### Validation

The examiner must be able to switch traffic from blue to green by changing only the Service selector.

Application data must remain available after the switch and after backup restore.

---

## Expert Exam 2: Asynchronous File Processing Platform

### Scenario

Create a platform where users upload files and workers process them asynchronously.

The platform must use RabbitMQ for messaging, MinIO for file storage, and PostgreSQL for processing results. The whole system must be deployed to Kubernetes and packaged as a Helm chart.

### Required Resources

```text
ingress
api
worker
rabbitmq
database
minio
```

### Required Workflow

```text
User uploads file
API stores file in MinIO
API publishes message to RabbitMQ
Worker consumes message
Worker processes file
Worker calculates metadata
Worker stores result in PostgreSQL
User checks processing status through API
```

### Required Endpoints

```text
POST /files
GET  /files/:id
GET  /files/:id/status
GET  /health
```

### Your Tasks

1. Write a Dockerfile for the API.

2. Write a Dockerfile for the worker.

3. Run both API and worker as non-root users.

4. Package the application as a Helm chart.

5. Include API, worker, ConfigMaps, Secrets, Deployments, and Services in the chart.

6. Deploy RabbitMQ, PostgreSQL, and MinIO as chart dependencies or separate manifests.

7. Create a Namespace called:

```text
expert-exam-02
```

8. Publish only Ingress and required management UIs.

9. Do not expose databases directly.

10. Create PVCs for:

```text
PostgreSQL
RabbitMQ
MinIO
```

11. Add liveness and readiness probes to every custom service.

12. Add an HPA to the worker Deployment.

13. Scale the worker to 0.

14. Upload a file.

15. Confirm that the message remains queued in RabbitMQ.

16. Scale the worker back up.

17. Confirm that the file gets processed.

18. Implement retry handling in the worker.

19. Configure a dead-letter queue in RabbitMQ.

20. Submit an invalid file.

21. Confirm that the invalid job reaches the dead-letter queue after repeated failures.

22. Install the chart with:

```bash
helm install
```

23. Change a value and run:

```bash
helm upgrade
```

24. Confirm that no data is lost.

25. In `README.md`, explain the role of every component and why API and worker should be separate Deployments.

### Required Deliverables

```text
expert-exam-02/
├── api/
├── worker/
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── .env.example
└── README.md
```

### Validation

The examiner must be able to install the platform using Helm.

Files must be processed asynchronously.

Invalid jobs must reach the dead-letter queue after retries.

---

## Expert Exam 3: Complete Local DevOps Platform on Minikube

### Scenario

Build a complete self-hosted project-management platform and deploy it on Minikube using a single umbrella Helm chart.

The platform must include a frontend, API, worker, PostgreSQL, Redis, Prometheus, Grafana, and a backup CronJob.

### Required Resources

```text
ingress
frontend
api
worker
database
redis
prometheus
grafana
backup
```

### Required Features

Users must be able to:

```text
Register
Log in
Create projects
Create tasks
Update task status
Generate reports asynchronously
Check report status
```

### Your Tasks

1. Write a separate multi-stage Dockerfile for:

```text
frontend
api
worker
```

2. Run all custom containers as non-root users.

3. Create at least three Namespaces:

```text
public
application
data
```

or use Network Policies to provide equivalent segmentation.

4. Document your choice in `README.md`.

5. Create PVCs for:

```text
PostgreSQL
Redis
Prometheus
Grafana
```

6. Package the entire platform as one umbrella Helm chart.

7. Do not expose PostgreSQL or Redis through NodePort or Ingress.

8. Only frontend and API traffic should go through Ingress.

9. Add health checks to every Deployment.

10. Add CPU and memory requests and limits.

11. Add restart policies.

12. Use read-only root filesystems where possible.

13. Mount `emptyDir` for required writable temporary paths.

14. Add HPA to the API Deployment.

15. Add HPA to the worker Deployment.

16. Configure Prometheus to scrape the API and worker.

17. Create Grafana dashboards for:

```text
Request count
Error count
Response time
Completed jobs
Failed jobs
```

18. Create a Kubernetes CronJob for PostgreSQL backups.

19. Store backups on a PVC.

20. Restart every Deployment individually using:

```bash
kubectl rollout restart
```

21. Confirm application data survives every restart.

22. Delete test data.

23. Trigger the backup CronJob manually:

```bash
kubectl create job --from=cronjob/<cronjob-name> <job-name>
```

24. Simulate data loss.

25. Restore from backup.

26. Confirm deleted data returns after restore.

27. Draw the full architecture inside `README.md`.

28. In `README.md`, explain:

```text
Containers compared with VMs
Images compared with containers
PersistentVolumeClaims compared with container storage
ClusterIP compared with NodePort compared with Ingress
Default Namespace compared with custom Namespaces
Raw manifests compared with Helm
```

### Required Deliverables

```text
expert-exam-03/
├── frontend/
├── api/
├── worker/
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── k8s/
│   └── backup-cronjob.yaml
├── .env.example
└── README.md
```

### Validation

The examiner must be able to install the full platform using Helm.

The platform must support login, projects, tasks, async reports, monitoring, backups, and restore.

---

# Exam Submission Requirements

Every exam submission must include:

```text
Application source code
Dockerfile or Dockerfiles
Kubernetes manifests or Helm chart
.dockerignore
.env.example
README.md
Architecture diagram
Testing commands
Screenshots
```

## Required Screenshots

```text
kubectl get pods -A
kubectl get svc -A
kubectl get deployments -A
kubectl get pvc -A
kubectl get ingress -A
Application working through Ingress or NodePort
Persistent data confirmed after Pod restart or rollout
```

## Required Commands to Document

```bash
kubectl apply -f k8s/
kubectl get all -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs -f <pod-name> -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout undo deployment/<name> -n <namespace>
kubectl delete -f k8s/
helm install
helm upgrade
helm uninstall
```

## Important Notes

Deleting a PersistentVolumeClaim can permanently delete its stored data unless the underlying PersistentVolume has a `Retain` reclaim policy.

Do not delete PVCs before taking persistence screenshots.

> The goal is not only to deploy working YAML files. The goal is to prove that you understand how Docker images, Pods, Deployments, Services, ConfigMaps, Secrets, Ingress, HPA, Helm, PVCs, rollouts, rollbacks, and debugging work together.

