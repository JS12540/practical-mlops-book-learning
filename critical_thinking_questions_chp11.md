# Critical Thinking Discussion – Answers

---

## 1. Name 3 possible consequences of unauthenticated cloud functions

Unauthenticated cloud functions (publicly accessible without identity verification) can introduce serious risks:

### **a) Security Breaches & Data Exposure**
If a function is publicly callable, attackers may:
- Access sensitive data (PII, credentials, internal metadata)
- Trigger logic not meant for external users
- Exploit weak input validation

**Impact:** Data leaks, compliance violations (GDPR, HIPAA), reputational damage.

---

### **b) Abuse & Cost Explosion**
Malicious users or bots may:
- Spam requests (DDoS-like behavior)
- Trigger expensive compute operations
- Exploit pay-per-use billing models

**Impact:** Unexpected cloud bills, degraded performance, service disruption.

---

### **c) Unauthorized Actions**
Without authentication/authorization:
- Anyone can invoke state-changing operations
- Internal workflows may be triggered externally
- Business logic protections are bypassed

**Impact:** Fraud, data corruption, system instability.

---

## 2. What are some drawbacks of not using a virtual environment?

Skipping virtual environments leads to dependency and reproducibility issues:

### **a) Dependency Conflicts**
- Different projects may require incompatible library versions
- Global installs override each other

**Example:** Project A needs `numpy==1.21`, Project B needs `numpy==2.0`.

---

### **b) System Pollution**
- Global Python environment becomes cluttered
- Harder to debug which package is used

---

### **c) Non-Reproducible Builds**
- Teammates cannot recreate your setup reliably
- CI/CD pipelines may fail

---

### **d) Risk to System Python**
- Modifying OS-managed Python can break tools

---

## 3. Describe two aspects of good debugging techniques and why they are useful

### **a) Reproducibility**
Good debugging requires:
- Consistent reproduction of the issue
- Minimal test cases

**Why useful:**
- Isolates root cause
- Prevents chasing non-deterministic bugs

---

### **b) Observability (Logs & Instrumentation)**
- Structured logging
- Metrics & traces

**Why useful:**
- Reveals hidden runtime behavior
- Helps diagnose production issues

---

## 4. Why is knowing packaging useful? What are some critical aspects of packaging?

### **Why Packaging Matters**

Packaging enables:
- Distribution of software
- Version control
- Dependency management
- Reproducible installations

Without packaging, sharing and scaling software becomes chaotic.

---

### **Critical Aspects of Packaging**

### **a) Dependency Specification**
- `requirements.txt` / `pyproject.toml`
- Version pinning

---

### **b) Versioning**
- Semantic Versioning (SemVer)
- Backward compatibility

---

### **c) Metadata**
- Name, author, license, description

---

### **d) Build System**
- Wheel / source distribution
- Reproducible builds

---

### **e) Entry Points**
- CLI commands
- Plugin systems

---

## 5. Is it a good idea to use an existing model from a cloud provider? Why?

### **Advantages**

### **a) Faster Time to Market**
- No training required
- Ready-to-use APIs

---

### **b) Lower Infrastructure Burden**
- No GPU management
- Automatic scaling

---

### **c) Proven Performance**
- Pretrained on large datasets

---

### **d) Maintenance & Updates**
- Continuous improvements

---

### **Trade-offs / Risks**

### **a) Cost**
- API usage fees can scale rapidly

---

### **b) Vendor Lock-in**
- Harder to migrate later

---

### **c) Limited Customization**
- Black-box behavior

---

### **d) Data Privacy**
- Data sent to third-party services

---

### **Conclusion**
Using provider models is excellent for:
- MVPs
- Standard use cases

Custom models are better for:
- Specialized domains
- Competitive differentiation

---

## 6. Trade-offs: Public Container Registry vs PyPI for an Open-Source ML CLI Tool

---

### **Option 1: Public Container Registry (Docker Hub, GHCR, etc.)**

### **Pros**
- Fully reproducible runtime
- No dependency issues
- Works across platforms
- Easy onboarding (`docker run ...`)

---

### **Cons**
- Larger download size
- Requires Docker knowledge
- Less Python ecosystem integration
- Harder for pip-based workflows

---

### **Option 2: Python Package Repository (PyPI)**

### **Pros**
- Native Python integration
- Lightweight installs
- Familiar workflow (`pip install tool`)
- Easy updates

---

### **Cons**
- Dependency conflicts possible
- Platform-specific issues
- Reproducibility challenges
- Requires Python environment setup

---

## **Key Trade-off Dimensions**

| Dimension | Container Registry | PyPI |
|----------|-------------------|------|
| Reproducibility | Excellent | Moderate |
| Install Size | Large | Small |
| Ease for Python Devs | Moderate | Excellent |
| Cross-Platform Consistency | High | Variable |
| Dependency Issues | Minimal | Possible |
| DevOps / Infra Fit | Excellent | Moderate |

---

## **Best Practice Strategy**

Many successful tools offer **both**:

- **PyPI** → For Python developers
- **Docker Image** → For production / non-Python users

Example:
```

pip install mytool
docker run mytool

```

---

# Final Thoughts

These topics highlight core engineering principles:

- Security-first design
- Environment isolation
- Systematic debugging
- Proper packaging
- Pragmatic ML adoption
- Deployment strategy trade-offs

Mastering them significantly improves software reliability, scalability, and maintainability.
