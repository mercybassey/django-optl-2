from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource  
import logging

# Define a Resource with a service name
resource = Resource(attributes={"service.name": "django-notes-app"})

# Create OTLP exporter
otlp_exporter = OTLPMetricExporter(
    endpoint="http://opentelemetry-collector:4317",
    insecure=True
)

# Set up MeterProvider with OTLP exporter
meter_provider = MeterProvider(resource=resource, metric_readers=[PeriodicExportingMetricReader(exporter=otlp_exporter)])
metrics.set_meter_provider(meter_provider)

# Get a meter
meter = metrics.get_meter(__name__)

# Define metrics
response_times = meter.create_histogram("response_times", description="Response times of Django views")






