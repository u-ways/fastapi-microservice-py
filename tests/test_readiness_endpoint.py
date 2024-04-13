import unittest

from httpx import Response
from starlette.testclient import TestClient

from main import app


class ReadinessTest(unittest.TestCase):
    @staticmethod
    def given_a_request() -> Response:
        return TestClient(app).get("/")

    def test_should_return_200(self):
        self.assertTrue(self.given_a_request().is_success)

    def test_should_return_empty_body(self):
        self.assertEqual("null", self.given_a_request().text)


if __name__ == "__main__":
    unittest.main()
