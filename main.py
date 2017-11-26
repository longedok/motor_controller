import os
from time import sleep

import requests

import RPi.GPIO as GPIO


SPEEDS_URL = os.environ.get('SPEEDS_URL', 'http://wth2017.hypershape.club/')

GPIO.setmode(GPIO.BOARD)


class Spinner:
    def __init__(self, input1, input2, enable, speed=100):
        self.input1 = input1
        self.input2 = input2
        self.enable = enable

        self.speed = speed

        GPIO.setup(self.input1, GPIO.OUT)
        GPIO.setup(self.input2, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)

        self.shim = GPIO.PWM(self.input2, 100)

        self.running = False

    def start(self):
        GPIO.output(self.enable, GPIO.HIGH)
        GPIO.output(self.input1, GPIO.LOW)
        # GPIO.output(self.input2, GPIO.HIGH)
        self.shim.start(self.speed)

        self.running = True

    def stop(self):
        GPIO.output(self.enable, GPIO.LOW)

        self.running = False

    def change_speed(self, speed):
        self.speed = speed

        self.shim.ChangeDutyCycle(self.speed)

        if not self.running:
            self.start()


SPINNERS = [
    Spinner(18, 16, 22),
    Spinner(21, 23, 19)
]


def speed_to_duty_cycle(speed):
    return int((speed * 100) / 2.0) + 50


def get_speeds():
    speeds = requests.get(SPEEDS_URL + 'speeds').json()
    clicking_rate = requests.get(SPEEDS_URL + 'clicks').json()

    print "got clicking rate %s" % clicking_rate

    clicking_rate = 100 if abs(clicking_rate - 1) < 0.000001 else 0

    print 'got speeds: %s' % speeds

    commit_speeds = map(speed_to_duty_cycle,[speed for speed in list(reversed(sorted(speeds.values())))[:1]]) or [0]

    return [clicking_rate] +  commit_speeds


def main():
    # for spinner in SPINNERS[1:]:
    #     spinner.start()
    #
    # sleep(3)

    try:
        while True:
            try:
                speeds = get_speeds()
            except:
                sleep(5)

                continue

            min_len = min(len(speeds), len(SPINNERS))

            for i in range(min_len):
                print 'spinner %d speed - %s' % (i + 1, speeds[i])

                SPINNERS[i].change_speed(speeds[i])

            sleep(5)
    finally:
        for spinner in SPINNERS:
            spinner.stop()

        GPIO.cleanup()

if __name__ == '__main__':
    main()
