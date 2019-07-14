from time import sleep
import board
import adafruit_dht
from datetime import datetime
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-s', '--sleep', action='store', type=int, default=5)
my_parser.add_argument('--id', action='store', type=str, default="dht11")

args = my_parser.parse_args()

SLEEP_SECONDS_SENSORS = args.sleep

dhtDevice = adafruit_dht.DHT11(board.D18)

current_day = datetime.now().day
out_path = "s_dht11_{}_out.csv".format(datetime.now().strftime('%Y_%m_%d'))
out_file = open(out_path, 'a')

while True:
    if datetime.now().day != current_day:
        out_file.close()
        out_path = "s_dht11_{}_out.csv".format(datetime.now().strftime('%Y_%m_%d'))
        out_file = open(out_path, 'a')
        current_day = datetime.now().day

    for _ in range(5):
        try:
            now = datetime.now()
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            print("{} - Temperature: {:.1f}C    Humidity: {}% ".format(
                now.strftime('%Y_%m_%d_%H%M%S'), temperature_c, humidity), flush=True)
            to_write = "{}, {:.1}, {}\n".format(now.strftime('%Y_%m_%d_%H%M%S'), temperature_c, humidity)
            out_file.write(to_write)
            break
        except RuntimeError as error:
            pass

    sleep(SLEEP_SECONDS_SENSORS)
