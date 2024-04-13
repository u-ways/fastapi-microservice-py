import unittest

from httpx import Response
from parameterized import parameterized
from starlette.testclient import TestClient

from main import app


class DocsTest(unittest.TestCase):
    @staticmethod
    def given_a_request(endpoint) -> Response:
        return TestClient(app).get(endpoint)

    @parameterized.expand([("docs",), ("redoc",)])
    def test_should_return_200(self, endpoint):
        self.assertTrue(self.given_a_request(endpoint).is_success)

    @parameterized.expand([("docs",), ("redoc",)])
    def test_should_return_html(self, endpoint):
        response = self.given_a_request(endpoint)
        self.assertTrue(response.headers["content-type"].startswith("text/html"))

    def test_should_expose_openapi_json(self):
        response = self.given_a_request("/openapi.json")
        self.assertTrue(response.is_success)
        self.assertTrue(response.headers["content-type"].startswith("application/json"))
        self.assertTrue(response.json().get("openapi"))


if __name__ == "__main__":
    unittest.main()
