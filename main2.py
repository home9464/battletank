"""
app.run(host='0.0.0.0', port =5000, debug=True, threaded=True)
"""
import sys
import random
import functools
import asyncio

from drive import Drive
#from camera import Camera
from gun import MainGun
from turret import Turret
from pad2 import GoogleStadiaController

driver = Drive()
#cam = Camera()
gunner = MainGun()
turretter = Turret()


async def main():
    print("press Ctl-C to exit")
    controller = GoogleStadiaController()
    controller.init()
    #controller.register('drive', drive)
    #controller.register('drive', driver.drive)
    #controller.register('move_gun', functools.partial(turretter.angle, 0))  # channel 0
    controller.register('move_gun', turretter.move)  # channel 0
    #controller.register('fire_gun', gunner.fire)  # channel 2
    try:
        await asyncio.create_task(controller.listen())
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
