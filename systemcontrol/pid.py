"""
PID Controller
"""
import time

class PID:
    def __init__(self, P=2.0, I=0.0, D=1.0, integratorMax=20, integratorMin=-20, totalMax=100, totalMin=0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.integratorMax = integratorMax
        self.integratorMin = integratorMin

        self.currentTime = time.time()
        self.lastTime = self.currentTime

        self.totalMax = totalMax
        self.totalMin = totalMin

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.setPoint = 0.0
        self.error = 0.0
        self.lastError = 0.0
        self.sampleTime = 1.2/4

    def update(self, currentValue):
    # Calculate PID output value for given reference input and feedback
        self.error = self.setPoint - currentValue

        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = self.error - self.lastError

        if (deltaTime >= self.sampleTime):
            self.PTerm = self.Kp * self.error
            self.ITerm += self.error * deltaTime

            if (self.ITerm < self.integratorMin):
                self.ITerm = self.integratorMin
            elif (self.ITerm > self.integratorMax):
                self.ITerm = self.integratorMax

            self.DTerm = 0.0
            if deltaTime > 0:
                self.DTerm = deltaError / deltaTime

            self.lastTime = self.currentTime
            self.lastError = self.error
            PID = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
        else:
            PID = 0

        return PID

    def setSetPoint(self, setPoint):
    # Initilize the setpoint of PID
        self.setPoint = setPoint

    def setKp(self, P):
        self.Kp = P

    def setKi(self, I):
        self.Ki = I

    def setKd(self, D):
        self.Kd = D

    def getPoint(self):
        return self.setPoint

    def getError(self):
        return self.error
