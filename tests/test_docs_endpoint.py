import pytest
from httpx import Response

from .utils import given_a_request


@pytest.fixture
def response(client, request) -> Response:
    endpoint = request.param
    return given_a_request(client, endpoint)


@pytest.mark.parametrize("response", ["docs", "redoc"], indirect=True)
def test_should_return_200(response):
    assert response.is_success, "Should return a 200 success status"


@pytest.mark.parametrize("response", ["docs", "redoc"], indirect=True)
def test_should_return_html(response):
    assert response.headers["content-type"].startswith("text/html"), "Content type should be HTML"


@pytest.mark.parametrize("response", ["openapi.json"], indirect=True)
def test_should_expose_openapi_json(response):
    assert response.status_code == 200, "Should return a 200 success status for OpenAPI JSON"
    assert response.headers["content-type"].startswith("application/json"), "Content type should be JSON"
    assert "openapi" in response.json(), "Response JSON should contain 'openapi' field"
