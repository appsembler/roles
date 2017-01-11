#!/usr/bin/env python

from copy import deepcopy
import datetime
import hashlib
import json
import logging
import re
from subprocess import Popen, PIPE
import sys

from pygerduty import PagerDuty


START_TIME = datetime.datetime.utcnow()

# Log example:
# 01/09-20:42:02.184887  [**] [1:20000:0] ICMP Packet found [**] [Priority: 0] {ICMP} 10.128.0.3 -> 10.128.0.2
LOG_FORMAT = r"""
             (?P<timestamp>\d+/\d+-\d+:\d+:\d+\.\d+)\s+
             \[\*\*\]\s+
             \[(?P<gid>\d+):(?P<sid>\d+):(?P<rev>\d+)\]\s+
             (?P<message>[\w\s!@#$%\^&\*()+=;\'",.?~`/]+)\s+
             \[\*\*\]\s+
             \[Priority:\s+(?P<priority>\d+)\]\s+
             \{(?P<protocol>\w+)\}\s+
             (?P<src>\d+\.\d+\.\d+\.\d+(:\d+)?)\s+
             ->\s+
             (?P<dest>\d+\.\d+\.\d+\.\d+(:\d+)?)
             """

DEFAULT_CONFIG = {
    'snort_log_path': '/var/log/snort/alert',
    'snort_log_format': LOG_FORMAT,
    'snort_alert_priority': 2,
    'pagerduty_subdomain': 'example',
    'pagerduty_api_token': '',
    'pagerduty_service_key': '',
}


def read_logs(log_path):
    """Tail a log file and yield lines from it"""

    p = Popen(['tail', '-F', log_path], stdout=PIPE)
    while True:
        yield p.stdout.readline()


def parse_log(log, log_format):
    """Parse a log line into a dict using a regex"""

    pattern = re.compile(log_format, re.VERBOSE)
    match = pattern.match(log)

    if not match:
        msg = 'Log entry did match our pattern: {}'.format(log)
        logging.warning(msg)
        return None

    fields = {}
    for field in pattern.groupindex.keys():
        fields[field] = match.group(field)

    return fields


def check_timestamp(snort_timestamp, date):
    """Check whether the Snort timestamp is later than the given date"""

    return snort_timestamp > date.strftime('%m/%d-%H:%M:%S.%f')


def get_incident_key(log, fields):
    """Compute a key based on a hash of the log entry."""

    # Prevent duplicate alerts in the same day
    data = ''.join(log[field] for field in fields)
    data += datetime.datetime.utcnow().strftime('%Y-%j')
    return hashlib.sha256(data).hexdigest()


def wait_for_alerts(pager, config):
    """Monitor a log file and send PagerDuty alerts"""

    log_path = config['snort_log_path']
    log_format = config['snort_log_format']
    alert_priority = config['snort_alert_priority']
    service_key = config['pagerduty_service_key']

    incident_keys = set()
    for log_entry in read_logs(log_path):
        log = parse_log(log_entry, log_format)
        incident_key = get_incident_key(log, ('message', 'src', 'dest'))

        if (check_timestamp(log['timestamp'], START_TIME) and
                incident_key not in incident_keys and
                int(log['priority']) <= alert_priority):
            description = 'Snort: {}'.format(log['message'])
            incident = pager.create_event(service_key, description, 'trigger',
                                          log, incident_key)
            incident_keys.add(incident_key)

            yield log, incident


def load_config():
    """Load configuration from a JSON file"""

    config = deepcopy(DEFAULT_CONFIG)
    with open('/etc/snort2pd/snort2pd.json', 'r') as f:
        config.update(json.load(f))

    return config


def main():
    config = load_config()
    pager = PagerDuty(config['pagerduty_subdomain'],
                      config['pagerduty_api_token'])

    for log, incident in wait_for_alerts(pager, config):
        msg = {'log': log, 'incident_key': incident}
        logging.info(str(msg))

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
