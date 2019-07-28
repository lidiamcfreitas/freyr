from time import sleep
from picamera import PiCamera
from datetime import datetime
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-s', '--sleep_minutes', action='store', type=int, default=30)
my_parser.add_argument('--id', action='store', type=str, default="camera")

args = my_parser.parse_args()

SLEEP_SECONDS_CAMERA = 60 * args.sleep_minutes

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

while True:
    now = datetime.now()
    fn_photo = now.strftime('%Y_%m_%d_%H%M%S') + '.jpg'
    camera.capture('/home/pi/captured_photos/' + fn_photo)
    print("Captured: ", fn_photo, flush=True)

    sleep(SLEEP_SECONDS_CAMERA)
