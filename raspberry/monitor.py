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
SLEEP_SECONDS_CAMERA = 30 * MINUTE_IN_SECONDS

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
dhtDevice = adafruit_dht.DHT11(board.D18)
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

aux_time_slept = SLEEP_SECONDS_CAMERA
while True:
    for sensor, channel in adc_channels.items():
        now = datetime.now()
        print('{} - {} Value: {} - Voltage: {:.3f}V'.format(
            now.strftime('%Y_%m_%d_%H%M%S'), sensor, channel.value, channel.voltage), flush=True)

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
    aux_time_slept += SLEEP_SECONDS_SENSORS

    if aux_time_slept >= SLEEP_SECONDS_CAMERA:
        now = datetime.now()
        fn_photo = now.strftime('%Y_%m_%d_%H%M%S') + '.jpg'
        camera.capture('/home/pi/captured_photos/' + fn_photo)
        print("Captured: ", fn_photo, flush=True)
        aux_time_slept = 0  # reset
