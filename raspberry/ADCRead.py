from time import sleep

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

chan_1 = AnalogIn(mcp, MCP.P1)

chan_2 = AnalogIn(mcp, MCP.P2)

while True:
    # print('Channel 0 Raw ADC Value: ', chan.value)
    # print('Channel 0 ADC Voltage: ' + str(chan.voltage) + 'V')
    print('Channel 1 Raw ADC Value: ', chan_1.value)
    print('Channel 1 ADC Voltage: ' + str(chan_1.voltage) + 'V')
    sleep(1)
    print('Channel 2 Raw ADC Value: ', chan_2.value)
    print('Channel 2 ADC Voltage: ' + str(chan_2.voltage) + 'V')
    sleep(1)
