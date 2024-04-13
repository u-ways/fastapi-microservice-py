import unittest

from httpx import Response
from starlette.testclient import TestClient

from main import app


class MetricsTest(unittest.TestCase):
    client: TestClient

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        # Trigger startup event as the instrumentator activates on startup
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        # Trigger shutdown event so the instrumentator can clean up
        cls.client.__exit__(None, None, None)

    def given_a_request(self) -> Response:
        return self.client.get("/metrics")

    def test_should_return_200(self):
        self.assertTrue(self.given_a_request().is_success)

    def test_should_return_metrics(self):
        self.assertTrue(self.given_a_request().text.startswith("# HELP"))

    def test_should_expose_startup_time_metric(self):
        response = self.given_a_request()
        self.assertIn("process_start_time_seconds", response.text)

    def test_should_expose_cpu_metrics(self):
        response = self.given_a_request()
        self.assertIn("process_cpu_seconds_total", response.text)
        self.assertIn("process_start_time_seconds", response.text)

    def test_should_expose_memory_metrics(self):
        response = self.given_a_request()
        self.assertIn("process_virtual_memory_bytes", response.text)
        self.assertIn("process_resident_memory_bytes", response.text)

    def test_should_expose_gc_metrics(self):
        response = self.given_a_request()
        self.assertIn("python_gc_objects_collected_total", response.text)
        self.assertIn("python_gc_objects_uncollectable_total", response.text)
        self.assertIn("python_gc_collections_total", response.text)

    def test_should_expose_request_metrics(self):
        response = self.given_a_request()
        self.assertIn("http_request_duration_seconds", response.text)
        self.assertIn("http_requests_total", response.text)


if __name__ == "__main__":
    unittest.main()
