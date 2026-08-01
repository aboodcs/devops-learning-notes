# 06 - Kubernetes Volumes and Storage

Containers in Kubernetes are **ephemeral**, meaning any data stored inside a container is lost if the container is restarted or replaced.

To persist data beyond a container's lifecycle, Kubernetes uses **Volumes**.

```text
Container
     │
     ▼
Ephemeral Storage
     │
     ▼
Deleted When Container Stops
```

With Kubernetes Volumes:

```text
Container
     │
     ▼
Kubernetes Volume
     │
     ▼
Persistent Data
```

Volumes allow applications to store data safely even when Pods restart.

---

# Why Do We Need Volumes?

Imagine a MySQL Pod.

```text
MySQL Pod
    │
    ▼
Database Files
```

If the Pod crashes or is recreated:

```text
Pod Deleted
     │
     ▼
Database Lost
```

Using a volume:

```text
MySQL Pod
     │
     ▼
Persistent Volume
     │
     ▼
Database Remains
```

The data survives Pod recreation.

---

# How Kubernetes Volumes Work

A volume is attached to a Pod.

```text
Pod
 ├── Container
 └── Volume
        │
        ▼
Persistent Storage
```

Every container inside the Pod can access the mounted volume.

---

# Volume Lifecycle

Unlike the container filesystem, a Kubernetes Volume lives as long as the Pod exists.

```text
Container Restart
      │
      ▼
Volume Still Exists
```

If the entire Pod is deleted, what happens next depends on the type of volume being used.

---

# Types of Kubernetes Volumes

Common volume types include:

```text
emptyDir
hostPath
PersistentVolume (PV)
PersistentVolumeClaim (PVC)
configMap
secret
```

Each type is designed for different use cases.

---

# emptyDir

An `emptyDir` volume is created when a Pod starts.

```text
Pod Starts
     │
     ▼
emptyDir Created
```

Example:

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: demo

spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: /cache
      name: cache

  volumes:
  - name: cache
    emptyDir: {}
```

Characteristics:

```text
Temporary Storage
Shared Between Containers
Deleted When Pod Is Deleted
```

---

# hostPath

A `hostPath` volume mounts a directory from the Kubernetes node.

```text
Node Directory
      │
      ▼
Pod
```

Example:

```yaml
volumes:
- name: logs
  hostPath:
    path: /var/log
```

This is useful for development and testing but should be used carefully in production because Pods become dependent on a specific node.

---

# Persistent Volumes (PV)

A **PersistentVolume (PV)** is storage provided to the cluster.

```text
Cluster
    │
    ▼
Persistent Volume
```

Example:

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: pv-demo

spec:
  capacity:
    storage: 5Gi

  accessModes:
  - ReadWriteOnce

  hostPath:
    path: /data
```

A PV exists independently of Pods.

---

# PersistentVolumeClaim (PVC)

Applications usually do not use a PV directly.

Instead, they create a **PersistentVolumeClaim (PVC)**.

```text
Pod
 │
 ▼
PVC
 │
 ▼
PV
```

Example:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: app-pvc

spec:
  accessModes:
  - ReadWriteOnce

  resources:
    requests:
      storage: 5Gi
```

The PVC requests storage, and Kubernetes binds it to a matching PV.

---

# Mounting a PVC

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: storage
      mountPath: /usr/share/nginx/html

  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: app-pvc
```

The application stores its data inside the persistent volume.

---

# Storage Workflow

```text
Application
      │
      ▼
Pod
      │
      ▼
PersistentVolumeClaim
      │
      ▼
PersistentVolume
      │
      ▼
Physical Storage
```

---

# Access Modes

Persistent Volumes support different access modes.

| Access Mode         | Description                          |
| ------------------- | ------------------------------------ |
| ReadWriteOnce (RWO) | Mounted as read-write by one node    |
| ReadOnlyMany (ROX)  | Mounted read-only by multiple nodes  |
| ReadWriteMany (RWX) | Mounted read-write by multiple nodes |

---

# Storage Classes

StorageClasses allow Kubernetes to dynamically provision storage.

```text
PVC
 │
 ▼
StorageClass
 │
 ▼
Cloud Disk
```

Instead of manually creating a PV, Kubernetes automatically provisions storage when a PVC is created.

---

# ConfigMap and Secret Volumes

ConfigMaps and Secrets can also be mounted as volumes.

```text
ConfigMap
     │
     ▼
Configuration Files

Secret
     │
     ▼
Sensitive Files
```

Applications can read configuration or secrets directly from mounted files.

---

# Example Project Structure

```text
kubernetes/
├── deployment.yaml
├── service.yaml
├── pvc.yaml
├── pv.yaml
└── storageclass.yaml
```

---

# Common Beginner Mistakes

### Storing Data Inside the Container

Bad:

```text
Container
↓

Application Data
```

Data is lost when the Pod is recreated.

Use a Persistent Volume instead.

---

### Using hostPath in Production

`hostPath` ties a Pod to one specific node.

Prefer Persistent Volumes backed by cloud or network storage for production workloads.

---

### Creating a PVC Without Available Storage

A PVC remains in the **Pending** state if no matching PV or StorageClass is available.

---

### Forgetting volumeMounts

Creating a volume alone is not enough.

You must mount it inside the container using `volumeMounts`.

---

### Confusing PV and PVC

Remember:

```text
PV  → Actual Storage

PVC → Request for Storage
```

Applications normally use PVCs, not PVs directly.

---

# Best Practices

```text
Use PVCs instead of directly referencing PVs
Use StorageClasses for dynamic provisioning
Use emptyDir only for temporary data
Avoid hostPath in production
Back up persistent data regularly
Separate application code from persistent storage
```

---

# Useful Commands

Create storage resources:

```bash
kubectl apply -f pv.yaml

kubectl apply -f pvc.yaml
```

List Persistent Volumes:

```bash
kubectl get pv
```

List PersistentVolumeClaims:

```bash
kubectl get pvc
```

Describe a PVC:

```bash
kubectl describe pvc app-pvc
```

Delete a PVC:

```bash
kubectl delete pvc app-pvc
```

---

# Summary

```text
Volumes → Storage attached to Pods
emptyDir → Temporary Pod storage
hostPath → Mount a node directory
PersistentVolume (PV) → Cluster storage resource
PersistentVolumeClaim (PVC) → Request for storage
StorageClass → Dynamic storage provisioning
volumeMounts → Mount storage inside containers
```

> Kubernetes Volumes provide persistent and shared storage for Pods. While containers are ephemeral, volumes ensure important application data survives restarts and Pod recreation. For production workloads, applications typically use **PersistentVolumeClaims (PVCs)** with **StorageClasses** to obtain durable storage dynamically.

