from os import environ
import json
from time import sleep

import RPi.GPIO as GPIO 


SPEEDS_FILE_PATH = environ.get('SPEEDS_FILE', '/home/pi/speeds.json')

CHANNEL_ASSOCIATION = {
    'unsav': 1
}

SHIMS = {
    user: GPIO.PWM(channel, 0) for user, channel in CHANNEL_ASSOCIATION.items()
}


def read_file():
    with open(SPEEDS_FILE_PATH) as speeds_file:
        return json.loads(speeds_file.read())


def main():
    GPIO.setmode(GPIO.BOARD)

    for channel in CHANNEL_ASSOCIATION.values():
        GPIO.setup(channel, GPIO.OUT)

    while True:
        for user, pwm in SHIMS.items():
            pass

        sleep(1)

if __name__ == '__main__':
    main()
