# Locust Load Testing Guide

This README provides an end-to-end guide to installing, running, and using **Locust** to perform load testing on HTTP APIs.

---

## Table of Contents

- [What is Locust](#what-is-locust)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Creating a Locust Test](#creating-a-locust-test)
- [Running Locust](#running-locust)
  - [Running with Web UI](#running-with-web-ui)
  - [Running in Headless Mode](#running-in-headless-mode)
- [Understanding the Locust UI](#understanding-the-locust-ui)
- [Common Locust Concepts](#common-locust-concepts)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## What is Locust

Locust is an open-source, Python-based load testing tool that allows you to define user behavior in code and simulate thousands of concurrent users hitting your application.

Key features:
- Python-based test scripts
- Web UI and headless execution
- Distributed load testing
- Real-time metrics and charts

---

## Prerequisites

- Python **3.8+**
- pip (Python package manager)
- Network access to the system under test

Verify Python:
```bash
python --version
````

---

## Installation

Install Locust using pip:

```bash
pip install locust
```

Verify installation:

```bash
locust --version
```

---

## Project Structure

A minimal Locust project looks like this:

```text
.
├── locustfile.py
└── README.md
```

Locust automatically looks for a file named `locustfile.py`.

---

## Creating a Locust Test

Create a file named `locustfile.py`:

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_posts(self):
        self.client.get("/posts")

    @task(1)
    def get_post_by_id(self):
        self.client.get("/posts/1")

    @task(1)
    def create_post(self):
        payload = {
            "title": "Locust Test",
            "body": "Load testing with Locust",
            "userId": 1
        }
        self.client.post("/posts", json=payload)
```

---

## Running Locust

### Running with Web UI

Start Locust with the target host:

```bash
locust -H https://jsonplaceholder.typicode.com
```

Open your browser and navigate to:

```
http://localhost:8089
```

Enter:

* **Number of users**
* **Spawn rate (users per second)**

Click **Start Swarming** to begin the test.

---

### Running in Headless Mode

Run Locust without the UI (ideal for CI/CD):

```bash
locust \
  -H https://jsonplaceholder.typicode.com \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless
```

---

## Understanding the Locust UI

Key metrics shown in the UI:

* **# Requests** – Total requests sent
* **# Fails** – Number of failed requests
* **Median** – Typical response time
* **95%ile / 99%ile** – Tail latency
* **RPS** – Requests per second

The **Statistics** tab shows per-endpoint performance.

---

## Common Locust Concepts

### Tasks

* Each `@task` represents a user action
* Task weight controls frequency

### Wait Time

Simulates real user think time:

```python
wait_time = between(1, 5)
```

### Client

* `self.client.get()`
* `self.client.post()`
* Automatically handles cookies and sessions

---

## Advanced Usage

### Adding Headers (Auth, API Keys)

```python
def on_start(self):
    self.client.headers.update({
        "Authorization": "Bearer <TOKEN>",
        "Content-Type": "application/json"
    })
```

---

### Validating Responses

```python
with self.client.get("/health", catch_response=True) as response:
    if response.status_code != 200:
        response.failure("Health check failed")
```

---

### Running Distributed Load Tests

```bash
# Master
locust --master -H https://your-api

# Worker
locust --worker --master-host <MASTER_IP>
```

---

## Best Practices

* Start with low load and ramp up gradually
* Define clear performance targets (SLOs)
* Monitor CPU, memory, and database metrics
* Test read and write endpoints separately
* Run soak tests to detect memory leaks

---

## Troubleshooting

### Locust command not found

```bash
pip install --user locust
```

### High latency or failures

* Check backend logs
* Monitor database connections
* Reduce spawn rate and ramp gradually

---

## References

* [https://docs.locust.io](https://docs.locust.io)
* [https://github.com/locustio/locust](https://github.com/locustio/locust)

---

## Summary

Locust enables realistic, scalable, and repeatable load testing using Python. With minimal setup, you can simulate real user behavior and identify performance bottlenecks before they impact production.

```
