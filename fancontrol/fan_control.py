#!/usr/bin/env python3

import time
import os

import RPi.GPIO as GPIO  # pip install RPi.GPIO

PIN = 2
MAX_TEMP = 60  # Celsius


def main():
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

                time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

    return 0


if __name__ == "__main__":
    raise SystemError(main())
