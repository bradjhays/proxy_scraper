"""."""
import logging
from unittest import mock

import requests
import pytest

from utils import scraper
from conftest import my_vcr
from tests import mockers

logger = logging.getLogger(__name__)


@my_vcr.use_cassette
def test_scraper_get_default_timeout():
    """."""
    url = "http://www.google.com"
    with pytest.raises(Exception):
        scraper.get(url=url, proxy=None, retry=0, timeout=None)


@my_vcr.use_cassette
def test_process_url():
    """."""
    url = "http://www.google.com"
    with pytest.raises(Exception):
        scraper.process_url(url)


@my_vcr.use_cassette
def test_detect_public_ip():
    """."""
    assert scraper.detect_public_ip() == "127.0.0.1"


@mock.patch("requests.get", side_effect=mockers.mocked_requests_get)
def test_scraper_not_proxied(_mocked_requests):
    """."""
    url = "http://not_proxied.com"
    with pytest.raises(scraper.InvalidProxyException):
        scraper.get(url=url, proxy="127.0.0.1", retry=0, timeout=None)


@mock.patch("requests.get", side_effect=mockers.mocked_requests_get)
def test_scraper_not_invalid_status_code(_mocked_requests):
    """."""
    url = "http://bad.status_code.com"
    res, addr = scraper.get(url=url, proxy="127.0.0.1", retry=0, timeout=None)
    assert res.status_code == 500
    assert addr == "127.0.0.1"


@mock.patch(
    "requests.get",
    side_effect=requests.exceptions.ProxyError("boom"),
)
def test_scraper_get_proxy_error(_mocked_requests):
    """."""
    url = "http://www.google.com"
    with pytest.raises(requests.exceptions.ProxyError):
        scraper.get(url=url, proxy="127.0.0.1", retry=0, timeout=None)
