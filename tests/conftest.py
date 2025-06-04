import os
import dotenv
import pytest

APP_URL = "APP_URL"
@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture
def app_url():
    return os.getenv(APP_URL)