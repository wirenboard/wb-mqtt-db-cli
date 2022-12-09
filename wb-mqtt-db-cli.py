#!/usr/bin/python
from __future__ import print_function
import time
# import pprint
import argparse
import csv
import datetime
import sys


try:
    import mosquitto
except ImportError:
    import paho.mqtt.client as mosquitto


from mqttrpc.client import TMQTTRPCClient, MQTTRPCError
import dateutil.parser

def format_value(value_str, decimal_places=None):
    if decimal_places and decimal_places >= 0:
        format_str = "%%.%df" % decimal_places

        return format_str % float(value_str)
    else:
        return value_str

def main():
    parser = argparse.ArgumentParser(description='wb-mqtt-db Console Client', add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--help', action='help',
                help='show this help message and exit')

    parser.add_argument('-h', '--host', dest='host', type=str,
                     help='MQTT host', default='localhost')

    parser.add_argument('-u', '--username', dest='username', type=str,
                     help='MQTT username', default='')

    parser.add_argument('-P', '--password', dest='password', type=str,
                     help='MQTT password', default='')

    parser.add_argument('-p', '--port', dest='port', type=int,
                     help='MQTT port', default='1883')

    parser.add_argument('--from', dest='date_from', type=str,
                     help='start date', default=None)

    parser.add_argument('--to', dest='date_to', type=str,
                     help='end date', default=None)

    parser.add_argument('--time-format', dest='time_format', type=str,
                     help='''strftime-style format string for timestamp formating. Use "%%s.%%f" for UNIX timestamp''', default="%Y-%m-%d %H:%M:%S.%f")

    parser.add_argument('--limit', dest='limit', type=int, help='The maximum number of data points to request',
        default=10000)

    i_group = parser.add_mutually_exclusive_group()

    i_group.add_argument('--interval', dest='min_interval', type=int,
                     help='Min interval between data points (ms)', default=None)

    i_group.add_argument('-a', '--auto-interval', dest='auto_interval', action="store_true",
                     help='Automatically estimate the interval between data points based on "limit", "from" and "start"')

    parser.add_argument('--decimal-places', dest='decimal_places', type=int, help='Number of decimal places in value')

    parser.add_argument('-d', '--delimiter', dest='delimiter', type=str, help='CSV field separator', default='\t')

    parser.add_argument('-o', '--output-fname', dest='output_fname', type=str, help='Write result to file. "-" means stdout', default='-')
    parser.add_argument("--timeout", dest="timeout", type=int, help="Request timeout (in seconds)")

    parser.add_argument('channels', metavar='DEVICE/CONTROL', type=str, nargs='+',
                        help='List of channels to request')


    args = parser.parse_args()

    if args.date_from:
        date_from = dateutil.parser.parse(args.date_from)
    else:
        date_from = None

    if args.date_to:
        date_to = dateutil.parser.parse(args.date_to)
    else:
        date_to = datetime.datetime.now()

    if args.min_interval:
        min_interval = args.min_interval
    else:
        min_interval = None

    if args.auto_interval:
        if args.date_from is None:
            parser.error("--from argument should be present when using -a/--auto-interval")

        time_interval = date_to - date_from
        if time_interval < datetime.timedelta(0):
            parser.error("--from is greater than --to (or in future)")
        min_interval = (time_interval / args.limit).total_seconds() * 1000



    client = mosquitto.Mosquitto()

    if args.username:
        client.username_pw_set(args.username, args.password)

    client.connect(args.host, args.port)
    client.loop_start()

    rpc_client = TMQTTRPCClient(client)
    client.on_message = rpc_client.on_mqtt_message

    channels = [channel.split('/', 2) for channel in args.channels]

    fieldnames = ['channel', 'time', 'average', 'min', 'max']
    if args.output_fname == '-':
        csvfile = sys.stdout
    else:
        csvfile = open(args.output_fname, 'wb')

    try:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=args.delimiter)

        for i, channel in enumerate(channels):
            rpc_params =  {
                'channels': [channel,],

                'timestamp' : {
                },
                'limit' : args.limit,
                'ver' : 1,
            }

            if args.date_from:
                rpc_params['timestamp']['gt'] = int(time.mktime(date_from.timetuple()))
            if args.date_to:
                rpc_params['timestamp']['lt'] = time.mktime(date_to.timetuple())

            if min_interval:
                rpc_params['min_interval'] = min_interval

            if args.timeout:
                rpc_params["request_timeout"] = args.timeout
                mqtt_timeout = args.timeout + 5
            else:
                mqtt_timeout = 30

            try:
                resp =  rpc_client.call('db_logger', 'history', 'get_values', rpc_params, timeout=mqtt_timeout)
            except MQTTRPCError as err:
                if err.code == -32100:
                    print("ERROR: Backend wb-mqtt-db failed to process request in time. Consider increasing timeout (--timeout).", file=sys.stderr)
                    return
                raise err

            if i == 0:
                writer.writeheader()

            if len(resp["values"]) == 0:
                print("No records for %s/%s channel" % tuple(channel))
            else:
                for row in resp['values']:
                    csvrow = dict(
                        channel = ("%s/%s" % tuple(channel)),
                        time    = datetime.datetime.fromtimestamp(row.get('t') or row.get('timestamp')).strftime(args.time_format),
                        average = format_value(row.get('v') or row.get('value'), args.decimal_places)
                    )
                    if 'min' in row:
                        csvrow['min'] = format_value(row['min'], args.decimal_places)
                    if 'max' in row:
                        csvrow['max'] = format_value(row['max'], args.decimal_places)

                    writer.writerow(csvrow)
    finally:
        csvfile.close()



if __name__ == "__main__":
    main()
