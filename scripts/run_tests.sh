#!/bin/bash -ex
cd "$(dirname "$0")/.."
echo "pwd: $(pwd)"

export RECORD_MODE="none"


pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m black .
# venv/lib/python3.10/site-packages
vulture --exclude "venv/" --min-confidence 80 $(pwd)

pylint *.py

python3 -m pytest --cov=$(pwd)/scripts \
   --cov=$(pwd)/app --cov=$(pwd)/utils $CAPTURE -x -ra \
   -vv --cache-clear --no-cov-on-fail \
   --cov-fail-under=90 \
   --html=reports/unit_report.html \
   --self-contained-html \
   tests/