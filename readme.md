# Faucet App - Kubernetes & Docker Deployment

This project is a Django-based **Faucet App**, deployed using **Kubernetes (Minikube)** or **Docker Compose**. It includes monitoring with **Prometheus & Grafana**, and alerting with **Alertmanager**.

---

## **Prerequisites**

Before running the project, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## **Running the Project with Docker Compose**

If you want to run everything **locally without Kubernetes**, use **Docker Compose**.

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/faucet-app.git
cd faucet-app
```

### **2. Create `.env` File for Configuration**

Copy the contents of `.env.dev` into a new `.env` file:

```bash
cp .env.dev .env
```

Then, open `.env` and replace the following variables with your actual values:

```bash
DJANGO_SECRET_KEY=your-secret-key
SEPOLIA_RPC_URL=your-rpc-url
FAUCET_PRIVATE_KEY=your-private-key
FAUCET_ADDRESS=your-address
```

### **3. Build and Run the Containers**

```bash
docker-compose up --build -d
```

This will:

- Start Django (`faucet-app`)
- Start PostgreSQL database (`db`)
- Start **Prometheus**, **Grafana**, and **Alertmanager**

### **4. Access the Services**

- **Faucet App**: `http://localhost:8000`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`
  - Default login: **admin / admin**
  - Add **Prometheus** as a data source (`http://prometheus:9090`)
- **Alertmanager**: `http://localhost:9093`

---

## **Running the Project with Kubernetes (Minikube)**

For **production-like environments**, you can deploy the app on **Kubernetes**.

### **1. Start Minikube**

```bash
minikube start
```

### **2. Enable Kubernetes Ingress**

```bash
minikube addons enable ingress
```

### **3. Update Secrets Configuration**

Before deploying, ensure that the Kubernetes secrets file `secrets.yaml` contains the correct values for:

```yaml
DJANGO_SECRET_KEY: your-secret-key
SEPOLIA_RPC_URL: your-rpc-url
FAUCET_PRIVATE_KEY: your-private-key
FAUCET_ADDRESS: your-address
```

Apply the updated secrets:

```bash
kubectl apply -f k8s/secrets.yaml
```

### **4. Deploy Everything**

```bash
kubectl apply -f k8s --recursive
```

This applies all YAML files inside the `k8s/` directory, including:

- Deployments for Django, PostgreSQL, Prometheus, Grafana, Alertmanager
- Services for exposing applications
- ConfigMaps and Secrets

### **5. Check Running Pods**

```bash
kubectl get pods -A
```

### **6. Get Minikube IP**

```bash
minikube ip
```

Use this IP to access the services.

### **7. Get NodePort for Services**

```bash
kubectl get svc
```

Look for:

- **Faucet App** → Port `8000`
- **Prometheus** → Port `9090`
- **Grafana** → Port `3000`
- **Alertmanager** → Port `9093`

### **8. Access Services**

- **Faucet App**: `http://<minikube-ip>:<node-port>`
- **Prometheus**: `http://<minikube-ip>:<node-port>`
- **Grafana**: `http://<minikube-ip>:<node-port>`
- **Alertmanager**: `http://<minikube-ip>:<node-port>`

---

## **Monitoring & Alerting**

### **1. Prometheus Queries**

- Total Requests per Endpoint:
  ```promql
  sum(rate(http_requests_total{job="django"}[1m])) by (handler)
  ```
- Average Response Time per Endpoint:
  ```promql
  avg(rate(http_request_duration_seconds_sum{job="django"}[1m])) by (handler)
  ```


### **Restart All Pods**

```bash
kubectl delete pod --all
kubectl apply -f k8s --recursive
```

