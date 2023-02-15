"""."""

import os
import logging
import vcr

BASE_DIR = os.path.dirname(__file__)
my_vcr = vcr.VCR(
    cassette_library_dir=f"{BASE_DIR}/cassettes",
    record_mode=os.getenv(
        "RECORD_MODE", "new_episodes"
    ),  # https://vcrpy.readthedocs.io/en/latest/usage.html#record-modes
    decode_compressed_response=True,
    filter_headers=[("X-Shopify-Access-Token", None)],
)

logging.basicConfig(
    level=logging.INFO,
    force=True,
    format="[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
)
logging.getLogger("vcr.cassette").setLevel(logging.ERROR)
logging.info("VCR: %s", my_vcr)
print(f"VCR: {my_vcr.record_mode}")
