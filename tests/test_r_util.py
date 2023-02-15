"""."""
import pytest
from utils import r_util

from pytest_redis import factories

redis_my = factories.redisdb("redis_nooproc")


def test_get_random_proxy(redis_my):  # pylint: disable=W0621
    """."""
    redis_my.sadd(r_util.UNCHECKED, "192.168.0.1")
    redis_my.sadd(r_util.WORKING, "192.168.0.2")

    assert r_util.get_random_proxy() in (b"192.168.0.1", b"192.168.0.2")


def test_get_random_proxy_exception(redis_my):  # pylint: disable=W0613,W0621
    """."""
    with pytest.raises(Exception):
        r_util.get_random_proxy()


def test_reset_proxy(redis_my):  # pylint: disable=W0613,W0621
    """."""
    ip_address = b"192.168.0.3"
    r_util.reset_proxy(ip_address=ip_address)
    assert ip_address in r_util.dash()[r_util.UNCHECKED]


def test_already_in_use(redis_my):  # pylint: disable=W0613,W0621
    """."""
    ip_address = b"192.168.0.4"
    r_util.already_in_use(ip_address)


def test_add_proxy_ip_not_already_in_use(redis_my):  # pylint: disable=W0613,W0621
    """."""
    ip_address = b"192.168.0.5"
    r_util.add_proxy_ip(ip_address)
