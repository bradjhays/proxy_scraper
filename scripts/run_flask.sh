#!/bin/sh

while true; do
    pip install -r requirements.txt
    python flask_app.py
    echo "flask died... wait 10 sec for restart"
    sleep 10
done
