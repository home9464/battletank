import time
import RPi.GPIO as GPIO

CHANNEL_ID = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class MainGun:
    def __init__(self):
        GPIO.setup(CHANNEL_ID, GPIO.OUT)
        GPIO.output(CHANNEL_ID, GPIO.LOW)

    def fire(self, yes_or_no:bool):
        """fire the 
        """
        if yes_or_no:
            GPIO.output(CHANNEL_ID, GPIO.HIGH)
        else:
            GPIO.output(CHANNEL_ID, GPIO.LOW)

    def stop_fire(self):
        GPIO.output(CHANNEL_ID, GPIO.LOW)
    
    def cleanup(self):
        GPIO.cleanup()

if __name__ =='__main__':
    gun = MainGun()
    while True:
        gun.fire(True)
        time.sleep(5)
        gun.fire(False)
        time.sleep(5)
    #gun.stop_fire()

