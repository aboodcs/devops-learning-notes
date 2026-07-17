# Kubernetes: Pods, Deployments, and Services

Kubernetes uses different objects to run and manage applications.

The three most important beginner objects are:

```text
Pod → Runs the application
Deployment → Manages the Pods
Service → Gives stable network access
```

## 1. Pod

A **Pod** is the smallest unit in Kubernetes.

A Pod usually contains one application container.

Example:

```text
Pod
└── Nginx container
```

You normally do not manage Pods directly in real projects because Pods can be deleted and recreated.

Create a simple Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 80
```

Apply it:

```bash
kubectl apply -f pod.yaml
```

Check it:

```bash
kubectl get pods
```

A Pod:

* Runs one or more containers
* Has its own IP address
* Can be deleted and recreated
* Is temporary

## 2. Deployment

A **Deployment** manages Pods.

It tells Kubernetes:

* Which image to run
* How many Pod replicas are needed
* How to update the application
* How to replace failed Pods

Example:

```text
Deployment
├── Pod 1
├── Pod 2
└── Pod 3
```

Deployment example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
```

Apply it:

```bash
kubectl apply -f deployment.yaml
```

Check the Deployment:

```bash
kubectl get deployments
```

Check its Pods:

```bash
kubectl get pods
```

If one Pod fails, the Deployment creates another one automatically.

A Deployment:

* Creates and manages Pods
* Keeps the required number of replicas running
* Replaces failed Pods
* Supports application updates
* Supports scaling

Scale it:

```bash
kubectl scale deployment nginx-deployment --replicas=5
```

## 3. Service

A **Service** gives stable network access to Pods.

Pods can be recreated, and their IP addresses can change.

A Service provides:

* A stable IP address
* A stable DNS name
* Load balancing between Pods

Example:

```text
User
  │
  ▼
Service
  ├── Pod 1
  ├── Pod 2
  └── Pod 3
```

Service example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx

  ports:
    - port: 80
      targetPort: 80

  type: ClusterIP
```

Apply it:

```bash
kubectl apply -f service.yaml
```

Check it:

```bash
kubectl get services
```

The selector:

```yaml
selector:
  app: nginx
```

connects the Service to Pods that have this label:

```yaml
labels:
  app: nginx
```

## Service Types

### ClusterIP

Used for communication inside the Kubernetes cluster.

```yaml
type: ClusterIP
```

This is the default Service type.

### NodePort

Opens the application on a port on every Kubernetes node.

```yaml
type: NodePort
```

Example:

```text
http://NODE-IP:NODE-PORT
```

### LoadBalancer

Creates an external load balancer in cloud environments.

```yaml
type: LoadBalancer
```

It is commonly used on AWS, Azure, and Google Cloud.

## How They Work Together

```text
User
  │
  ▼
Service
  │
  ▼
Deployment
  ├── Pod 1
  ├── Pod 2
  └── Pod 3
```

The flow is:

```text
1. Deployment creates the Pods
2. Pods run the containers
3. Service sends traffic to the Pods
```

## Simple Example

Suppose you want to run an Nginx website.

The **Pod** runs the Nginx container.

The **Deployment** makes sure three Nginx Pods are always running.

The **Service** gives users one stable address and distributes requests between the Pods.

## Main Difference

| Object     | What It Does                   |
| ---------- | ------------------------------ |
| Pod        | Runs the container             |
| Deployment | Manages and scales Pods        |
| Service    | Provides stable access to Pods |

## Useful Commands

View Pods:

```bash
kubectl get pods
```

View Deployments:

```bash
kubectl get deployments
```

View Services:

```bash
kubectl get services
```

View everything:

```bash
kubectl get all
```

Delete the resources:

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

## Summary

```text
Pod        → Runs the application container
Deployment → Creates, replaces, updates, and scales Pods
Service    → Provides stable networking and load balancing
```

> A Pod runs the application, a Deployment manages the Pods, and a Service connects users or other applications to them.

