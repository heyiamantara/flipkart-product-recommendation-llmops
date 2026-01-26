# 🛒 Cloud-Native Flipkart Product Recommendation System (RAG & LLMOps)

An **end-to-end Flipkart product recommendation system** built using
**Retrieval-Augmented Generation (RAG)** and deployed using **Docker,
Kubernetes (Minikube), and Google Cloud Platform**, with **full monitoring
via Prometheus and Grafana**.

This project demonstrates a **production-grade LLMOps pipeline**, covering
data ingestion, recommendation logic, cloud deployment, and observability.

---

## 📌 Project Overview

Modern e-commerce platforms like Flipkart rely on **personalized product
recommendations** to enhance user experience and boost conversions.

This project simulates a **Flipkart-style recommendation engine** that
suggests relevant products using **RAG-based semantic retrieval** combined
with LLM reasoning.

The system is:
- Cloud-native
- Scalable
- Fully containerized
- Observable using monitoring tools

---

## 🏗️ System Architecture & Workflow

<img src="images/System-workflow.png" alt="Flipkart Product Recommendation Workflow" width="900"/>

### 🔄 Architecture Explanation

The system follows a complete **LLMOps lifecycle**:

### 1. Local Project Setup
- API and configuration setup
- Data conversion and preprocessing
- Data ingestion into vector store
- RAG chain implementation
- Flask web application with HTML & CSS frontend

### 2. Containerization & Orchestration
- Application containerized using Docker
- Kubernetes manages pods, services, and secrets
- Secure secret handling via Kubernetes Secrets

### 3. Version Control
- Code managed using GitHub
- Continuous versioning through commits and pushes

### 4. Cloud Deployment
- Google Cloud VM instance provisioning
- Minikube Kubernetes cluster running inside VM
- Application deployed inside the cluster

### 5. Monitoring & Observability
- Prometheus collects application metrics
- Grafana visualizes metrics via dashboards
- Enables real-time monitoring and health tracking

---

## ✨ Key Features

- 🔍 RAG-based product recommendation system
- ⚙️ Flask backend with REST APIs
- 🐳 Dockerized application
- ☸️ Kubernetes orchestration using Minikube
- ☁️ Deployed on Google Cloud VM
- 📊 Monitoring with Prometheus & Grafana
- 🔐 Secure secret management

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Backend:** Flask  
- **LLM / RAG:** Groq, HuggingFace  
- **Containerization:** Docker  
- **Orchestration:** Kubernetes (Minikube)  
- **Cloud:** Google Cloud Platform (VM)  
- **Monitoring:** Prometheus, Grafana  
- **Version Control:** Git & GitHub  

---

## 🚀 Deployment Guide

### 1. Initial Setup

- Push code to GitHub
- Create a `Dockerfile`
- Create Kubernetes deployment YAML
- Create a Google Cloud VM instance:
  - Machine Type: E2 Standard
  - RAM: 16 GB
  - Disk: 256 GB
  - OS: Ubuntu 24.04 LTS
  - Enable HTTP & HTTPS traffic

---

### 2. Configure VM Instance

Clone your GitHub repository on the VM:

    git clone https://github.com/heyiamantara/flipkart-product-recommendation-llmops.git
    ls
    cd flipkart-product-recommendation-llmops
    ls

---

### Install Docker

Follow the official Docker documentation for Ubuntu.

Steps:
1. Search: Install Docker on Ubuntu
2. Open the official site (docs.docker.com)
3. Run the first command block
4. Run the second command block
5. Test Docker installation:

    docker run hello-world

---

### Run Docker Without sudo

From Docker docs → Post-installation steps for Linux  
Run all commands listed there.

Verify:

    docker ps

---

### Enable Docker to Start on Boot

    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service

Verify Docker status:

    systemctl status docker
    docker ps
    docker ps -a

---

### 3. Configure Minikube Inside VM

Install Minikube:

1. Search: Install Minikube
2. Open: minikube.sigs.k8s.io
3. Choose:
   - OS: Linux
   - Architecture: x86
   - Installation: Binary download
4. Copy and execute installation commands on VM

Start Minikube:

    minikube start

---

### Install kubectl

Install kubectl using Snap:

    sudo snap install kubectl --classic

Verify installation:

    kubectl version --client

---

### Verify Kubernetes Cluster

    minikube status
    kubectl get nodes
    kubectl cluster-info
    docker ps

---

### 4. Interlink GitHub on VM

Configure Git credentials:

    git config --global user.email "your-email@gmail.com"
    git config --global user.name "heyiamantara"

Push code changes:

    git add .
    git commit -m "initial commit"
    git push origin main

When prompted:
- Username: "your username"
- Password: GitHub Personal Access Token

---

### 5. Build and Deploy Application on VM

Point Docker to Minikube:

    eval $(minikube docker-env)

Build Docker image:

    docker build -t flask-app:latest .

Create Kubernetes secrets:

    kubectl create secret generic llmops-secrets \
      --from-literal=GROQ_API_KEY="" \
      --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
      --from-literal=ASTRA_DB_KEYSPACE="default_keyspace" \
      --from-literal=ASTRA_DB_API_ENDPOINT="" \
      --from-literal=HF_TOKEN="" \
      --from-literal=HUGGINGFACEHUB_API_TOKEN=""

Deploy application:

    kubectl apply -f flask-deployment.yaml
    kubectl get pods

Expose application:

    kubectl port-forward svc/flask-service 5000:80 --address 0.0.0.0

Access the application:

    http://<VM_EXTERNAL_IP>:5000

---

### 6. Prometheus and Grafana Monitoring

Create monitoring namespace:

    kubectl create namespace monitoring
    kubectl get ns

Deploy Prometheus:

    kubectl apply -f prometheus/prometheus-configmap.yaml
    kubectl apply -f prometheus/prometheus-deployment.yaml

Deploy Grafana:

    kubectl apply -f grafana/grafana-deployment.yaml

Access Prometheus:

    kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090

Access Grafana:

    kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000

Grafana default credentials:

    Username: admin
    Password: admin

Configure Grafana:
1. Go to Settings → Data Sources → Add Data Source
2. Select Prometheus
3. URL: http://prometheus-service.monitoring.svc.cluster.local:9090
4. Click Save & Test
5. Create dashboards for visualization
