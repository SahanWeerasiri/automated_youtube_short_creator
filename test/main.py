from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/venom-445906"

# List time series data for API requests
results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type="aiplatform.googleapis.com/request_count"',
        "interval": {"seconds": 86400},  # Last 24 hours
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)

for result in results:
    print(result)