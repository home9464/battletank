import sys
import random
import functools
import asyncio

from drive import Drive
#from camera import Camera
from gun import MainGun
from turret import Turret
from gamepad import GamepadController

driver = Drive()
#cam = Camera()
gunner = MainGun()
commander = Turret()


async def main():
    print("press Ctl-C to exit")
    controller = GamepadController(debug=False)
    #controller.register('drive', drive)
    controller.register('drive', driver.drive)
    controller.register('servo0', functools.partial(commander.angle, 0))  # channel 0
    controller.register('servo1', functools.partial(commander.angle, 2))  # channel 2
    controller.register('fire', gunner.fire)  # channel 2
    try:
        controller_producer = asyncio.create_task(controller.producer())
        #controller_random_event = asyncio.create_task(controller.random_event())
        controller_consumer = asyncio.create_task(controller.consumer())
        #await asyncio.gather(controller_producer)
        #task2 = asyncio.create_task(cam.start())
        await controller_producer
        #await controller_consumer
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        #cam.close()

if __name__ == '__main__':
    asyncio.run(main())
