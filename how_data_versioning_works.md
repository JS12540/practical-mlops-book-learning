# 🗂️ Data Versioning in Machine Learning: Production Guide

## 📋 Table of Contents
- [What is Data Versioning?](#1️⃣-what-is-data-versioning-in-plain-english)
- [Why It's Critical](#2️⃣-why-data-versioning-is-critical-in-production)
- [Production Pipeline Flow](#3️⃣-high-level-production-flow-data--model)
- [Key Concepts](#4️⃣-key-concepts-before-examples)
- [Part A: DVC (Data Version Control)](#part-a--data-versioning-using-dvc-industry-standard)
- [Part B: AWS Native Tools](#part-b--data-versioning-using-aws-native-tools)
- [Part C: DVC vs AWS Native](#part-c--dvc-vs-aws-native-when-to-use-what)
- [Mental Model](#11️⃣-mental-model-to-remember-forever)

---

## 1️⃣ What is data versioning (in plain English)?

**Data versioning = the ability to answer these questions anytime in production:**

* Which **exact data** was used to train **this model**?
* If the model breaks today, can I **reproduce** yesterday's results?
* If data changes, can I **roll back** safely?
* Can I compare **Model v3 trained on Data v7** vs **Model v4 trained on Data v9**?

👉 Think of it like **Git for data**, but data is huge and lives outside Git.

---

## 2️⃣ Why data versioning is CRITICAL in production

**Without data versioning:**

* You **can't reproduce** model behavior
* Debugging becomes guesswork
* Compliance / audits fail
* Retraining becomes risky

**With data versioning:**

* Every model is **traceable**
* Training is **deterministic**
* Rollbacks are **safe**
* Experiments are **comparable**

---

## 3️⃣ High-level production flow (data → model)

Let's anchor everything to this real pipeline:

```
Raw Data (Data Lake)
   ↓
ETL / Feature Engineering
   ↓
Curated / Feature Dataset
   ↓
Model Training
   ↓
Model Artifact + Metadata
```

Data versioning tracks **every arrow** here.

---

## 4️⃣ Key concepts (before examples)

| Concept                  | Meaning                               |
| ------------------------ | ------------------------------------- |
| **Data version**         | Immutable snapshot of data            |
| **Dataset hash**         | Fingerprint of the data               |
| **Lineage**              | Where data came from & how it changed |
| **Model ↔ Data mapping** | Which data trained which model        |

---

# PART A — DATA VERSIONING USING **DVC** (Industry-standard)

## 5️⃣ What DVC actually does

DVC:

* Stores **metadata in Git**
* Stores **actual data in S3**
* Tracks data via **hashes**
* Links **code + data + model**

### Architecture (DVC)

```
Git Repo
 ├── code/
 ├── data.dvc (pointer file)
 ├── model.dvc
 └── dvc.lock (exact versions)
```

Actual data lives in **S3**, not Git.

---

## 6️⃣ End-to-end example (DVC + AWS S3)

### 🔹 Step 1: Raw data lands in Data Lake

```
s3://my-datalake/raw/transactions/2024-01-01.csv
```

You **don't modify** this. Raw data is append-only.

---

### 🔹 Step 2: ETL creates training dataset

ETL job outputs:

```
data/processed/train.csv
data/processed/val.csv
```

Now version it 👇

```bash
dvc add data/processed/
git add data/processed.dvc .gitignore
git commit -m "Add processed training data v1"
```

What happens:

* DVC computes **hash of files**
* Uploads data to S3 (DVC remote)
* Git stores **only metadata**

---

### 🔹 Step 3: Train model using this data

```bash
python train.py --data data/processed/
```

Output:

```
models/fraud_model.pkl
```

Version it:

```bash
dvc add models/fraud_model.pkl
git add models/fraud_model.pkl.dvc
git commit -m "Train model v1 on data v1"
```

Now you have:

```
Model v1 → Data v1 (locked)
```

---

### 🔹 Step 4: New data arrives → retrain

Raw data updates:

```
transactions/2024-01-02.csv
```

ETL reruns → new features

```bash
dvc add data/processed/
git commit -m "Processed data v2"
```

Retrain:

```bash
dvc add models/fraud_model.pkl
git commit -m "Train model v2 on data v2"
```

Now:

| Model | Data Version |
| ----- | ------------ |
| v1    | data v1      |
| v2    | data v2      |

💡 You can **checkout any version**:

```bash
git checkout <commit>
dvc pull
```

Boom — exact data + model restored.

---

## 7️⃣ How production uses this (DVC)

In production metadata store (MLflow / DB):

```json
{
  "model_version": "fraud_model_v2",
  "git_commit": "a83bd9",
  "data_hash": "c91f2a",
  "dvc_remote": "s3://ml-dvc-store"
}
```

That's **full reproducibility**.

---

# PART B — DATA VERSIONING USING **AWS NATIVE TOOLS**

This is how **big enterprises** often do it.

### AWS Lake House Architecture
![AWS Lake House Implementation](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2021/07/22/Figure-2.-High-level-design-for-an-AWS-lake-house-implementation.png)

### AWS Data Pipeline Architecture
![AWS Data Pipeline](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2021/10/05/figure-1-3-1167x630.png)

### SageMaker ML Pipeline
![SageMaker Pipeline](https://d2908q01vomqb2.cloudfront.net/77de68daecd823babbb58edb1c8e14d7106e83bb/2020/02/04/Next-Caller-Amazon-SageMaker-1.png)

### End-to-End ML Workflow
![ML Workflow](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/10/22/ML-4030-image001.jpg)

---

## 8️⃣ AWS-native data versioning building blocks

| Layer    | AWS Tool                     |
| -------- | ---------------------------- |
| Raw data | **S3 (versioned buckets)**   |
| ETL      | **AWS Glue / EMR**           |
| Metadata | **Glue Data Catalog**        |
| Features | **SageMaker Feature Store**  |
| Models   | **SageMaker Model Registry** |
| Lineage  | **SageMaker Lineage**        |

---

## 9️⃣ Step-by-step AWS example (realistic)

### 🔹 Step 1: Enable S3 versioning (VERY IMPORTANT)

```bash
aws s3api put-bucket-versioning \
  --bucket my-datalake \
  --versioning-configuration Status=Enabled
```

Now:

```
transactions.csv
 ├── versionId: v1
 ├── versionId: v2
```

S3 **automatically versions raw data**.

---

### 🔹 Step 2: ETL using Glue

Glue job reads:

```
s3://my-datalake/raw/
```

Writes:

```
s3://my-datalake/processed/features/
```

Each run writes to a **new prefix**:

```
features/run_id=2024_01_01/
features/run_id=2024_01_02/
```

👉 This is **implicit data versioning**.

Glue Catalog stores schema + location.

---

### 🔹 Step 3: Feature Store (optional but powerful)

```python
feature_group_name = "fraud_features_v3"
```

Each feature group has:

* `creation_time`
* `record_identifier`
* `event_time`

SageMaker Feature Store **tracks versions automatically**.

---

### 🔹 Step 4: Model training in SageMaker

Training job metadata:

```json
{
  "training_job": "fraud-train-2024-01-02",
  "input_data": "s3://.../features/run_id=2024_01_02/",
  "feature_group": "fraud_features_v3"
}
```

This is stored in **SageMaker Lineage**.

---

### 🔹 Step 5: Register model

```bash
Model: fraud-model
Version: 4
Data location: s3://.../features/run_id=2024_01_02/
```

Now AWS knows:

```
Model v4 ← Feature run 2024_01_02 ← Raw S3 versions
```

---

## 10️⃣ How AWS answers "which data trained this model?"

Via:

* **Model Registry**
* **Lineage Graph**
* **S3 Version IDs**
* **Glue Catalog**

You can literally visualize:

```
Raw Data v12
   ↓
ETL Job run 98
   ↓
Feature Group v3
   ↓
Model v4
```

---

# PART C — DVC vs AWS Native (When to use what)

| Scenario              | Use            |
| --------------------- | -------------- |
| Startup / small team  | **DVC**        |
| Heavy AWS infra       | **AWS Native** |
| Git-centric workflows | **DVC**        |
| Compliance / audits   | **AWS Native** |
| Hybrid                | **DVC + S3**   |

💡 Many teams:

* Use **DVC for experimentation**
* Use **AWS native for production**

---

## 11️⃣ Mental model to remember forever

> **A model is useless without knowing the exact data that created it.**

Always store:

```
(model_version, data_version, code_version)
```

---

## 📚 Additional Resources

- [DVC Documentation](https://dvc.org/doc)
- [AWS SageMaker Lineage](https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html)
- [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html)
- [SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
- [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

---

**Made with ❤️ for reproducible ML**
