#!/usr/bin/env python3

import os
from time import sleep
import RPi.GPIO as GPIO

PIN = 2  # The pin ID, edit here to change it
MAX_TEMP = 70  # The maximum temperature in Celsius after which we trigger the fan


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.setwarnings(False)
    try:
        while True:
            res = os.popen("vcgencmd measure_temp").readline()
            temp = res.replace("temp=", "").replace("'C\n", "")
            # print("temp is {0}".format(temp)) #Uncomment here for testing
            cpu_temp = float(temp)
            if cpu_temp > MAX_TEMP:
                GPIO.output(PIN, True)
            else:
                GPIO.output(PIN, False)

                # Read the temperature every 5 sec, increase or decrease this limit if you want
                sleep(5)
    finally:
        GPIO.cleanup()  # resets all GPIO ports used by this program
