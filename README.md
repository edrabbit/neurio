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


Format:
You can output in two formats: json and kv (key=value). If you choose KV,
each channel will be output on a separate log line. If you choose json, all
channels will be included in one log line.

Ex.

    python fetch_neurio.py --ip 192.168.1.227 --format kv --type sensor

    2015-03-09T00:12:35.670884+00:00 Power(kW)=0.174, EnergyImported(kWh)=9.281, ReactivePower(kVAR)=-0.042, Voltage(V)=118.645, EnergyExported(kWh)=0.000, Channel=1
    2015-03-09T00:12:35.670884+00:00 Power(kW)=0.628, EnergyImported(kWh)=25.960, ReactivePower(kVAR)=-0.153, Voltage(V)=118.418, EnergyExported(kWh)=0.000, Channel=3
    2015-03-09T00:12:35.670884+00:00 Power(kW)=0.454, EnergyImported(kWh)=16.679, ReactivePower(kVAR)=-0.111, Voltage(V)=118.192, EnergyExported(kWh)=0.000, Channel=2
    2015-03-09T00:12:35.670884+00:00 Power(kW)=0.000, EnergyImported(kWh)=0.000, ReactivePower(kVAR)=0.000, Voltage(V)=0.000, EnergyExported(kWh)=0.000, Channel=4


    python fetch_neurio.py --ip 192.168.1.227 --format json --type sensor

    2015-03-09T00:11:14.376018+00:00 {"1": {"Power (kW)": "0.173", "Energy Imported (kWh)": "9.277", "Reactive Power (kVAR)": "-0.043", "Voltage (V)": "118.789", "Energy Exported (kWh)": "0.000", "Channel": "1"}, "3": {"Power (kW)": "0.621", "Energy Imported (kWh)": "25.946", "Reactive Power (kVAR)": "-0.155", "Voltage (V)": "118.534", "Energy Exported (kWh)": "0.000", "Channel": "3"}, "2": {"Power (kW)": "0.448", "Energy Imported (kWh)": "16.669", "Reactive Power (kVAR)": "-0.111", "Voltage (V)": "118.278", "Energy Exported (kWh)": "0.000", "Channel": "2"}, "4": {"Power (kW)": "0.000", "Energy Imported (kWh)": "0.000", "Reactive Power (kVAR)": "0.000", "Voltage (V)": "0.000", "Energy Exported (kWh)": "0.000", "Channel": "4"}}


Important note: Fetching data may break if the format of the Neurio web
interface changes since this is parsing the HTML until an API is available.

https://www.neur.io/

I am not affiliated with Neurio in any way.
