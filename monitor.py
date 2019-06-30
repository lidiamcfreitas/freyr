from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht
from picamera import PiCamera
from datetime import datetime

MINUTE_IN_SECONDS = 60
SLEEP_SECONDS_SENSORS = 5
SLEEP_SECONDS_CAMERA = 10 * MINUTE_IN_SECONDS


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

adc_channels = {
    'water_level': AnalogIn(mcp, MCP.P0),
    'photoresistor': AnalogIn(mcp, MCP.P1),
    'soil_moisture': AnalogIn(mcp, MCP.P2)
}
dhtDevice = adafruit_dht.DHT11(board.D18)
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

aux_time_slept = 0
while True:
    print("\n------- Sensor Values -------")
    for sensor, channel in adc_channels.items():
        print('{} Value: {}'.format(sensor, channel.value))
        print('{} Voltage: {}V'.format(sensor, str(channel.voltage)))

    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print("Temperature: {:.1f} C    Humidity: {}% "
              .format(temperature_c, humidity))
    except RuntimeError as error:
        print(error.args[0])

    sleep(SLEEP_SECONDS_SENSORS)
    aux_time_slept+= SLEEP_SECONDS_SENSORS

    if aux_time_slept>=SLEEP_SECONDS_CAMERA:
        now = datetime.now()
        fn_photo = now.strftime('%Y_%m_%d_%H%M%S') + '.jpg'
        camera.capture('~/captured_photos/' + fn_photo)
        print("Captured: ", name)
        aux_time_slept=0 # reset
