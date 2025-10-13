# AutoScaleX — Local Demo (Auto-scaling CI/CD + Monitoring)

This repository is a ready-to-run local demo for the AutoScaleX hackathon project.
It demonstrates a simple Flask app packaged as a Docker image, deployed to a local
Kubernetes (Minikube) cluster with Horizontal Pod Autoscaler (HPA). It also includes
a GitHub Actions workflow for building and scanning the image.

## What's included
- `app.py` — simple Flask app that simulates CPU load
- `requirements.txt` — Python dependencies
- `Dockerfile` — container image
- `k8s/deployment.yaml` — Kubernetes Deployment
- `k8s/service.yaml` — Kubernetes Service (NodePort)
- `k8s/hpa.yaml` — Horizontal Pod Autoscaler (HPA)
- `.github/workflows/main.yml` — GitHub Actions build & scan workflow

## Prerequisites (on the laptop)
- Docker (desktop or engine)
- Minikube
- kubectl
- Helm (for optional Prometheus/Grafana)
- Git
- (Optional) Trivy for local image scanning

## Step-by-step local run guide

### 1) Start Minikube (recommended resources)
```bash
minikube start --cpus=2 --memory=4096
minikube status
```

Enable metrics-server (required by HPA):
```bash
minikube addons enable metrics-server
```

### 2) Build Docker image for Minikube (use Minikube's Docker daemon)
Option A: Use Minikube's Docker environment (recommended)
```bash
eval $(minikube -p minikube docker-env)
docker build -t autoscalex:latest .
```

Option B: Build with your local Docker and push to a registry (if you prefer)
- Tag image: `docker tag autoscalex:latest youruser/autoscalex:latest`
- Push to DockerHub and update `k8s/deployment.yaml` image field.

### 3) Deploy to Kubernetes
```bash
kubectl apply -f k8s/
kubectl get deployments,pods,svc -A
```

### 4) Access the service (NodePort)
```bash
minikube service autoscalex-service
```
This will open the app in your browser (or print a URL). You can also `curl` the NodePort.

### 5) Install Prometheus + Grafana (optional, for monitoring)
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack
```
Forward Grafana to localhost:
```bash
kubectl port-forward svc/monitoring-grafana 3000:80
# then open http://localhost:3000
```
Get Grafana admin password:
```bash
kubectl get secret monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

### 6) Verify HPA and metrics
```bash
kubectl get hpa
kubectl top pods
kubectl get pods -w
```

### 7) Generate load to trigger autoscaling
Open a separate terminal and run:
```bash
kubectl run loadgen --image=busybox -i --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://autoscalex-service:5000; done"
```
Watch pods scale up:
```bash
kubectl get hpa -w
kubectl get pods -w
```

To stop the load generator:
```bash
kubectl delete pod loadgen
```

### 8) GitHub Actions (CI)
The `.github/workflows/main.yml` will build the image and run Trivy scan on push to `main`. Because Minikube is local, the workflow does not deploy automatically to your local cluster. For a fully automated demo, use a cloud cluster or push the built image to DockerHub and apply manifests from the workflow.

## Troubleshooting
- If HPA doesn't show metrics: ensure `metrics-server` is running:
  `kubectl get deployment metrics-server -n kube-system`
- If Minikube is slow: stop other heavy apps, increase memory/CPUs, or use cloud provider.
- If Prometheus fails install: check Helm repo and run `helm repo update`.

## Cleanup
```bash
kubectl delete -f k8s/
helm uninstall monitoring
minikube stop
```

-- End of README --
