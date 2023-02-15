"""Redis util

Manages 3 redis sets:
 - unchecked - proxy ips that have not been used
 - working - proxy ip that have worked
 - not_working - black listed

"""
import os
import logging

import random
from redis import Redis

REDIS_CONN = None
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

UNCHECKED = "unchecked"
WORKING = "working"
NOT_WORKING = "not_working"


def get_redis_addr():
    """."""
    return os.getenv("REDIS_HOST", "localhost")


def get_redis_connection():
    """."""
    global REDIS_CONN
    if not REDIS_CONN:
        REDIS_CONN = Redis(host=get_redis_addr(), port=6379)
        if not REDIS_CONN:
            raise Exception(f"Couldn't reach redis at {get_redis_addr()}:6379")
    return REDIS_CONN


def get_random_proxy():
    """create a tuple from unchecked and working sets."""

    available_proxies = tuple()
    for rset in (UNCHECKED, WORKING):
        val = get_redis_connection().srandmember(rset)
        logger.info("%s: %s", rset, val)
        if val:
            available_proxies += (val,)
    logger.info(available_proxies)
    if not available_proxies:
        raise Exception("no proxies available")
    logger.info(available_proxies)
    return random.choice(available_proxies)


def already_in_use(ip_address):
    """."""
    for l_name in (UNCHECKED, WORKING, NOT_WORKING):
        if get_redis_connection().sismember(l_name, ip_address):
            logger.info("'%s' set has %s", l_name, ip_address)
            return True
    logger.info("%s not in use", ip_address)
    return False


def add_proxy_ip(ip_address):
    """."""
    if not already_in_use(ip_address):
        reset_proxy(ip_address)
    else:
        logger.info("already in use")


def dash():
    """values for dashboard."""
    ret = {}
    for l_name in (UNCHECKED, WORKING, NOT_WORKING):
        ret[l_name] = list(get_redis_connection().smembers(l_name))
        ret[f"count_{l_name}"] = get_redis_connection().scard(l_name)
    return ret


def reset_proxy(ip_address):
    """."""
    logger.info("Resetting %s", ip_address)
    # add to the unchecked
    get_redis_connection().sadd(UNCHECKED, ip_address)
    # remove from others, if present
    for l_name in (WORKING, NOT_WORKING):
        get_redis_connection().srem(l_name, ip_address)


def set_working(ip_address):
    """."""
    logger.info("Set %s as working", ip_address)
    # add to the working set
    get_redis_connection().sadd(WORKING, ip_address)
    # remove from others, if present
    for l_name in (UNCHECKED, NOT_WORKING):
        get_redis_connection().srem(l_name, ip_address)


def set_not_working(ip_address):
    """."""
    logger.info("Set %s as NOT working", ip_address)
    # add to the not_working set
    get_redis_connection().sadd(NOT_WORKING, ip_address)
    # remove from others, if present
    for l_name in (UNCHECKED, WORKING):
        get_redis_connection().srem(l_name, ip_address)
