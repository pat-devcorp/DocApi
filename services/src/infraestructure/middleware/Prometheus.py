from prometheus_client import REGISTRY, Counter, Histogram, generate_latest

# from prometheus_client.exposition import make_wsgi_app


class Prometheus:
    def __init__(self, app):
        self.app = app
        self.request_counter = Counter(
            "flask_requests_total", "Total number of requests received"
        )
        self.request_duration = Histogram(
            "flask_request_duration_seconds", "Request duration in seconds"
        )

    def __call__(self, environ, start_response):
        # Increment request counter
        self.request_counter.inc()

        # Measure request duration
        with self.request_duration.time():
            response = self.app(environ, start_response)

        return response

    def get_metricts():
        return generate_latest(REGISTRY)
