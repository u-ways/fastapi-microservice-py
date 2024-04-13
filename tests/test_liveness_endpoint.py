import unittest

from httpx import Response
from starlette.testclient import TestClient

from main import app
from model.state import State
from model.status import Status


class LivenessTest(unittest.TestCase):
    @staticmethod
    def given_a_request() -> Response:
        return TestClient(app).get("/health")

    def test_should_return_200(self):
        self.assertTrue(self.given_a_request().is_success)

    def test_should_return_status_model(self):
        expected_status = Status(status=State.UP, message="Service is healthy.")
        actual_status = Status(**self.given_a_request().json())
        self.assertEqual(expected_status, actual_status)


if __name__ == "__main__":
    unittest.main()
