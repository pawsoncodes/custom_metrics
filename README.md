
# Datadog Custom Metrics Example

This repository provides multiple examples and best practices for sending custom metrics to Datadog using the latest API methods and DogStatsD. These examples demonstrate how to track application-specific data like custom performance metrics, latency, and business metrics in a scalable way.

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Sending Custom Metrics via Datadog API](#sending-custom-metrics-via-datadog-api)
- [Sending Custom Metrics via DogStatsD](#sending-custom-metrics-via-dogstatsd)
- [Best Practices](#best-practices)
  - [Cost and Billing Considerations](#cost-and-billing-considerations)
  - [Tagging and Metric Naming](#tagging-and-metric-naming)

---

## Overview

Custom metrics in Datadog allow you to track data points that are not covered by default integrations. For example, you can track:
- The number of API requests to a service
- Latency or processing time of critical operations
- Business metrics such as revenue, sign-ups, or specific user actions

This repository provides examples on how to:
1. Submit custom metrics using the latest **Datadog API v2**.
2. Submit custom metrics using **DogStatsD**, a lightweight, UDP-based protocol for high-performance applications.

---

## Setup

### Prerequisites
- A Datadog account: [Sign Up Here](https://www.datadoghq.com/)
- Python 3.6+ installed on your machine
- Your Datadog **API Key**

### Step 1: Install Dependencies

Clone this repository and install the required Python packages:

```bash
git clone https://github.com/yourusername/datadog-custom-metrics-example.git
cd datadog-custom-metrics-example
pip install -r requirements.txt
```

The `requirements.txt` file includes:
```bash
datadog-api-client
datadog
```

### Step 2: Configure Your Datadog API Key

Make sure you have your Datadog **API Key** available. You can set it as an environment variable before running the examples:

```bash
export DATADOG_API_KEY=your_datadog_api_key
```

Alternatively, you can pass the API key directly in your code, as demonstrated in the examples.

---

## Sending Custom Metrics via Datadog API

The latest Datadog API v2 provides a robust, modern interface for sending custom metrics. Below is an example of how to submit a custom metric using the API.

### Example: Submitting a Custom Metric via API

```python
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries

# Configure the Datadog API client
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)

    # Define the metric payload
    body = MetricPayload(
        series=[
            MetricSeries(
                metric="custom.myapp.requests",
                type=MetricIntakeType.GAUGE,
                points=[
                    MetricPoint(
                        timestamp=int(datetime.now().timestamp()),
                        value=150.0,
                    ),
                ],
                tags=["env:prod", "service:webapp"],
            ),
        ],
    )

    # Submit the metric
    response = api_instance.submit_metrics(body=body)
    print(response)
```

### Example: Submitting a Histogram Metric via API

```python
from datetime import datetime
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries

# Configure the API client
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)

    # Define the histogram metric payload
    body = MetricPayload(
        series=[
            MetricSeries(
                metric="custom.myapp.response_time",
                points=[
                    MetricPoint(
                        timestamp=int(datetime.now().timestamp()),
                        value=350.0,  # Response time in ms
                    ),
                ],
                tags=["env:staging", "endpoint:/api"],
            ),
        ],
    )

    # Submit the metric
    response = api_instance.submit_metrics(body=body)
    print(response)
```

---

## Sending Custom Metrics via DogStatsD

DogStatsD is an efficient, UDP-based solution for high-performance applications. Metrics are collected via the Datadog agent. 

### Example: Submitting Metrics via DogStatsD

```python
from datadog import DogStatsd

# Initialize DogStatsd client
statsd = DogStatsd()

# Submit a gauge metric
statsd.gauge('myapp.cpu_load', 75.5, tags=["env:prod", "host:webserver"])

# Increment a counter
statsd.increment('myapp.request_count', tags=["env:prod", "endpoint:/api"])

print("Metrics sent via DogStatsD!")
```

---

## Best Practices

### Cost and Billing Considerations

Custom metrics are counted towards your Datadog usage, so it’s important to keep an eye on how many you send. Here are some **best practices** to reduce cost while still getting valuable insights:

1. **Metric Cardinality**:
   - **Cardinality** refers to the number of unique combinations of metric names and tags. The higher the cardinality, the more expensive your monitoring setup becomes.
   - **Reduce Tags**: Limit the number of tags you use on each metric. For example, avoid adding too many dimensions (like unique user IDs) unless absolutely necessary.

2. **Use Distribution Metrics**:
   - For high-cardinality metrics, consider using **distribution metrics**, which provide statistical summaries across different hosts and services without exploding the number of unique timeseries.
   
3. **Set Custom Metric Alerts**:
   - Set up alerts to notify you when you are approaching your custom metric limits. You can monitor your custom metric count using Datadog's **usage metrics** (`datadog.custom_metric.count`).
   
4. **Aggregate at the Application Level**:
   - Instead of sending raw data every second, consider aggregating data on your application side (for example, compute the average, min, or max over a 10-second period) and send those values as custom metrics. This reduces the number of data points you submit.

### Tagging and Metric Naming

- **Use Consistent Naming Conventions**: Always prefix your custom metrics with your application name (e.g., `myapp.`) to make them easier to search and manage.
- **Tagging Best Practices**:
  - Use tags for important attributes like `env`, `service`, and `host`.
  - Avoid over-tagging to keep metric cardinality low.

---

## License

This repository is licensed under the MIT License.
