"""."""
from unittest import mock

from pytest_redis import factories
import pytest

from conftest import my_vcr
from scripts import load_proxies
from utils import r_util
from tests import mockers


redis_my = factories.redisdb("redis_nooproc")


@my_vcr.use_cassette
def test_load_proxy(redis_my):  # pylint: disable=W0613, W0621
    """."""
    load_proxies.fetch_lists(proxy_limit=3)
    assert b"http://188.133.136.105:1256" in r_util.dash()[r_util.WORKING]


@mock.patch("json.load", return_value=[{"type": "unsupported"}])
def test_load_proxy_unsupported(_mocked_json_load):
    """."""
    with pytest.raises(load_proxies.UnsupportedList):
        load_proxies.fetch_lists(proxy_limit=3)


def test_check_proxy_exception():
    """."""
    assert not load_proxies.check_proxy(proxy="http://c.nowhere")


@mock.patch("requests.get", side_effect=mockers.mocked_requests_get)
def test_check_proxy_false(_mock_get):  # pylint: disable=W0613
    """."""
    assert not load_proxies.check_proxy(proxy="wont_work")


@mock.patch("requests.get", side_effect=mockers.mocked_requests_get)
def test_load_json_list(_mock_get, redis_my):  # pylint: disable=W0613, W0621
    """."""
    load_proxies.load_json_list(
        proxy_def={"url": "http://someurl.com/test.json", "container": "key1"}
    )


@mock.patch("requests.get", side_effect=mockers.mocked_requests_get)
def test_load_json_list_return_proto_string(
    _mock_get, redis_my
):  # pylint: disable=W0613, W0621
    """."""
    load_proxies.load_json_list(
        proxy_def={
            "url": "http://someurl2.com/test.json",
            "container": "key1",
            "ip": "ip",
            "port": "port",
            "proto": "protocols",
        }
    )
