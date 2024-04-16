import pytest
from httpx import Response

from .utils import given_a_request


@pytest.fixture(autouse=True)
def response(client) -> Response:
    return given_a_request(client, "/metrics")


def test_should_return_200(response):
    assert response.is_success


def test_should_return_metrics(response):
    assert response.text.startswith("# HELP")


def test_should_expose_startup_time_metric(response):
    assert "process_start_time_seconds" in response.text


def test_should_expose_cpu_metrics(response):
    assert "process_cpu_seconds_total" in response.text
    assert "process_start_time_seconds" in response.text


def test_should_expose_memory_metrics(response):
    assert "process_virtual_memory_bytes" in response.text
    assert "process_resident_memory_bytes" in response.text


def test_should_expose_gc_metrics(response):
    assert "python_gc_objects_collected_total" in response.text
    assert "python_gc_objects_uncollectable_total" in response.text
    assert "python_gc_collections_total" in response.text


def test_should_expose_request_metrics(response):
    assert "http_request_duration_seconds" in response.text
    assert "http_requests_total" in response.text
