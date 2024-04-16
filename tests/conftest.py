"""
conftest.py: sharing fixtures across multiple files

The conftest.py file serves as a means of providing fixtures for an entire directory.
Fixtures defined in a conftest.py can be used by any test in that package without needing
to import them (pytest will automatically discover them).

You can have multiple nested directories/packages containing your tests, and each directory
can have its own conftest.py with its own fixtures, adding on to the ones provided by the
conftest.py files in parent directories.
"""

import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as client:
        # Any setup code you want to run before the tests on the client goes here
        yield client
        # Any teardown code you want to run after the tests on the client goes here
