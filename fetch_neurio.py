""" Retrieve Neurio sensor data directly from your sensor

Outputs in either json or key=value format with a timestamp of when the data
was fetched.
"""

__author__ = "Ed Hunsinger"
__email__ = "edrabbit@edrabbit.com"


import argparse
import datetime
import json
import logging

import bs4
import pytz
import urllib2


def fetch_page(url, localtime=True):
    """ Fetches the page with readings and returns (timestamp, page contents)
    """
    r = urllib2.urlopen(url)
    if localtime:
        timestamp = datetime.datetime.now()
    else:
        timestamp = datetime.datetime.now(pytz.utc)
    return timestamp, r.read()


def parse_readings(data):
    """ Parse the html returned by the page

    This may break if they structure of the page changes at any point.
    """
    bs = bs4.BeautifulSoup(data)
    parsed_tables = {}
    tables = bs.findAll('table')
    table_num = 0
    for table in tables:
        parsed_tables[table_num] = {}
        rows = table.findAll('tr')
        row_num = 0
        for row in rows:
            parsed_tables[table_num][row_num] = {}
            cols = row.findAll('td')
            col_num = 0
            for col in cols:
                parsed_tables[table_num][row_num][col_num] = {}
                value = col.text.replace('\n', '')
                parsed_tables[table_num][row_num][col_num] = value
                col_num += 1
            row_num += 1
        table_num += 1
    return parsed_tables


def get_raw_measurements(parsed_data):
    """ Get the raw measurements returned in a dictionary with channels
    """
    rm = parsed_data[0]
    raw_measurements = {}
    for index in [2, 3, 4, 5]:
        channel = rm[index][0]
        raw_measurements[channel] = {}
        for key, col_name in rm[1].iteritems():
            raw_measurements[channel][col_name] = rm[index][key]
    return raw_measurements


def get_sensor_readings(parsed_data):
    """ Get the sensor readings returned in a dictionary with channels
    """
    sr = parsed_data[1]
    sensor_readings = {}
    for index in [2, 3, 4, 5]:
        channel = sr[index][0]
        sensor_readings[channel] = {}
        for key, col_name in sr[1].iteritems():
            sensor_readings[channel][col_name] = sr[index][key]
    return sensor_readings


def print_json_log(readings, timestamp):
    """ Log data in json strings with timestamp
    """
    json_values = json.dumps(readings)
    logline = "%s %s" % (timestamp, json_values)
    logging.info(logline)


def readings_as_json(ip, local=False):
    """Return readings as a json string"""
    url = 'http://%s/both_tables.html' % ip
    (timestamp, data) = fetch_page(url, localtime=local)
    parsed_data = parse_readings(data)
    readings = get_sensor_readings(parsed_data)
    readings['timestamp'] = timestamp.isoformat()
    return json.dumps(readings)


def print_keyvalue(readings, timestamp):
    """ Log data in Splunk-friendly key=value pairs
    """
    for channel in readings:
        keyvalues = []
        for key, value in readings[channel].iteritems():
            keyvalues.append("%s=%s" % (key.replace(' ', ''), value))
        logline = "%s %s" % (timestamp, ', '.join(keyvalues))
        logging.info(logline)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch Neurio sensor data')
    parser.add_argument(
        '-i', '--ip', type=str, help='IP address of sensor', required=True)
    parser.add_argument(
        '-f', '--format', type=str, help='Format to output readings in',
        choices=['json', 'kv'], required=True)
    parser.add_argument(
        '-t', '--type', type=str, help='Which readings to output',
        choices=['raw', 'sensor'], required=True)
    parser.add_argument(
        '-o', '--outputfile', type=str, help='File to log to',
        default='output.log')
    parser.add_argument(
        '--local', action='store_true',
        help='Return timestamps using local system time instead of UTC')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format='%(message)s', filename=args.outputfile)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    url = 'http://%s/both_tables.html' % args.ip
    (timestamp, data) = fetch_page(url, localtime=args.local)
    parsed_data = parse_readings(data)

    if args.type == 'raw':
        readings = get_raw_measurements(parsed_data)
    elif args.type == 'sensor':
        readings = get_sensor_readings(parsed_data)

    if args.format == 'json':
        print_json_log(readings, timestamp.isoformat())
    elif args.format == 'kv':
        print_keyvalue(readings, timestamp.isoformat())
