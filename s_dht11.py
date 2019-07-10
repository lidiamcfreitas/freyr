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

while True:
    for _ in range(5):
        try:
            now = datetime.now()
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("{} - Temperature: {:.1f}C    Humidity: {}% ".format(
                now.strftime('%Y_%m_%d_%H%M%S'), temperature_c, humidity), flush=True)
            break
        except RuntimeError as error:
            pass

    sleep(SLEEP_SECONDS_SENSORS)
