"""."""
import os
from functools import lru_cache
import logging
import pprint
import requests

from utils import r_util as r

pp = pprint.PrettyPrinter(indent=4)
VALID_STATUSES = [200, 301, 302, 307, 404]
# session = requests.Session()
MAX_RETRY = int(os.getenv("MAX_RETRY", "5"))
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
logger = logging.getLogger(__name__)


@lru_cache
def detect_public_ip():
    """."""
    try:
        res = requests.get("http://ident.me/")
        answer = res.text
    except Exception as err:  # pylint: disable=W0703
        return f"Error: {err}"
    else:
        return answer


class InvalidProxyException(Exception):
    """."""


def get(url, proxy=None, retry=0, timeout=None):
    """."""
    if not timeout:
        timeout = TIMEOUT
    if not proxy:
        logger.debug("fetching random proxy")
        proxy = r.get_random_proxy()

    logger.info("using proxy %s", proxy)
    assert proxy, "failed to get a proxy"
    try:
        d_proxy = proxy.decode("utf-8")
    except AttributeError:
        d_proxy = proxy
    logger.info("using d_proxy %s", d_proxy)
    try:
        proto = "http"
        if "https://" in d_proxy:
            proto = "https"
        logger.info("get with requests")
        res = requests.get(
            url,
            proxies={proto: d_proxy},
            timeout=timeout,
            allow_redirects=True,
            stream=True,
        )
        # Check that the proxy actually forwarded the request
        logger.info("have a response")
        try:
            orig_resp = res.raw._original_response  # pylint: disable=W0212
            r_ip = orig_resp.fp.raw._sock.getpeername()[0]  # pylint: disable=W0212
            logger.info(r_ip)
        except AttributeError as err:
            if not hasattr(res, "raw"):
                logger.info(pprint.pformat(res.__dict__))
            else:
                logger.info(pprint.pformat(orig_resp.__dict__))
            logger.warning(err)
            r_ip = None

        logger.info("proxy work? %s =? %s", r_ip, d_proxy)
        if r_ip == d_proxy:
            r.set_not_working(proxy)
            raise InvalidProxyException(f"proxy {d_proxy} did not proxy request")
        if res.status_code in VALID_STATUSES:
            r.set_working(proxy)
        else:
            r.set_not_working(proxy)

        return res, d_proxy
    except (
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ProxyError,
    ) as err:
        r.set_not_working(proxy)
        print(f"!ERR({retry}): {err}")
        if not retry or retry > MAX_RETRY:
            raise
        return get(url)


def process_url(url):
    """async handle crawl, and put it somewhere."""
    logger.info("Process %s", url)
    res, proxy_used = get(url, retry=2)
    print(
        f"{url} via '{proxy_used} returned {res.text} ({res.status_code}) - my ip = {detect_public_ip()}"
    )
    return res
