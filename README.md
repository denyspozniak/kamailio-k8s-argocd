# Kamailio Kubernetes Setup

## Prerequisites

### 1. Install Minikube:

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
### 2. Start Minikube:

```
minikube start
```

### 3. Install ArgoCD:

ArgoCD is a declarative continuous delivery tool for Kubernetes. To install it:

```
kubectl create ns argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

kubectl port-forward svc/argocd-server -n argocd --address 0.0.0.0 8080:443
```
