from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-s', '--sleep', action='store', type=int, default=5)
my_parser.add_argument('--id', action='store', type=str, default="adc")

args = my_parser.parse_args()

SLEEP_SECONDS_SENSORS = args.sleep

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

adc_channels = {
    # 'water_level': AnalogIn(mcp, MCP.P0),
    'photoresistor': AnalogIn(mcp, MCP.P1),
    # 'soil_moisture': AnalogIn(mcp, MCP.P2)
}

while True:
    for sensor, channel in adc_channels.items():
        now = datetime.now()
        print('{} - {} Value: {} - Voltage: {:.3f}V'.format(
            now.strftime('%Y_%m_%d_%H%M%S'), sensor, channel.value, channel.voltage), flush=True)

    sleep(SLEEP_SECONDS_SENSORS)
