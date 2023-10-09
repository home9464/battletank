"""move the tank

"""
from typing import List

import RPi.GPIO as GPIO

BCM_PIN = {
    'motor1_pwm': 18, 
    'motor1_A': 15, 
    'motor1_B': 14,
    'motor2_pwm': 27, 
    'motor2_A': 17, 
    'motor2_B': 22
}

BOARD_PIN = {
    'motor1_pwm': 12, 
    'motor1_A': 10, 
    'motor1_B': 8,
    'motor2_pwm': 13, 
    'motor2_A': 11, 
    'motor2_B': 15
}

class Drive:
    DIRECTION_FORWARD = 1
    DIRECTION_BACKWARD = 2
    DIRECTION_LEFT = 3
    DIRECTION_RIGHT = 4
    def __init__(self, mode=GPIO.BCM):  # or GPIO.BOARD
        # GPIO.cleanup()
        GPIO.setmode(mode)  # Set Pi to use pin number when referencing GPIO pins.
        self.PIN = BCM_PIN if mode == GPIO.BCM else BOARD_PIN
        GPIO.setup(self.PIN['motor1_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_B'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_B'], GPIO.OUT)
        # the 1st motor
        self.pwm1 = GPIO.PWM(self.PIN['motor1_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        # the 2nd motor
        self.pwm2 = GPIO.PWM(self.PIN['motor2_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        self.pwm1.start(0) # Start the 1st motor  with 0% duty cycle
        self.pwm2.start(0) # Start the 2nd motor  with 0% duty cycle
        self.pwm1_forward_flag = 0
        self.pwm2_forward_flag = 0

    def stop(self):
        self.throttle(0)

    def _pin(self, a, b, c, d):
        GPIO.output(self.PIN['motor1_A'], a)
        GPIO.output(self.PIN['motor1_B'], b)
        GPIO.output(self.PIN['motor2_A'], c)
        GPIO.output(self.PIN['motor2_B'], d)

    def forward(self, percent=100):
        self.throttle(percent)
        self._pin(0, 1, 1, 0)

    def backward(self, percent=100):
        self.throttle(percent)
        self._pin(1, 0, 0, 1)

    def left(self, percent=100):
        self.throttle(percent)
        self._pin(0, 1, 0, 1)

    def right(self, percent=100):
        self.throttle(percent)
        self._pin(1, 0, 1, 0)

    def drive(self, direction_and_throttle:List) -> None:
        direction, throttle_percent = direction_and_throttle
        print(direction, throttle_percent)
        assert 0 <= direction and direction <= 4
        if direction == 0:
            self.stop()
        elif direction == 1:
            self.forward(throttle_percent)
        elif direction == 2:
            self.backward(throttle_percent)
        elif direction == 3:
            self.left(throttle_percent)
        elif direction == 4:
            self.right(throttle_percent)
            
    def throttle(self, percentage: int = 100) -> None:
        assert 0 <= percentage and percentage <= 100
        self.pwm1.ChangeDutyCycle(percentage)
        self.pwm2.ChangeDutyCycle(percentage)

    def close(self):
        try:
            self.pwm1.stop()
            self.pwm2.stop()
        finally:
            GPIO.cleanup()

if __name__ =='__main__':
    import time
    driver = Drive()
    for direction in [1, 2, 3, 4]:
        driver.drive(direction)
        time.sleep(3)
    driver.drive(0)
    driver.close()