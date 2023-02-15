#!/bin/bash -x
cd "$(dirname "$0")/.."
echo "pwd: $(pwd)"

pip install -r requirements.txt

python3 -m scripts.load_proxies