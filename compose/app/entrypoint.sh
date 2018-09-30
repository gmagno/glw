#!/usr/bin/env bash
sleep 4
cd /code/app && gunicorn -w 1 -b 0.0.0.0:60010 --preload app:application &
sleep 2
cd /code/ui && python3 -m http.server 60030 &
sleep 2
cd /code/ && pytest -p no:sugar test/
# sleep 2
# cd /code/report && python3 -m http.server 60040
