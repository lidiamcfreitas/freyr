import signal
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


class DHT11Monitor:
    def __init__(self):
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)
        self.current_day = datetime.now().day
        self.out_path = "s_dht11_{}_out.csv".format(datetime.now().strftime('%Y_%m_%d'))
        self.out_file = open(self.out_path, 'a')

    def terminate(self):
        self.out_file.close()
        print("Exiting ... ")

    def change_log_file(self):
        self.out_file.close()
        self.out_path = "s_dht11_{}_out.csv".format(datetime.now().strftime('%Y_%m_%d'))
        self.out_file = open(self.out_path, 'a')
        self.current_day = datetime.now().day


monitor = DHT11Monitor()

while True:
    if datetime.now().day != monitor.current_day:
        monitor.change_log_file()

    for _ in range(5):
        try:
            now = datetime.now()
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            print("{} - Temperature: {:.1f}C    Humidity: {}% ".format(
                now.strftime('%Y_%m_%d_%H%M%S'), temperature_c, humidity), flush=True)
            to_write = "{}, {:.1}, {}\n".format(now.strftime('%Y_%m_%d_%H%M%S'), temperature_c, humidity)
            monitor.out_file.write(to_write)
            break
        except RuntimeError as error:
            pass

    sleep(SLEEP_SECONDS_SENSORS)
