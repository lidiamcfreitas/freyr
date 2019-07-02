from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht
from picamera import PiCamera
from datetime import datetime
import json
import requests

MINUTE_IN_SECONDS = 60
SLEEP_SECONDS_SENSORS = 5
SLEEP_SECONDS_CAMERA = 30 * MINUTE_IN_SECONDS
HEADERS = {"Content-type": "application/json"}
URL_VEGECLOUD = "https://api.vegecloud.com/in/34315633/"
API_KEY_VEGECLOUD = "EHAGWK27SSMXGR7L" 
VEGECLOUD_MAP = {
    'water_level': -1,
    'soil_moisture': -1,
    'humidity': -1, # 1
    'temperature': -1, # 2
    'photoresistor': 3
}

class VegeCloudMessage:
    def __init__(self, sensors=[1,2,3]):
        self.message = {
            "api_key": API_KEY_VEGECLOUD,
            "sensors":[]}
        self.map_sensor2array = {} # map hub sensor number to array position
        for i in range(len(sensors)):
            self.map_sensor2array[sensors[i]] = i;
            new_sensor = {
                    "slot": sensors[i],
                    "samples": []}
            self.message["sensors"].append(new_sensor)
        print(self.message)

    def add_sample(self, sensor, value):
        if (sensor==-1): 
            return

        now = datetime.now()
        sample = {
                "t": now.strftime("%Y-%m-%d %H:%M:%S"),
                "v": value
        }
        print(self.map_sensor2array[sensor])
        print(self.message)
        self.message["sensors"][self.map_sensor2array[sensor]]["samples"].append(sample);

    def send(self):
        print('\n---- SENDING ----')
        print(self.message)
        print('-----------------\n')
        response = requests.post(URL_VEGECLOUD, data=json.dumps(self.message), headers=HEADERS)
        print(json.loads(response.text))


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

aux_time_slept = 0
while True:
    message = VegeCloudMessage(sensors=[1,2,3])

    print("\n------- Sensor Values -------")
    for sensor, channel in adc_channels.items():
        print('{} Value: {}'.format(sensor, channel.value))
        print('{} Voltage: {}V'.format(sensor, str(channel.voltage)))
        message.add_sample(VEGECLOUD_MAP[sensor], channel.voltage)

    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print("Temperature: {:.1f} C    Humidity: {}% "
              .format(temperature_c, humidity), flush=True)
        message.add_sample(VEGECLOUD_MAP['temperature'], temperature_c)
        message.add_sample(VEGECLOUD_MAP['humidity'], humidity)

    except RuntimeError as error:
        print(error.args[0])
    
    try:
        message.send()
    except ConnectionError as error:
        print(error.args[0])

    sleep(SLEEP_SECONDS_SENSORS)
    aux_time_slept += SLEEP_SECONDS_SENSORS
