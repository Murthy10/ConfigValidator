import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def path():
    directory, _ = os.path.split(os.path.abspath(__file__))
    return directory + '/'
