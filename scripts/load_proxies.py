"""This is meant to run on a cron, see scripts/load_proxies.sh

Fetch the list of proxies and add them to the redis list for "unchecked"
."""
import json
import logging
import pprint
import requests

from utils import r_util
from utils import scraper

pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)

CHECK_ADDR = "http://ident.me/"
MY_IP = requests.get(CHECK_ADDR)
logger.info("my_ip: %s", MY_IP)
ACCEPTED_CODES = [200, 301, 302, 307]


class UnsupportedList(Exception):
    """."""


def check_proxy(proxy):
    """."""
    assert proxy
    logger.info("Checking `%s`...", proxy)
    result = None
    proxy_used = None
    try:
        result, proxy_used = scraper.get(
            CHECK_ADDR, proxy=proxy, timeout=30, retry=False
        )
    except (
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ProxyError,
    ) as err:
        logger.warning("%s: %s", proxy, err)
        return False

    if result and "<body>" in result.text:
        logger.warning("Proxy returned html when ip string was expected")
        return False

    if result and result.status_code in ACCEPTED_CODES and result.text != MY_IP.text:
        logger.debug(
            "%s via %s returned %s (%s) - my ip = %s",
            CHECK_ADDR,
            proxy_used,
            result.text,
            result.status_code,
            MY_IP.text,
        )
        return True
    return False


def load_json_list(proxy_def, proxy_limit=None):
    """."""
    res = requests.get(proxy_def["url"]).json()[proxy_def["container"]]
    logger.debug(pprint.pformat(res))
    added = 0
    for idx, proxy in enumerate(res):
        # pp.pprint(proxy)
        p_ip = proxy[proxy_def["ip"]]
        port = proxy[proxy_def["port"]]
        proto = proxy[proxy_def["proto"]]
        if isinstance(proto, list):
            proto = proto[0]
        info = f"{proto}://{p_ip}:{port}"
        logger.info("%s/%s -> %s", idx, proxy_limit, info)
        if check_proxy(info):
            logger.info("! add %s", info)
            r_util.add_proxy_ip(info)
            added += 1
        else:
            logger.warning("%s failed check", info)

        if proxy_limit and idx > proxy_limit:
            logger.info("hit proxy_limit of %s", proxy_limit)
            break
    logger.info("added %s with limit of %s", added, proxy_limit)


def fetch_lists(proxy_limit=None, limit=None):
    """."""
    with open("config/known_proxy_lists.json", encoding="utf-8") as f_obj:
        proxy_list = json.load(f_obj)
        logger.info(pprint.pformat(proxy_list))

        for idx, proxy in enumerate(proxy_list):
            logger.info("%s/%s --> %s", idx, limit, proxy)
            if proxy["type"] == "json":
                load_json_list(proxy, proxy_limit=proxy_limit)
                logger.info("%s/%s lists", idx, limit)
                # TODO: when we need to limit num of proxy lists
                # if limit and idx > limit:
                #     break
            else:
                raise UnsupportedList(f"list type {proxy['type']}, not supported")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        force=True,
        format="[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    )
    fetch_lists()
