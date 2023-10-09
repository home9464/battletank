import time
import random
import termios, fcntl, sys, os

from adafruit_servokit import ServoKit

#from maingun import NerfGun

class Turret:

    def __init__(self, max_angle=180):
        servos_indices = [0, 2]  # only use one servo
        self.servokit = ServoKit(channels=16)

        #self.min_x = 0
        #self.max_x = 180

        #self.min_y = 15
        #self.max_y = 90

        self.max_angle = 180
        
        for i in servos_indices:
            #self.servokit.servo[i].set_pulse_width_range(450, 2450)
            self.servokit.servo[i].set_pulse_width_range(500, 2500)
            self.servokit.servo[i].actuation_range = self.max_angle
        #self.gun = NerfGun()
        self.center()

    def angle(self, index:int, offset:int)-> None:
        """
        Args:
        """
        #print('turret', index, offset)
        #offset = 1 if offset > 1 else -1
        if index == 0:  # move the barrel vertically
            if offset == 1:
                if 80 <= self.x < 105:
                    self.x += 1
                    self.servokit.servo[index].angle = self.x
            elif offset == -1:
                if 80 < self.x <= 105:
                    self.x -= 1
                    self.servokit.servo[index].angle = self.x
            #elif offset == 0:
            #    print('STOP')

        elif index == 2:  # turn the turret
            if offset == 1:
                if 0 <= self.y < 180:
                    self.y += 1
                    self.servokit.servo[index].angle = self.y
            elif offset == -1:
                if 0 < self.y <= 180:
                    self.y -= 1
                    self.servokit.servo[index].angle = self.y
            #elif offset == 0:
            #    print('STOP')


        else:
            pass
        #print('!!!', angle)

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
        self.x = 90
        self.y = 90
        self.angle(0, self.x)
        self.angle(2, self.y)

    def up(self):
        self.y += 1
        if self.min_y <= self.y <= self.max_y:
            self.angle(0, self.y)

    def down(self):
        self.y -= 1
        if self.min_y <= self.y <= self.max_y:
            self.angle(0, self.y)

    def left(self):
        self.x -= 1
        if 0 <= self.x <= 180:
            self.angle(0, self.x)

    def right(self):
        self.x += 1
        if 0 <= self.x <= 180:
            self.angle(0, self.x)

    def _vertical(self, offset):
        """
        105 > self.x > 75 
        """
        self.x += offset
        print(self.x)
        if 80 <= self.x <= 105:
            self.angle(0, self.x)

    def _horizontal(self, offset):
        """
        

        """
        #assert -90 < offset < 90
        self.y += offset
        if 0 <= self.y <= 180:
            self.angle(2, self.y)

    def x_angle(self):
        return self.x 

    def y_angle(self):
        return self.y

def test2():
    rcws = Turret()
    time.sleep(1)
    Turret.ADJUST_GUN_UP_DOWN = True
    rcws.angle(2, 30)
    Turret.ADJUST_GUN_UP_DOWN = True
    time.sleep(3)
    #rcws.vertical(15)
    #rcws.horizontal(45)
    #time.sleep(1)
    #rcws.horizontal(-90)
    #for _ in range(15):
    #    rcws.vertical(-1)
    #    time.sleep(0.2)
    #for _ in range(30):
    #    rcws.vertical(1)
    #    time.sleep(0.2)
    #for _ in range(18):
    #rcws.horizontal(0)
    #time.sleep(2)
    #rcws.horizontal(-90)
    #time.sleep(2)
    #rcws.horizontal(180)
    #time.sleep(2)
    #rcws.horizontal(0)
    #time.sleep(2)
    #rcws.horizontal(0)
    #time.sleep(2)
    #rcws.horizontal(10)
    #time.sleep(0.2)
    #rcws.vertical(15)
    '''
    for _ in range(6):
        _x = random.randint(6, 10)
        _y = random.randint(0, 15)
        rcws.horizontal(_x)
        rcws.vertical(_y)
        time.sleep(1)
        #sq.shoot()
    '''

if __name__ == '__main__':
    test2()
