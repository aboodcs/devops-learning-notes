# 10 - OKE Kubernetes

**OKE** means **Oracle Kubernetes Engine**.

OKE is Oracle Cloud's managed Kubernetes service.

It lets you run Kubernetes clusters in OCI without manually installing Kubernetes yourself.

```text id="s6q4t1"
OKE = Oracle Kubernetes Engine
```

Simple meaning:

```text id="ap1v8z"
OCI manages the Kubernetes control plane
You manage applications and worker nodes
```

## What Is Kubernetes?

Kubernetes is a platform for running containers.

It helps you manage:

```text id="x9r2qf"
Pods
Deployments
Services
ConfigMaps
Secrets
Ingress
Scaling
Rolling updates
```

Without Kubernetes, you may run containers manually using Docker.

With Kubernetes, you describe what you want, and Kubernetes keeps it running.

## What Is OKE?

OKE is Kubernetes running on Oracle Cloud.

Instead of creating Kubernetes manually on virtual machines, OCI provides a managed Kubernetes service.

```text id="o0ysum"
You
 ↓
Create OKE Cluster
 ↓
Deploy apps using kubectl
 ↓
OCI runs Kubernetes infrastructure
```

## Why Use OKE?

OKE helps you run containerized applications in production.

It gives you:

```text id="h3g2fh"
Managed Kubernetes control plane
Worker nodes on OCI Compute
Integration with OCI Load Balancer
Integration with OCI VCN networking
Scaling support
Better production deployment workflow
```

## Kubernetes Cluster Components

A Kubernetes cluster has two main parts:

```text id="btw7vp"
Control Plane
Worker Nodes
```

## 1. Control Plane

The **Control Plane** manages the Kubernetes cluster.

It is responsible for:

```text id="ndc1s2"
Scheduling Pods
Managing cluster state
Handling API requests
Checking node health
Managing deployments
```

In OKE, OCI manages the control plane for you.

```text id="gug5kz"
OKE Control Plane → Managed by Oracle
```

## 2. Worker Nodes

**Worker Nodes** are the machines that run your application containers.

In OKE, worker nodes are OCI Compute Instances.

```text id="h1a7jf"
OKE Cluster
├── Worker Node 1
├── Worker Node 2
└── Worker Node 3
```

Your Pods run on these worker nodes.

## Simple OKE Architecture

```text id="lm4o4v"
OCI Tenancy
└── Compartment
    └── VCN
        ├── Public Subnet
        │   └── Load Balancer
        │
        └── Private Subnet
            ├── Worker Node 1
            ├── Worker Node 2
            └── Worker Node 3
```

Application traffic flow:

```text id="xz8hu4"
User
 ↓
OCI Load Balancer
 ↓
Kubernetes Service
 ↓
Pods running on worker nodes
```

## OKE vs Self-Managed Kubernetes

| OKE                          | Self-Managed Kubernetes             |
| ---------------------------- | ----------------------------------- |
| Oracle manages control plane | You install and manage everything   |
| Easier to start              | More manual work                    |
| Integrated with OCI          | You configure integrations yourself |
| Good for production          | Good for learning internals         |
| Uses OCI Compute nodes       | Uses any servers you prepare        |

## Main OKE Concepts

```text id="f4fx0e"
Cluster
Node Pool
Worker Node
Pod
Deployment
Service
Load Balancer
kubeconfig
kubectl
```

## 1. Cluster

A **Cluster** is the full Kubernetes environment.

It contains:

```text id="m8b8qn"
Control plane
Worker nodes
Networking
Kubernetes API
Applications
```

Example:

```text id="idj4k0"
Cluster name: dev-oke-cluster
```

## 2. Node Pool

A **Node Pool** is a group of worker nodes with the same configuration.

Example:

```text id="slbqy1"
Node Pool: dev-node-pool
├── Node 1
├── Node 2
└── Node 3
```

A node pool defines things like:

```text id="ny5hqh"
Number of nodes
Compute shape
Operating system image
Subnet
Availability domain
```

## 3. Worker Node

A **Worker Node** is an OCI Compute Instance inside the OKE cluster.

It runs:

```text id="kx8pte"
Pods
Container runtime
Kubelet
Networking components
```

Check nodes using:

```bash id="ivgmso"
kubectl get nodes
```

## 4. Pod

A **Pod** is the smallest unit in Kubernetes.

It usually runs one container.

Example:

```text id="w5s0w8"
Pod
└── Container: nginx
```

Check Pods:

```bash id="ouz3vi"
kubectl get pods
```

## 5. Deployment

A **Deployment** manages Pods.

It makes sure the correct number of Pods are running.

Example:

```yaml id="n9c8hr"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
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

```bash id="lae7sk"
kubectl apply -f deployment.yaml
```

## 6. Service

A **Service** exposes Pods inside or outside the cluster.

Common service types:

```text id="kihlhx"
ClusterIP
NodePort
LoadBalancer
```

For OKE, `LoadBalancer` is important because it can create an OCI Load Balancer.

Example:

```yaml id="ll6v24"
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
```

Apply it:

```bash id="z9xcl2"
kubectl apply -f service.yaml
```

Check the external IP:

```bash id="ob928u"
kubectl get service nginx-service
```

## OKE and OCI Load Balancer

When you create a Kubernetes Service with type `LoadBalancer`, OKE can provision an OCI Load Balancer.

```text id="z8l3rf"
Kubernetes Service type LoadBalancer
        ↓
OCI Load Balancer created
        ↓
Users access the application
```

Example:

```text id="kf3ju2"
User
 ↓
OCI Load Balancer Public IP
 ↓
OKE Service
 ↓
Nginx Pods
```

## kubeconfig

`kubeconfig` is the configuration file used by `kubectl` to connect to a Kubernetes cluster.

Without kubeconfig, your terminal does not know how to talk to the OKE cluster.

Check current Kubernetes context:

```bash id="c7g1fr"
kubectl config current-context
```

List contexts:

```bash id="y802i8"
kubectl config get-contexts
```

## kubectl

`kubectl` is the command-line tool used to manage Kubernetes.

Common commands:

```bash id="rkay5h"
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get namespaces
```

Describe a resource:

```bash id="bg68nz"
kubectl describe pod POD_NAME
```

View logs:

```bash id="cojeug"
kubectl logs POD_NAME
```

## Basic OKE Workflow

```text id="msjzdk"
1. Create VCN
2. Create OKE cluster
3. Create node pool
4. Configure kubeconfig
5. Use kubectl
6. Deploy application
7. Expose application using Service
8. Monitor and troubleshoot
```

## Console Path

To create or manage OKE:

```text id="zhk58m"
OCI Console
→ Developer Services
→ Kubernetes Clusters
```

During cluster creation, you usually choose:

```text id="e1v6lm"
Compartment
Kubernetes cluster name
VCN
Subnets
Node pool
Worker node shape
Number of nodes
```

## OKE Networking

OKE needs OCI networking.

Important networking resources:

```text id="puuf36"
VCN
Subnets
Route Tables
Security Lists or NSGs
Internet Gateway
NAT Gateway
Load Balancer
```

A common production-style design:

```text id="f6232t"
VCN
├── Public Subnet
│   └── Load Balancer
│
└── Private Subnet
    └── Worker Nodes
```

This keeps worker nodes private and exposes only the Load Balancer.

## Public Nodes vs Private Nodes

### Public Worker Nodes

Public nodes can have public IP addresses.

They are easier for labs, but less secure.

```text id="lvy1bq"
Internet
 ↓
Worker Node with Public IP
```

### Private Worker Nodes

Private nodes do not have public IP addresses.

They are better for real projects.

```text id="y5p7ak"
Internet
 ↓
Load Balancer
 ↓
Private Worker Nodes
```

## OKE and Container Images

OKE runs containers from container images.

Images can come from:

```text id="mb98gc"
Docker Hub
GitHub Container Registry
Oracle Container Registry
Oracle Cloud Infrastructure Registry
```

Example image:

```text id="pgi7n7"
nginx:alpine
```

Example Deployment uses the image:

```yaml id="jhlh5i"
containers:
  - name: nginx
    image: nginx:alpine
```

## OKE and OCIR

**OCIR** means **Oracle Cloud Infrastructure Registry**.

It is OCI's container image registry.

You can use it to store Docker images.

```text id="od60hm"
Docker build
   ↓
Push image to OCIR
   ↓
OKE pulls image
   ↓
Pods run application
```

## Example App Deployment

Create `deployment.yaml`:

```yaml id="gyv0ih"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-oke
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-oke
  template:
    metadata:
      labels:
        app: hello-oke
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
```

Create `service.yaml`:

```yaml id="0yjk85"
apiVersion: v1
kind: Service
metadata:
  name: hello-oke-service
spec:
  type: LoadBalancer
  selector:
    app: hello-oke
  ports:
    - port: 80
      targetPort: 80
```

Apply:

```bash id="1h4nnn"
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Check resources:

```bash id="ou7jt4"
kubectl get pods
kubectl get deployments
kubectl get services
```

## Scaling an Application

Scale the Deployment to 4 replicas:

```bash id="j1n7y2"
kubectl scale deployment hello-oke --replicas=4
```

Check Pods:

```bash id="a58y49"
kubectl get pods
```

Kubernetes will create more Pods.

```text id="zmrlv3"
2 Pods → 4 Pods
```

## Rolling Update

If you update the image, Kubernetes can roll out the new version gradually.

Example:

```bash id="np3ffy"
kubectl set image deployment/hello-oke nginx=nginx:latest
```

Check rollout:

```bash id="l7ssww"
kubectl rollout status deployment/hello-oke
```

Rollback if needed:

```bash id="hv6kp3"
kubectl rollout undo deployment/hello-oke
```

## OKE and IAM

OKE needs IAM permissions to create and manage cloud resources.

Examples:

```text id="q4h1ym"
Create worker nodes
Create load balancers
Use networking resources
Pull images from registry
Manage cluster resources
```

For real projects, do not give everyone full admin access.

Use groups and policies carefully.

## OKE and DevOps

OKE is important in DevOps because it supports:

```text id="nhu6au"
Container deployments
CI/CD pipelines
Rolling updates
Helm deployments
GitOps with Argo CD
Auto scaling
Production Kubernetes workloads
```

Example CI/CD flow:

```text id="gxlohn"
Developer pushes code
        ↓
GitHub Actions builds Docker image
        ↓
Image pushed to registry
        ↓
OKE deploys new version
```

## OKE with Helm

You can deploy applications to OKE using Helm.

Example:

```bash id="hxcwyg"
helm install nginx-release ./nginx-chart
```

Upgrade:

```bash id="2j3ti2"
helm upgrade nginx-release ./nginx-chart
```

Rollback:

```bash id="gujeqg"
helm rollback nginx-release 1
```

OKE is just Kubernetes, so normal Helm commands work.

## OKE with Terraform

Terraform can create OKE infrastructure using code.

Terraform can manage:

```text id="bzdgji"
VCN
Subnets
Security rules
OKE cluster
Node pools
Load balancers
IAM policies
```

Simple idea:

```text id="fljo7m"
Terraform code
   ↓
OCI Provider
   ↓
OKE Cluster
```

This is useful for repeatable DevOps environments.

## Monitoring OKE

You should monitor:

```text id="x7wl72"
Node health
Pod status
CPU usage
Memory usage
Application logs
Service health
Load Balancer status
```

Useful commands:

```bash id="xseqx0"
kubectl get nodes
kubectl get pods -A
kubectl describe node NODE_NAME
kubectl top nodes
kubectl top pods
```

`kubectl top` needs metrics to be available in the cluster.

## Common Beginner Mistakes

### Forgetting kubeconfig

Problem:

```text id="f35fdd"
kubectl cannot connect to the cluster
```

Check:

```bash id="dj7o1e"
kubectl config get-contexts
```

### Worker Nodes Not Ready

Check nodes:

```bash id="yd71i3"
kubectl get nodes
```

Describe node:

```bash id="tgknpj"
kubectl describe node NODE_NAME
```

Possible reasons:

```text id="nh870t"
Networking issue
Node pool problem
Image pull issue
Security rules issue
Cluster not fully ready
```

### LoadBalancer Service Stuck

If the external IP is pending:

```bash id="3vrlui"
kubectl get svc
```

Check:

```text id="vn6mi0"
Is the cluster allowed to create Load Balancers?
Are subnets correct?
Are security rules correct?
Is the service type LoadBalancer?
```

### ImagePullBackOff

This means Kubernetes cannot pull the container image.

Possible reasons:

```text id="fxa31i"
Wrong image name
Private registry needs credentials
Image tag does not exist
Registry access issue
```

Check:

```bash id="cxfat1"
kubectl describe pod POD_NAME
```

### CrashLoopBackOff

This means the container starts, crashes, and Kubernetes keeps restarting it.

Check logs:

```bash id="c3xc2d"
kubectl logs POD_NAME
```

Describe the Pod:

```bash id="ucdnb3"
kubectl describe pod POD_NAME
```

## Simple Troubleshooting Flow

```text id="kh4q94"
1. kubectl get nodes
2. kubectl get pods -A
3. kubectl describe pod POD_NAME
4. kubectl logs POD_NAME
5. kubectl get svc
6. Check OCI Load Balancer
7. Check security rules
8. Check application configuration
```

## Cleanup

Delete application resources:

```bash id="tpdgn9"
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
```

Or delete by name:

```bash id="i6g7w6"
kubectl delete service hello-oke-service
kubectl delete deployment hello-oke
```

For cloud resources like OKE cluster, node pools, and load balancers, delete them from OCI Console or Terraform if you created them using Terraform.

## Summary

```text id="oe7e56"
OKE          → Oracle Kubernetes Engine
Cluster      → Full Kubernetes environment
Control Plane → Managed by OCI
Node Pool    → Group of worker nodes
Worker Node  → OCI Compute Instance running Pods
Pod          → Smallest Kubernetes unit
Deployment   → Manages Pods and replicas
Service      → Exposes Pods
LoadBalancer → Creates OCI Load Balancer for external access
kubeconfig   → Connects kubectl to the cluster
kubectl      → CLI tool for Kubernetes
```

> OKE is Oracle Cloud's managed Kubernetes service. It lets you run containerized applications on Kubernetes while OCI manages the control plane.

