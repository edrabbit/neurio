fetch_neurio
============

Retrieve your Neurio sensor data directly from the sensor itself.

    usage: fetch_neurio.py [-h] --ip IP --format {json,kv} --type {raw,sensor}
                           [--local]

    Fetch Neurio sensor data

    optional arguments:
      -h, --help           show this help message and exit
      --ip IP              IP address of sensor
      --format {json,kv}   Format to output readings in
      --type {raw,sensor}  Which readings to output
      --local              Return timestamps using local system time instead of
                           UTC


Requirements:
    pip install BeautifulSoup4
    pip install pytz

Important note: This may break if the format of the Neurio web interface
changes as we are parsing HTML.

https://www.neur.io/

I am not affiliated with Neurio in any way.
