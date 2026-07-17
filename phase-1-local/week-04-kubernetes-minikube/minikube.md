# Minikube

**Minikube** is a tool that runs a small Kubernetes cluster on your local machine.

It is used for learning and practice before working with real Kubernetes clusters in the cloud.

```text id="hyyksp"
Your Laptop
└── Minikube
    └── Kubernetes Cluster
        ├── Pods
        ├── Deployments
        └── Services
```

## Why Do We Use Minikube?

In real companies, Kubernetes usually runs on cloud servers.

For learning, we do not need a big cloud cluster.

Minikube lets us practice Kubernetes locally on one machine.

You can use it to practice:

```text id="o9a3f1"
Pods
Deployments
Services
ConfigMaps
Secrets
Volumes
Namespaces
Ingress
```

## Minikube vs Kubernetes

| Kubernetes                       | Minikube                      |
| -------------------------------- | ----------------------------- |
| Container orchestration platform | Local Kubernetes cluster      |
| Used in real production systems  | Used for learning and testing |
| Can run many nodes               | Usually runs one local node   |
| Runs on cloud or servers         | Runs on your laptop           |

## Check Minikube Version

```bash id="t6hrio"
minikube version
```

Check Kubernetes client:

```bash id="pgaz29"
kubectl version --client
```

## Start Minikube

```bash id="f1f0qc"
minikube start
```

If you are using Docker as the driver:

```bash id="d5442h"
minikube start --driver=docker
```

Check status:

```bash id="c6q39f"
minikube status
```

Expected result:

```text id="yf1a6x"
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

## Check the Cluster

```bash id="efnsre"
kubectl cluster-info
```

View nodes:

```bash id="dug7b2"
kubectl get nodes
```

You should see one node:

```text id="azk5fz"
minikube
```

## Run a Simple Pod

Create `pod.yaml`:

```yaml id="fy2td8"
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

```bash id="dce4f4"
kubectl apply -f pod.yaml
```

Check it:

```bash id="ce9wuk"
kubectl get pods
```

Describe it:

```bash id="6qwl32"
kubectl describe pod nginx-pod
```

Delete it:

```bash id="5413jp"
kubectl delete -f pod.yaml
```

## Run a Deployment

Create `deployment.yaml`:

```yaml id="n4fwbd"
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

```bash id="j4bovu"
kubectl apply -f deployment.yaml
```

Check the Deployment:

```bash id="q1uln2"
kubectl get deployments
```

Check the Pods:

```bash id="78b85p"
kubectl get pods
```

Scale the Deployment:

```bash id="zraocx"
kubectl scale deployment nginx-deployment --replicas=4
```

Check again:

```bash id="0leeky"
kubectl get pods
```

## Create a Service

A Service gives stable access to the Pods.

Create `service.yaml`:

```yaml id="w8l28i"
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

  type: NodePort
```

Apply it:

```bash id="hbr46v"
kubectl apply -f service.yaml
```

Check Services:

```bash id="ek2z0v"
kubectl get services
```

Open the application:

```bash id="8tr4pb"
minikube service nginx-service
```

Or get the URL:

```bash id="b6co6s"
minikube service nginx-service --url
```

## Useful Minikube Commands

Start Minikube:

```bash id="670my4"
minikube start
```

Stop Minikube:

```bash id="uj1dbq"
minikube stop
```

Delete Minikube cluster:

```bash id="yf2qj9"
minikube delete
```

Open Kubernetes dashboard:

```bash id="nf6tuq"
minikube dashboard
```

View Minikube IP:

```bash id="i1lylu"
minikube ip
```

SSH into Minikube node:

```bash id="kkr4im"
minikube ssh
```

Check status:

```bash id="3l4t0f"
minikube status
```

## Useful kubectl Commands

View everything:

```bash id="53wkjd"
kubectl get all
```

View Pods:

```bash id="za82j9"
kubectl get pods
```

View Deployments:

```bash id="r29bw8"
kubectl get deployments
```

View Services:

```bash id="3qfzk4"
kubectl get services
```

Describe a resource:

```bash id="q61x2t"
kubectl describe pod pod-name
```

View logs:

```bash id="8td3qs"
kubectl logs pod-name
```

Enter a Pod:

```bash id="85714d"
kubectl exec -it pod-name -- sh
```

Delete a resource:

```bash id="6lsdtj"
kubectl delete -f file.yaml
```

## Common Problems

### Minikube is not running

Error:

```text id="y0paqy"
The connection to the server was refused
```

Fix:

```bash id="vyu4ju"
minikube start
```

Check:

```bash id="8m7yk5"
minikube status
```

### Pod is stuck

Check the Pod:

```bash id="jyyd56"
kubectl describe pod pod-name
```

Check logs:

```bash id="ro15zw"
kubectl logs pod-name
```

### ImagePullBackOff

This means Kubernetes could not pull the Docker image.

Check the image name:

```bash id="plq3yq"
kubectl describe pod pod-name
```

Example mistake:

```text id="4e00g4"
ngnix
```

Correct image:

```text id="2b2f96"
nginx
```

## Clean Up the Lab

Delete the Service:

```bash id="bnp1qt"
kubectl delete -f service.yaml
```

Delete the Deployment:

```bash id="j0zc89"
kubectl delete -f deployment.yaml
```

Check everything:

```bash id="p41vha"
kubectl get all
```

Stop Minikube:

```bash id="pn8ejh"
minikube stop
```

## Summary

```text id="dtup1b"
Minikube   → Runs Kubernetes locally
kubectl    → Controls the Kubernetes cluster
Pod        → Runs the application container
Deployment → Manages and scales Pods
Service    → Gives stable access to Pods
```

> Minikube is the easiest way to practice Kubernetes on your own machine.

