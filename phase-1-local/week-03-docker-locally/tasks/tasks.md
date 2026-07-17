# Docker Practical Exams

## General Rules

* Every exam is completely independent.
* Start every exam inside a new empty directory.
* Do not reuse files, containers, networks, images, or volumes from another exam.
* Do not use `localhost` for communication between containers.
* Use Docker Compose service names for container-to-container communication.
* Do not copy passwords directly into the application source code.
* Every project must include a `README.md`.
* Do not include unnecessary files inside Docker images.

Each exam must test:

* Containers compared with virtual machines
* Docker images
* Docker containers
* Docker volumes
* Dockerfile
* Docker Compose
* Docker networks
* Port mapping
* Environment variables
* Application containerisation

---

# Easy Exams

---

## Easy Exam 1: Python Visit Counter

### Scenario

You have a simple Python web application that displays a welcome message and counts how many times users visit the website.

The visit counter must be stored in Redis.

### Your Tasks

1. Create a simple Python web application.

2. Create a custom Dockerfile for the application.

3. Create a Docker Compose file containing:

```text
web
redis
```

4. Connect both services to a custom Docker network.

5. Configure the application to connect to Redis using the Redis service name.

6. Publish the application on:

```text
http://localhost:5000
```

7. Create a named volume for Redis data.

8. Confirm that the counter remains available after the Redis container is removed and recreated.

9. Add a `.dockerignore` file.

10. Use environment variables for the Redis hostname and port.

11. Add a health endpoint:

```text
/health
```

12. In `README.md`, explain:

```text
What is a Docker image?
What is a Docker container?
What is a Docker volume?
What is the difference between a container and a VM?
```

### Required Deliverables

```text
easy-exam-01/
├── application files
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

### Validation

The examiner must be able to run:

```bash
docker compose up -d --build
```

The counter must increase and remain stored after container recreation.

---

## Easy Exam 2: Node.js Notes Application

### Scenario

Create a simple Node.js API for storing personal notes.

Notes must be stored in MongoDB.

### Required Endpoints

```text
GET  /notes
POST /notes
GET  /health
```

### Your Tasks

1. Create the Node.js application.

2. Write a Dockerfile from scratch.

3. Create two services:

```text
api
mongo
```

4. Connect the services using a custom network.

5. Store MongoDB data inside a named volume.

6. Publish the API on port:

```text
3000
```

7. Configure the MongoDB connection using environment variables.

8. Ensure the API uses the service name `mongo` instead of `localhost`.

9. Add `.dockerignore`.

10. Add a health check for the API.

11. Stop and recreate the MongoDB container.

12. Confirm that previously created notes still exist.

13. Document the difference between:

```text
docker run
docker compose up
```

14. Explain why MongoDB does not need a published host port.

### Required Deliverables

```text
easy-exam-02/
├── application files
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

---

## Easy Exam 3: File Upload Application

### Scenario

Create a small web application where users can upload files and view the names of uploaded files.

### Your Tasks

1. Build the application using Python or Node.js.

2. Write a custom Dockerfile.

3. Store uploaded files inside:

```text
/app/uploads
```

4. Attach a named volume to the upload directory.

5. Create a Compose service called:

```text
uploader
```

6. Publish the application on port:

```text
8080
```

7. Add an environment variable for the upload directory.

8. Add a custom network.

9. Upload at least two files.

10. Remove and recreate the container.

11. Confirm that the uploaded files still exist.

12. Run another temporary container and inspect the volume contents.

13. Add `.dockerignore`.

14. Explain the difference between:

```text
Container filesystem
Docker volume
Host bind mount
```

### Required Deliverables

```text
easy-exam-03/
├── application files
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

---

# Medium Exams

---

## Medium Exam 1: URL Shortener

### Scenario

Create an application that receives a long URL and generates a short code.

The application must store URLs in PostgreSQL.

### Required Endpoints

```text
POST /shorten
GET  /:code
GET  /health
```

### Required Services

```text
api
database
adminer
```

### Your Tasks

1. Build the API using Python or Node.js.

2. Write a Dockerfile from scratch.

3. Create a PostgreSQL service.

4. Create an Adminer service.

5. Create a named volume for PostgreSQL.

6. Connect the API and database through a private network.

7. Connect Adminer to the database network.

8. Publish only:

```text
API port
Adminer port
```

9. Store database configuration in environment variables.

10. Add a database health check.

11. Configure the API to wait until the database is healthy.

12. Reject invalid URLs.

13. Confirm that the same short code redirects to the original URL.

14. Recreate the database container and confirm that URLs remain stored.

15. Explain why the database container is not a virtual machine.

### Required Deliverables

```text
medium-exam-01/
├── api/
├── database/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

---

## Medium Exam 2: Background Job Processor

### Scenario

Create a system where an API receives jobs and a separate worker processes them.

Redis must be used as the queue.

### Required Services

```text
api
worker
redis
```

### Required Job Statuses

```text
queued
processing
completed
failed
```

### Your Tasks

1. Create an API for submitting jobs.

2. Create a separate worker process.

3. Use one Docker image for both the API and worker.

4. Use different Compose commands for the API and worker.

5. Connect all services to a custom network.

6. Create a named Redis volume.

7. Add environment variables for Redis connection settings.

8. Add health checks for the API and Redis.

9. Submit at least five jobs.

10. Display worker logs while jobs are processed.

11. Stop the worker.

12. Submit another job.

13. Confirm that the job remains queued.

14. Restart the worker.

15. Confirm that the queued job is processed.

16. Scale the worker service to three containers.

17. Confirm that multiple workers process jobs.

18. Explain the difference between an image and multiple containers created from that image.

### Required Deliverables

```text
medium-exam-02/
├── application files
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

---

## Medium Exam 3: Inventory API Behind Nginx

### Scenario

Create an inventory API and place it behind an Nginx reverse proxy.

MySQL must store the inventory data.

### Required Services

```text
nginx
api
database
```

### Required Endpoints

```text
GET    /products
POST   /products
PUT    /products/:id
DELETE /products/:id
GET    /health
```

### Your Tasks

1. Build the API using Python or Node.js.

2. Write a custom application Dockerfile.

3. Create an Nginx configuration.

4. Create two networks:

```text
frontend
backend
```

5. Connect Nginx and the API to `frontend`.

6. Connect the API and database to `backend`.

7. Do not connect Nginx directly to the database network.

8. Publish only the Nginx port.

9. Store database data in a named volume.

10. Add health checks for the API and database.

11. Configure Nginx to route requests to the API using the API service name.

12. Confirm that the API cannot be accessed directly from the host.

13. Confirm that data survives database container recreation.

14. Explain why custom networks are better than manually using container IP addresses.

### Required Deliverables

```text
medium-exam-03/
├── api/
├── nginx/
├── database/
├── compose.yaml
├── .env.example
└── README.md
```

---

# Hard Exams

---

## Hard Exam 1: Authentication System

### Scenario

Create an authentication API where users can register, log in, and access a protected route.

PostgreSQL must store users, and Redis must store sessions or temporary login data.

### Required Services

```text
nginx
api
database
redis
```

### Required Endpoints

```text
POST /register
POST /login
POST /logout
GET  /profile
GET  /health
```

### Your Tasks

1. Create the authentication application.

2. Hash passwords before storing them.

3. Write a multi-stage Dockerfile.

4. Run the application container as a non-root user.

5. Create separate frontend and backend networks.

6. Publish only the Nginx port.

7. Store PostgreSQL data in a named volume.

8. Store Redis data in a separate named volume.

9. Add health checks to all important services.

10. Use environment variables for all connection settings.

11. Add restart policies.

12. Use specific image versions instead of `latest`.

13. Add a read-only filesystem to the API where possible.

14. Add a temporary filesystem for temporary application files.

15. Test registration and login.

16. Restart the API container and confirm that user data remains available.

17. Stop Redis and document the application behaviour.

18. Explain the security difference between a container and a full VM.

### Required Deliverables

```text
hard-exam-01/
├── api/
├── nginx/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
└── README.md
```

---

## Hard Exam 2: Mini E-Commerce System

### Scenario

Create a small e-commerce system using separate product and order services.

Each service must use its own database.

### Required Services

```text
gateway
product-service
order-service
product-database
order-database
```

### Required Product Endpoints

```text
GET  /products
POST /products
GET  /products/:id
```

### Required Order Endpoints

```text
GET  /orders
POST /orders
GET  /orders/:id
```

### Your Tasks

1. Create a separate Dockerfile for each application service.

2. Create an API gateway using Nginx.

3. Route:

```text
/api/products
/api/orders
```

4. Give the product service its own database.

5. Give the order service its own database.

6. Do not allow the order service to directly read the product database.

7. When creating an order, contact the product service to confirm the product exists.

8. Create separate networks for:

```text
gateway communication
product system
order system
```

9. Publish only the gateway port.

10. Use a separate named volume for each database.

11. Add health checks.

12. Add environment variables.

13. Create an order for an existing product.

14. Reject an order for a missing product.

15. Stop the product service.

16. Confirm that the order service returns a controlled error.

17. Restart the entire Compose project and confirm that data remains available.

18. Explain why one large container should not run all services.

### Required Deliverables

```text
hard-exam-02/
├── gateway/
├── product-service/
├── order-service/
├── compose.yaml
├── .env.example
└── README.md
```

---

## Hard Exam 3: Monitoring System

### Scenario

Create an application and monitor it using Prometheus and Grafana.

### Required Services

```text
app
prometheus
grafana
load-generator
```

### Required Application Endpoints

```text
GET /
GET /health
GET /metrics
GET /slow
GET /error
```

### Required Metrics

```text
Total requests
Requests by endpoint
Requests by status code
Application errors
Request duration
```

### Your Tasks

1. Build the application container.

2. Build a separate load-generator container.

3. Configure Prometheus to collect application metrics.

4. Configure Grafana to use Prometheus as a data source.

5. Store Prometheus data in a named volume.

6. Store Grafana data in another named volume.

7. Create custom networks.

8. Add health checks.

9. Generate normal requests.

10. Generate slow requests.

11. Generate failed requests.

12. Create Grafana panels for:

```text
Request rate
Error rate
Response time
Total requests
```

13. Stop the application container.

14. Confirm that Prometheus reports the application as unavailable.

15. Restart Grafana.

16. Confirm that the dashboard remains available.

17. Explain the difference between application logs and application metrics.

### Required Deliverables

```text
hard-exam-03/
├── app/
├── load-generator/
├── prometheus/
├── grafana/
├── compose.yaml
└── README.md
```

---

# Expert Exams

These exams are harder than all previous exams.

---

## Expert Exam 1: Blue-Green Deployment

### Scenario

Create two versions of the same application and switch traffic between them using Nginx.

### Required Services

```text
nginx
app-blue
app-green
database
backup
```

### Application Versions

```text
Blue version
Green version
```

### Required Endpoints

```text
GET  /version
GET  /health
GET  /records
POST /records
```

### Your Tasks

1. Build one application image that supports different version values through environment variables.

2. Run two containers from the same image:

```text
app-blue
app-green
```

3. Configure Nginx to initially send traffic to blue.

4. Confirm that blue returns its version.

5. Store records in PostgreSQL.

6. Use a named database volume.

7. Add health checks to blue and green.

8. Change Nginx traffic from blue to green.

9. Perform the switch without deleting application data.

10. Stop blue after traffic is moved.

11. Create a backup service using a Compose profile.

12. Store database backups in a named volume.

13. Create a database backup.

14. Delete the database container and database volume.

15. Recreate the database.

16. Restore the backup.

17. Confirm that the records return.

18. Explain how containers allow blue-green deployment more easily than full virtual machines.

### Required Deliverables

```text
expert-exam-01/
├── app/
├── nginx/
├── backup/
├── compose.yaml
├── .env.example
└── README.md
```

---

## Expert Exam 2: File Processing Platform

### Scenario

Create a platform where users upload files and workers process them asynchronously.

### Required Services

```text
nginx
api
worker
rabbitmq
database
minio
```

### Required Workflow

```text
Upload file
Store file in MinIO
Send message to RabbitMQ
Worker receives message
Worker processes file
Worker stores result in PostgreSQL
User checks processing status
```

### Required Endpoints

```text
POST /files
GET  /files/:id
GET  /files/:id/status
GET  /health
```

### Your Tasks

1. Create an API container.

2. Create a separate worker container.

3. Store uploaded files in MinIO.

4. Use RabbitMQ as the message queue.

5. Store processing results in PostgreSQL.

6. Calculate:

```text
Filename
File size
File type
SHA-256 hash
Processing time
```

7. Create separate Docker networks.

8. Publish only Nginx and required management interfaces.

9. Create named volumes for:

```text
PostgreSQL
RabbitMQ
MinIO
```

10. Add health checks.

11. Run application containers as non-root users.

12. Stop the worker.

13. Upload a file.

14. Confirm that the message remains queued.

15. Restart the worker.

16. Confirm that the file is processed.

17. Add retry handling.

18. Add a dead-letter queue.

19. Submit an invalid file.

20. Confirm that the job reaches the dead-letter queue after repeated failures.

21. Explain the role of every container in the architecture.

### Required Deliverables

```text
expert-exam-02/
├── api/
├── worker/
├── nginx/
├── compose.yaml
├── .env.example
└── README.md
```

---

## Expert Exam 3: Complete Local DevOps Platform

### Scenario

Create a complete containerised project-management platform.

### Required Services

```text
nginx
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
Generate reports
View report status
```

### Your Tasks

1. Create a frontend container.

2. Create an API container.

3. Create a worker container.

4. Use PostgreSQL for application data.

5. Use Redis for caching or background jobs.

6. Use Nginx as the only public entry point.

7. Use Prometheus for monitoring.

8. Use Grafana for dashboards.

9. Create a backup container.

10. Create at least three networks:

```text
public
application
data
```

11. Create named volumes for all persistent services.

12. Write a separate Dockerfile for every custom service.

13. Use multi-stage builds.

14. Run custom containers as non-root users.

15. Add `.dockerignore` files.

16. Use `.env.example`.

17. Do not use the `latest` image tag.

18. Add health checks.

19. Add restart policies.

20. Add resource limits.

21. Use read-only filesystems where possible.

22. Do not publish PostgreSQL or Redis ports.

23. Generate reports using the worker.

24. Monitor API requests and worker jobs.

25. Create a Grafana dashboard showing:

```text
Request count
Error count
Response time
Completed jobs
Failed jobs
```

26. Restart every service separately.

27. Confirm that application data remains available.

28. Create a database backup.

29. Delete test data.

30. Restore the backup.

31. Confirm that the deleted data returns.

32. Draw the complete architecture inside `README.md`.

33. Explain:

```text
Containers compared with VMs
Images compared with containers
Volumes compared with container storage
Internal ports compared with published ports
Default network compared with custom networks
```

### Required Deliverables

```text
expert-exam-03/
├── frontend/
├── api/
├── worker/
├── nginx/
├── prometheus/
├── grafana/
├── backup/
├── compose.yaml
├── .env.example
└── README.md
```

---

# Exam Submission Requirements

Every exam submission must include:

```text
Application source code
Dockerfile
compose.yaml
.dockerignore
.env.example
README.md
Architecture diagram
Testing commands
Screenshots
```

## Required Screenshots

```text
docker images
docker compose ps
docker network ls
docker volume ls
Application working
Persistent data after restart
```

## Required Commands to Document

```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs
docker compose down
docker compose down -v
```

## Important

Using:

```bash
docker compose down -v
```

must delete the project volumes and all persistent data.

Do not run this command before taking the persistence screenshots.


