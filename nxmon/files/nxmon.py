#!/usr/bin/env python3
import subprocess
import time

from prometheus_client import CollectorRegistry, write_to_textfile
from prometheus_client import Gauge

NGINX_PATH = "/usr/sbin/nginx"

# prepare Prometheus metrics
registry = CollectorRegistry()
nginx_config_status = Gauge(
    "nginx_config_status", "Nginx Config Status", registry=registry)
nginx_config_status_time = Gauge(
    "nginx_config_status_time_seconds", "Time to run nginx -t",
    registry=registry)


def main():
    start = time.time()
    status = subprocess.call([NGINX_PATH, "-t"])
    end = time.time()
    nginx_config_status.set(status)
    nginx_config_status_time.set(end - start)
    write_to_textfile('/var/lib/node_exporter/nxmon.prom', registry)


if __name__ == "__main__":
    main()
