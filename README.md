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
minikube addons enable registry
```

### 3. Install ArgoCD:

ArgoCD is a declarative continuous delivery tool for Kubernetes. To install it:

```
kubectl create ns argocd
kubectl create ns kamailio

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
minikube service -n argocd argocd-server --url &

argocd login --insecure --username admin --password PASSWORD --grpc-web 127.0.0.1:PORT



minikube service -n kamailio-3g kamailio-3g


or use:

kubectl port-forward svc/argocd-server -n argocd --address 0.0.0.0 8080:443
kubectl port-forward svc/kamailio-3g -n kamailio-3g 5060:5060
```

### 4. Using minikube image registry:

```
https://stackoverflow.com/questions/42564058/how-can-i-use-local-docker-images-with-minikube
https://minikube.sigs.k8s.io/docs/handbook/pushing/#Linux
https://www.baeldung.com/ops/docker-local-images-minikube

minikube image load <image name>

or try to build inside minikube:

eval $(minikube docker-env)
#eval $(minikube docker-env -u)
docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker build . -t kamailio
#docker tag kamailio localhost:5000/kamailio
#docker push localhost:5000/kamailio
curl -X GET http://docker.local:5000/v2/ubuntu/tags/list
```

### 5. Debugging pods:

The command `kubectl debug` allows you to troubleshoot running pods by creating a temporary container with debugging tools. In this example, we're using the nicolaka/netshoot image which contains networking troubleshooting utilities.

The command format is:
```
kubectl debug kamailio-3g-78c879f4c8-hcjr5 -n kamailio-3g -it --image=nicolaka/netshoot
```
