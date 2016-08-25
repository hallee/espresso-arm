"""
Software PWM.

Hardkernel doesn't support hardware PWM on the Odroid C2.
This should work fine on the Raspberry Pi GPIO as well, though.
"""

import time
import wiringpi2 as wp
from multiprocessing import Process, Value

class SoftwarePWM:
    """
    Software PWM.
    Opens a process that runs continuously.
    """
    def __init__(self, pinNum):
        self.Process = Process
        self.duration = None
        self.onTime = Value("d", 0.0)
        self.offTime = Value("d", 0.0)
        self.stop = False
        self.processStarted = False

        self.pin = pinNum

    def controlPin(self, onTime, offTime, pin):
        wp.pinMode(pin, 1)

        while not self.stop:
            wp.digitalWrite(pin, 1)
            time.sleep(onTime.value)
            wp.digitalWrite(pin, 0)
            time.sleep(offTime.value)

    def pwmUpdate(self, dutyCycle, f):
        self.duration = 1/f
        self.onTime.value = self.duration * (dutyCycle / 100)
        self.offTime.value = self.duration - self.onTime.value

        if self.processStarted == False:
            self.p = self.Process(target = self.controlPin, args = (self.onTime, self.offTime, self.pin,))
            self.p.start()
            self.processStarted = True

# class HeaterControl:

#
# def main():
#     controller = SoftwarePWM(27)
#     controller.pwmUpdate(25, 1)
#
#
# if __name__ == '__main__':
#     main()
