from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()

minute = 60
camera.resolution = (2592, 1944)
camera.framerate = 15

while True:
    now = datetime.now()
    name = now.strftime('%Y%m%d_%H%M%S') + '.jpg' 
    camera.capture('/home/pi/photos/'+name)
    sleep(10 * minute)
