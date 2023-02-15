# Distributed Proxy crawler (POC)
This project is scaffolding for a distributed and proxied crawler system to be used for scraping.

This can theoretically scale to the number of good proxies available in the redis set

In this example we are using redis as a backbone for known proxies and (in the future) a worker.

To make this project more scalable, you could the worker with [aws sns](https://aws.amazon.com/sns/) that triggers an [aws Lambda](https://aws.amazon.com/lambda/) version of scraper.py


## Scope
This project is a basic scraper only with pure html (no JS rendering)

## Running
There are three moving parts to this project:
1. A job submission and status/dashboard UI (flask) at http://127.0.0.1:5001 (configure port in docker-compose.yml)
2. Proxy loader (scripts/load_proxies.sh) - This script should be run on a cron or triggered when the amount of available proxies < some number. 
3. Worker (scripts/run_worker.sh) - This script will run any enqueued jobs

### Startup
Make sure you have a virtual environment active.

**terminal 1** - build frontend, worker1 and run redis
```
$ docker-compose up --build
```
**terminal 2** - load proxies and test functionality
```
$ scripts/load_proxies.sh
```
### Use

Open a browser to http://127.0.0.1:5001 (configure port in docker-compose.yml) and use UI



## Free proxy Lists
https://free-proxy-list.net/
https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc


## Known TODOs
Below is a list of things that this project will strive to do in the near future.

1. Exclusive lock(s) for a proxy/move to IN_USE set
2. Add worker functionality of RQ/Celery/etc