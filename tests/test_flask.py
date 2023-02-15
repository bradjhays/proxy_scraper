"""."""
import pytest
from app import app


@pytest.fixture
def client():
    """Configures the app for testing"""

    app.config["TESTING"] = True
    app_client = app.test_client()

    yield app_client


def test_home(client):  # pylint: disable=W0621
    """."""
    landing = client.get("/")
    html = landing.data.decode()
    assert "count_not_working" in html


def test_submit_urls(client):  # pylint: disable=W0621
    """."""
    landing = client.post("/submit_urls", data={"urls": "127.0.0.1\n192.168.1.1"})
    html = landing.data.decode()
    assert "{'127.0.0.1': 1, '192.168.1.1': 1}" in html
