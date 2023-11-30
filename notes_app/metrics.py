from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource  

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

# Define a counter for request counts
request_count = meter.create_counter(
    name="request_count",
    description="Counts the number of requests received",
    unit="1"  
)




