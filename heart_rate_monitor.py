#!/usr/bin/env python

import time
from collections import deque

import RPi.GPIO as GPIO

class HeartRateMonitor:
    INTERRUPT_PIN = 17
    MAX_DETECTED_TIMES_COUNT = 20
    MAX_PULSE_INTERVAL = 2.0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.INTERRUPT_PIN, GPIO.IN)

        self._init_array()

    def _init_array(self):
        self.detected_times = deque([])

    def _calc_heart_rate(self):
        return 1200.0 / (self.detected_times[-1] - self.detected_times[0])

    def _interrupt(self):
        self.detected_times.append(time.time())

        if(len(self.detected_times) == 1):
            return

        interval = self.detected_times[-1] - self.detected_times[-2]
        heart_rate = -1
        if interval > self.MAX_PULSE_INTERVAL:
            print('Heart rate measure error. Monitoring will restart!')
            self._init_array()
            return

        if(len(self.detected_times) >= self.MAX_DETECTED_TIMES_COUNT):
            heart_rate = self._calc_heart_rate()
            self.detected_times.popleft()

        print("HeartRate: {heart_rate}, Interval: {interval}".format(heart_rate = heart_rate, interval = interval))

    def execute(self):
        print('Please ready your heart rate monitor.')
        time.sleep(3)

        while True:
            GPIO.wait_for_edge(self.INTERRUPT_PIN, GPIO.RISING)
            self._interrupt()

if __name__ == '__main__':
    monitor = HeartRateMonitor()
    monitor.execute()
