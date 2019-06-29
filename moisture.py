import spidev
import time

delay = 0.5
moist_channel = 0

spi = spidev.SpiDev()
spi.open(0,0)

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1

    r = spi.xfer2([0])
    data = ((r[1] & 3) << 8)  +  r[2]
    # return data
    return r

while True:
    moist_value = readadc(moist_channel)
    print('Moist Value: ' , moist_value)
    time.sleep(delay)

