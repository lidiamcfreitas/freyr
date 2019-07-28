'''
Simple service to start or stop a water valve. Usage:

1. To open a valve:
    python s_gpio.py start PIN
2. To close a valve:
    python s_gpio.py stio PIN
'''
import signal
import argparse
import sys

from gpiozero import DigitalOutputDevice
from time import sleep
from datetime import datetime

class Valve:
    def __init__(self):
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)

    def __str__(self):
        return '''\nSimple service to start or stop a water valve. Usage: 
        1. To open a valve: 
            python s_gpio.py start PIN 
        2. To close a valve: 
            python s_gpio.py stop PIN '''

    def terminate(self):
        print("Exiting... ")

    def start(self):
        self.valve.on()

    def stop(self):
        self.valve.off()

    def setPin(self, pin):
        self.valve = DigitalOutputDevice(pin)


if __name__ == "__main__":
    
    currValve = Valve()
    
    try:
        # Parse inputs
        mode = sys.argv[1]
        pin = sys.argv[2]

        # Set valve pins
        currValve.setPin(pin)
        
        if mode == 'start':
            currValve.start()
        elif mode == 'stop':
            currValve.stop()
        else:
            print(currValve)

        signal.pause()
    except Exception:
        print(currValve)