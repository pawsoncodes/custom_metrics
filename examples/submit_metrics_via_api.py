
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries

# Create a Configuration object with the API key explicitly set
configuration = Configuration(
    api_key={'apiKeyAuth': 'your_api_key'}  # Add your API key here
)

# Create a Guage metric
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)

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

    response = api_instance.submit_metrics(body=body)
    print(response)
