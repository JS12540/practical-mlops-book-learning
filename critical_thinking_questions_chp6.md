# Critical Thinking Discussion Questions

## Why might it be desirable to log to multiple sources at the same time?

Logging to multiple sources (also called *multi-destination logging*) is desirable because it improves **reliability, observability, and usability** of system diagnostics.

1. **Redundancy and fault tolerance**  
   If one logging destination fails (e.g., a disk fills up or a log server is unreachable), other destinations can still capture critical information. This ensures logs are not lost during failures.

2. **Different audiences and use cases**  
   - Developers may want logs written locally to files for debugging.
   - Operations teams may want logs streamed to centralized log management systems (e.g., ELK, Splunk) for monitoring and alerting.
   - Security teams may require logs sent to immutable storage for auditing and compliance.

3. **Real-time monitoring and long-term storage**  
   Logs can be sent simultaneously to:
   - A console or dashboard for real-time visibility.
   - A persistent storage system for historical analysis and post-incident forensics.

4. **Scalability in distributed systems**  
   In microservices or cloud environments, logging to a centralized system while also keeping local logs helps correlate events across services while retaining service-level detail.

---

## Why is it critical to monitor data drift?

Monitoring data drift is critical because machine learning models and data-driven systems **assume that future data behaves similarly to training data**—an assumption that often breaks over time.

1. **Model performance degradation**  
   When input data distributions change (feature drift) or the relationship between inputs and outputs changes (concept drift), model predictions become less accurate.

2. **Silent failures**  
   Data drift often occurs gradually and does not trigger obvious system errors. Without monitoring, models may continue running while producing increasingly incorrect results.

3. **Business and operational risk**  
   In domains like finance, healthcare, or fraud detection, undetected drift can lead to:
   - Incorrect decisions
   - Financial loss
   - Compliance or regulatory issues

4. **Early detection enables corrective action**  
   Monitoring allows teams to:
   - Retrain models
   - Adjust features
   - Update thresholds or rules  
   before major failures occur.

5. **Trust and accountability**  
   Continuous monitoring helps maintain stakeholder trust by ensuring the system remains reliable and explainable over time.

---

## Name three advantages of using logging facilities versus `print()` or `echo` statements

1. **Log levels and filtering**  
   Logging frameworks support severity levels (e.g., DEBUG, INFO, ERROR), allowing teams to control verbosity without changing code. `print()` statements lack this flexibility.

2. **Structured and consistent output**  
   Logs can include timestamps, severity levels, thread IDs, request IDs, and metadata in a standardized format, making them easier to parse and analyze automatically.

3. **Multiple outputs and integrations**  
   Logging systems can write to files, consoles, remote servers, or monitoring tools simultaneously. `print()` and `echo` are usually limited to standard output.

Additional advantages include better performance, asynchronous logging, log rotation, and improved maintainability in production systems.

---

## List the five most common log levels, from least to most verbose

From **least verbose (most severe)** to **most verbose (most detailed)**:

1. **ERROR** – Serious problems that prevent part of the system from functioning correctly  
2. **WARN** – Potential issues or unusual situations that are not yet errors  
3. **INFO** – High-level information about normal system operations  
4. **DEBUG** – Detailed information useful for debugging during development  
5. **TRACE** – Extremely fine-grained details, often showing every step of execution  

---

## What are three common metric types found in metric-capturing systems?

1. **Counters**  
   - Track the number of times an event occurs  
   - Examples: number of requests, errors, or transactions  
   - Values only increase (or reset)

2. **Gauges**  
   - Represent a value at a specific point in time  
   - Examples: memory usage, CPU utilization, queue size  
   - Values can increase or decrease

3. **Histograms (or Summaries)**  
   - Capture the distribution of values over time  
   - Examples: request latency, response size  
   - Useful for percentiles (e.g., p95, p99) and performance analysis  

---

