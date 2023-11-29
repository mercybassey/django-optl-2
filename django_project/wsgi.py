import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from django.core.wsgi import get_wsgi_application


# WSGI application setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Common resource for and traces
resource = Resource(attributes={SERVICE_NAME: "django-notes-app"})

# Setup for tracing
trace_exporter = OTLPSpanExporter(endpoint="http://opentelemetry-collector:4317")
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)

# Custom Formatter for logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.trace_id = getattr(record, "otelTraceID", "N/A")
        record.span_id = getattr(record, "otelSpanID", "N/A")
        record.service_name = getattr(record, "otelServiceName", "N/A")
        return super().format(record)

# Configure logging with custom formatter
log_handler = logging.StreamHandler()
log_handler.setFormatter(CustomFormatter('%(asctime)s trace_id=%(trace_id)s span_id=%(span_id)s %(levelname)s %(name)s %(message)s service_name=%(service_name)s'))
logging.basicConfig(level=logging.INFO, handlers=[log_handler])

LoggingInstrumentor().instrument(set_logging_format=True, log_level=logging.INFO)

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)



