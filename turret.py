import time
import random
import termios, fcntl, sys, os

from adafruit_servokit import ServoKit

class Turret:

    def __init__(self, max_angle=180):
        self.servokit = ServoKit(channels=16)

        self.vertical_servo_id = 0
        self.horizontal_servo_id = 2

        self.horizontal_angle = 90
        self.vertical_angle = 90

        for i in [self.vertical_servo_id, self.horizontal_servo_id]:
            #self.servokit.servo[i].set_pulse_width_range(450, 2450)
            self.servokit.servo[i].set_pulse_width_range(500, 2500)
            self.servokit.servo[i].actuation_range = 180
        # center
        self.center()


    def angle(self, index:int, offset:int=1)-> None:
        """
        Args:
        """
        # print('turret', index, offset, self.horizontal_angle)
        if index == self.vertical_servo_id:  # move the barrel vertically
            self.vertical(offset)

        elif index == self.horizontal_servo_id:  # turn the turret
            self.horizontal(offset)

    def shoot(self):
        """
        servo4: 150(off) - 90(on)
        """
        try:
            self.gun.on()
            time.sleep(1)
            self.angle(4, 150)
            time.sleep(1)
            self.angle(4, 90)
            time.sleep(1)
            self.angle(4, 150)
        finally:
            self.gun.off()

    def center(self):
        """
        """
        self.angle(0, 90)
        self.angle(2, 90)

    def vertical(self, offset):
        """
        105 > self.x > 75 
        """
        if 80 <= self.vertical_angle + offset < 105:
            self.vertical_angle += offset
            self.servokit.servo[self.vertical_servo_id].angle = self.vertical_angle

    def horizontal(self, offset):
        """
        """
        #if 0 <= offset < 180:
        #    self.horizontal_angle = offset
        #    print('X', self.horizontal_angle)
        #    self.servokit.servo[self.horizontal_servo_id].angle = self.horizontal_angle
        if 0 <= self.horizontal_angle + offset < 180:
            self.horizontal_angle += offset
            self.servokit.servo[self.horizontal_servo_id].angle = self.horizontal_angle
            time.sleep(0.01)


def test2():
    rcws = Turret()
    #for i in range(90):
    #    rcws.horizontal(1)
    #    time.sleep(0.2)
    for i in range(10):
        rcws.vertical(1)
        time.sleep(0.2)
    for i in range(10):
        rcws.vertical(-1)
        time.sleep(0.2)



if __name__ == '__main__':
    test2()
