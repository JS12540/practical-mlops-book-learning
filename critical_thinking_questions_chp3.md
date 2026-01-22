# Critical Thinking Discussion – Practical MLOps (Chapter 3)

This document provides detailed answers to the critical thinking discussion questions based on **Chapter 3 of _Practical MLOps_**, with additional practical context and examples.

---

## 1. Can a container be used to perform online predictions with an Edge TPU device like Coral?

**Yes, it is possible**, but there are important constraints and requirements.

### How it works

A container **can run inference workloads** that use an Edge TPU (such as Google Coral) if:
- The **host OS has the Edge TPU drivers installed**
- The TPU device is **passed into the container**
- The container image includes the **Edge TPU runtime and libraries**
- The ML model is compiled specifically for the Edge TPU (e.g., using `edgetpu_compiler`)

For example:
- On Linux, you can pass the USB Edge TPU into the container using:
  ```bash
  docker run --device=/dev/bus/usb ...
  ```
- The container runs a lightweight inference server (Flask, FastAPI, gRPC)
- The model performs **low-latency, real-time predictions** at the edge

### Why it can be challenging

- Containers **do not virtualize hardware**, they share the host kernel
- TPU drivers **must exist on the host**, not just in the container
- Edge TPUs support **only specific operations** (e.g., quantized TensorFlow Lite models)
- Debugging hardware access inside containers can be complex

### Conclusion

Containers work well for **deployment consistency**, but Edge TPU usage requires:
- Tight coupling with host hardware
- Specialized model formats
- Careful device and driver configuration

---

## 2. What is a container runtime, and how does it relate to Docker?

A **container runtime** is the software responsible for:
- Running containers
- Managing container lifecycle (start, stop, delete)
- Handling isolation (namespaces, cgroups)
- Interacting with the OS kernel

### Relationship to Docker

Docker is **not just a runtime**, but a complete platform.

Docker includes:
- **Docker CLI** – user interface
- **Docker Engine** – daemon that manages containers
- **containerd** – the actual container runtime
- **runc** – low-level runtime that interfaces with the Linux kernel

### Key point

Docker **uses container runtimes**, but Docker itself is **not the runtime**.

Other container runtimes include:
- containerd
- CRI-O
- Podman

These runtimes are commonly used by orchestration tools like Kubernetes.

---

## 3. Three good practices when creating a Dockerfile

### 1. Use minimal base images

- Choose lightweight images like `python:3.x-slim` or `alpine`
- Reduces image size, build time, and attack surface

**Why it matters:** Smaller images are faster to deploy and more secure.

### 2. Leverage Docker layer caching

- Copy dependency files first (e.g., `requirements.txt`)
- Install dependencies before copying application code

Example:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**Why it matters:** Speeds up rebuilds and CI pipelines.

### 3. Avoid running containers as root

- Use a non-root user inside the container
- Reduces security risks

Example:
```dockerfile
RUN useradd -m appuser
USER appuser
```

**Why it matters:** Limits damage if a container is compromised.

---

## 4. Two critical DevOps concepts mentioned in Chapter 3 and why they are useful

### 1. Continuous Integration (CI)

**Definition:**
Automatically testing and validating code whenever changes are made.

**Why it's useful in MLOps:**
- Detects broken pipelines early
- Ensures models, data, and code work together
- Prevents deployment of faulty models

### 2. Continuous Deployment / Continuous Delivery (CD)

**Definition:**
Automatically deploying validated code or models to production or staging environments.

**Why it's useful in MLOps:**
- Enables rapid iteration of models
- Reduces manual deployment errors
- Supports frequent model updates and retraining

---

## 5. Definition of "the edge" and ML examples

### Definition (in my own words)

**The edge** refers to computing that happens **close to where data is generated**, rather than in a centralized cloud or data center. This often means running ML models directly on devices like sensors, cameras, phones, or embedded systems.

### Why edge ML is important

- Low latency (real-time decisions)
- Reduced bandwidth usage
- Improved privacy (data doesn't leave the device)
- Works even with limited or no internet connectivity

### Examples of ML at the edge

1. **Computer Vision on Cameras**
   - Face detection on security cameras
   - Defect detection on factory assembly lines

2. **Speech Recognition**
   - Voice assistants processing wake words locally
   - On-device transcription

3. **Predictive Maintenance**
   - ML models running on industrial sensors
   - Detecting anomalies in vibration or temperature data

4. **Autonomous Systems**
   - Drones using onboard ML for navigation
   - Robots making movement decisions in real time

---

## Summary

- Containers **can** be used with Edge TPUs, but hardware access must be carefully managed
- A container runtime is the engine that runs containers; Docker builds on top of it
- Well-written Dockerfiles improve security, performance, and reliability
- CI/CD are core DevOps practices that enable scalable and reliable ML systems
- Edge ML brings intelligence closer to data sources for faster, safer decisions
