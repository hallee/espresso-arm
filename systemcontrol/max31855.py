"""
Driver for the Adafruit MAX31855
Thermocouple amplifier board.

The SPI interface is software driven
as hardware SPI output is not implemented
for the Odroid C2. 
"""

import time
import wiringpi2 as wp
from multiprocessing import Value

class SoftwareSPI:
    """
    Software clock for SPI. Very slow.
    """
    def __init__(self):
        self.duration = None
        self.onTime = Value("d", 0.0)
        self.offTime = Value("d", 0.0)
        self.stop = False
        self.temp = 0
        self.bitIndex = 0

        self.clk = 5
        self.cs = 4
        self.do = 1

    def getTemp(self):
        return self.temp

    def controlPin(self, onTime, offTime):
        wp.wiringPiSetup()
        wp.pinMode(self.clk, 1)
        wp.pinMode(self.cs, 1)
        wp.pinMode(self.do, 0)
        wp.digitalWrite(self.clk, 1)
        wp.digitalWrite(self.cs, 1)
        d = 0
        bitIndex = 0

        while not self.stop:
            wp.digitalWrite(self.clk, 0)
            if bitIndex == 0:
                d = 0
                wp.digitalWrite(self.cs, 0)
            d <<= 1
            d |= wp.digitalRead(self.do)
            time.sleep(offTime.value)
            wp.digitalWrite(self.clk, 1)
            time.sleep(onTime.value)
            if bitIndex == 31:
                if (d & 0x7):
                    # "Serious Problem"
                    print('Problem with MAX31855 board.')
                    d = 0
                elif (d & 0x80000000):
                    # Negative!
                    d = 0xFFFFC000 | ((d >> 18) & 0x00003FFFF)
                else:
                    d >>= 18
                d *= 0.25
                self.temp = d
                wp.digitalWrite(self.cs, 1)
                bitIndex = 0
            else:
                bitIndex += 1


    def initiateSPI(self, dutyCycle, f):
        self.duration = 1/f
        self.onTime.value = self.duration * (dutyCycle / 100)
        self.offTime.value = self.duration - self.onTime.value
        self.controlPin(self.onTime, self.offTime)
