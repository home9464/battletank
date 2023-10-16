"""The Xbox controller

1. it was not started
2. powered off after connection

devadm info --query=property --name=/dev/input/js0 | grep "ID_INPUT_JOYSTICK=1"


DEVPATH=/devices/platform/soc/fe201000.serial/tty/ttyAMA0/hci0/hci0:11/0005:045E:02E0.000A/input/input11/event4
DEVNAME=/dev/input/event4
MAJOR=13
MINOR=68
SUBSYSTEM=input
USEC_INITIALIZED=6836871854
ID_INPUT=1
ID_INPUT_JOYSTICK=1
ID_INPUT_KEY=1
ID_BUS=bluetooth
XKBMODEL=pc105
XKBLAYOUT=us
BACKSPACE=guess
ID_INPUT_JOYSTICK_INTEGRATION=external
ID_PATH=platform-soc
ID_PATH_TAG=platform-soc
ID_FOR_SEAT=input-platform-soc
LIBINPUT_DEVICE_GROUP=5/45e/2e0:dc:a6:32:65:d4:45
LIBINPUT_FUZZ_00=255
LIBINPUT_FUZZ_01=255
TAGS=:uaccess:power-switch:seat:


"""
import time
import asyncio
import random
from evdev import  InputDevice



"""XBOX
STICK_OR_PAD_TYPE = 3
CODE_LEFT_STICK_VERTICAL = 0
CODE_LEFT_STICK_HORIZONTAL = 1

CODE_RIGHT_STICK_VERTICAL = 3
CODE_RIGHT_STICK_HORIZONTAL = 4

CODE_PAD_HORIZONTAL = 16
CODE_PAD_VERTICAL = 17

CODE_BUTTON_A = 304
CODE_BUTTON_B = 305
CODE_BUTTON_X = 306
CODE_BUTTON_Y = 307
CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309
CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309

CODE_BUTTON_VIEW = 310
CODE_BUTTON_MENU = 311
"""

### Google Stadia

STICK_OR_PAD_TYPE = 3
CODE_LEFT_STICK_VERTICAL = 0
CODE_LEFT_STICK_HORIZONTAL = 1

CODE_RIGHT_STICK_HORIZONTAL = 2
CODE_RIGHT_STICK_VERTICAL = 5

CODE_PAD_HORIZONTAL = 16
CODE_PAD_VERTICAL = 17

CODE_BUTTON_A = 304  # 304, 1, 0/1
CODE_BUTTON_B = 305  # 305, 1, 0/1
CODE_BUTTON_X = 307  # 307, 1, 0/1
CODE_BUTTON_Y = 308  # 308, 1, 0/1

CODE_BUTTON_LEFT_BUMPER = 310  # 310, 1, 0/1
CODE_BUTTON_RIGHT_BUMPER = 311  # 311, 1, 0/1

CODE_BUTTON_LEFT_TRIGGER = 10 # 10, 3, 0-255
CODE_BUTTON_RIGHT_TRIGGER = 9  # 9, 3, 0-255

CODE_BUTTON_VIEW = 314  # 314, 1, 0/1
CODE_BUTTON_MENU = 315  # 315, 1, 0/1

class GamepadController:
    def __init__(self, debug=True):
        self._wait_until_connected()
        # {'event': [event_handlers]}
        self.events_callback = {'drive':[], 'servo0':[], 'servo1':[], 'fire':[]}

        # {'event': event_value}
        self.events_value = {'drive':None, 'servo0':None, 'servo1':None,
            'camera_onoff': None,
            'fire': None}
        self.queue = asyncio.Queue()
        self.debug = debug

    def _find_input_device(self):
        """
        multiple devices may present. e.g. a wireless mouse receiver.
        find the correct device.

        udevadm info --query=property --name=/dev/input/event4 | grep "ID_INPUT_JOYSTICK=1"
        """
    def _wait_until_connected(self, device='/dev/input/event0'):
        self.controller = None
        while self.controller is None:
            try:
                self.controller = InputDevice(device)
            except OSError as e:
                print(e)
                self.controller = None
                time.sleep(1)
        print('Controller connected')

    def register(self, event, callback):
        """
        run callback() when event happens
        """
        if event in self.events_callback and callback not in self.events_callback[event]:
            self.events_callback[event].append(callback)


    def unregister(self, event, callback):
        """
        remove callback()
        """
        if event in self.events_callback and callback in self.events_callback[event]:
            self.events_callback[event].remove(callback)

    async def random_event(self):
        while True:
            direction = random.choice(list(range(1, 5)))
            await self.queue.put(('drive', [direction, 100])) # moving
            await asyncio.sleep(0.5) # keep moving for 0.5 second
            await self.queue.put(('drive', [0, 100])) # stop
            await asyncio.sleep(random.randint(3600, 7200))  # sleep

    async def producer(self):
        # non-blocking
        while True:
            try:
                async for event in self.controller.async_read_loop():
                    #if event.code in [0,1,2,4,5]:  # no sticks
                    #    continue
                    if self.debug:
                        if event.value != 0:
                            print(f'code, type, value: {event.code}, {event.type}, {event.value}')
                        else:
                            print(f'{event.code} released, {event.value}')

                    if  event.code == CODE_PAD_HORIZONTAL or event.code == CODE_PAD_VERTICAL:

                        # either x!=0 or y!=0 or both != 0
                        x = event.value if event.code == CODE_PAD_HORIZONTAL else 0
                        y = event.value if event.code == CODE_PAD_VERTICAL else 0
                        direction = 0
                        if x == 0:  # y != 0
                            if y == -1:
                                direction = 1  # 'up'
                            elif y == 1:
                                direction = 2  # 'down'
                            else:
                                pass
                        elif y == 0:  # x != 0
                            if x == -1:
                                direction = 3  # 'left'
                            elif x == 1:
                                direction = 4  # 'right'
                            else:
                                pass
                        else:  # x != 0 and y != 0
                            if x == -1 and y == -1:  # up-left
                                direction = 5  # 'up-left'
                            elif x == -1 and y == 1:  # up-right
                                direction = 6  # 'up-right'
                            elif x == 1 and y == -1:  # down-left
                                direction = 7  # 'down-left'
                            else:
                                direction = 8  # 'down-right'
                        #driver.drive(direction)
                        directions = {
                            0: 'STOP',
                            1: 'UP',
                            2: 'DOWN',
                            3: 'LEFT',
                            4: 'RIGHT'
                        }
                        throttle = 100
                        self.events_value['drive'] = [direction, throttle]

                    #if  event.code == CODE_RIGHT_STICK_VERTICAL:
                        #self.events_value[event.code] = event.value
                    #    self.events_value['servo0'] = 1 if event.value > 127 else -1
                        #print(f'{event.value}\r')
                    #if  event.code == CODE_RIGHT_STICK_HORIZONTAL:
                    #    self.events_value['servo1'] = 1 if event.value > 127 else -1
                    #print('MOVE:', event.code, event.value)

                    """
                    if  event.code == CODE_RIGHT_STICK_HORIZONTAL:
                        #print('H:', event.code, event.value)
                        if event.value < 10:
                            self.events_value['servo1'] = -1
                        elif event.value > 245:
                            self.events_value['servo1'] = 1
                        else:
                            pass

                    if  event.code == CODE_RIGHT_STICK_VERTICAL:  # [0, 255]
                        if event.value < 10:
                            self.events_value['servo0'] = -1
                        elif event.value > 245:
                            self.events_value['servo0'] = 1
                        else:
                            pass
                    """
                    if  event.code == CODE_BUTTON_LEFT_BUMPER:
                        self.events_value['servo1'] = 1 if event.value else 0
                    if  event.code == CODE_BUTTON_RIGHT_BUMPER:
                        self.events_value['servo1'] = -1 if event.value else 0

                    if  event.code == CODE_BUTTON_LEFT_TRIGGER:
                        self.events_value['servo0'] = -1 if event.value else 0
                    if  event.code == CODE_BUTTON_RIGHT_TRIGGER:
                        self.events_value['servo0'] = 1 if event.value else 0
                    

                    if  event.code == CODE_BUTTON_A:
                        self.events_value['fire'] = event.value

                    #if  event.code == CODE_BUTTON_VIEW and event.value == 1:  # turn on / off camera
                    #    self.events_value['camera_onoff'] = 1 - self.events_value['camera_onoff']
                    #print(self.events_value)
                    
                    for evt, evt_value in self.events_value.items():
                        if evt_value is not None:
                            await self.queue.put((evt, evt_value))
                    #self.events_value = {}
                    #await asyncio.sleep(0)
                    #for evt, callbacks in self.events_callback.items():
                    #    for cb in callbacks:  # multiple callbacks on one event?
                    #        if self.events_value[evt] is not None:
                    #            cb(self.events_value[evt])
                    #            # reset all events
                    #            self.events_value[evt] = None
                #await asyncio.sleep(0)
            except OSError as e:  # when controller was poweroff
                print('Controller not connected')
                self._wait_until_connected()

    async def consumer(self):
        while True:
            evt, evt_value = await self.queue.get()
            for cb in self.events_callback[evt]:
                cb(evt_value)
            await asyncio.sleep(0)

    def close(self):
            pass


def drive(args):
    direction, throttle = args
    print('I am driving', direction, throttle)


if __name__ == '__main__':
    async def main():
        controller = GamepadController(debug=False)
        controller.register('drive', drive)
        try:
            producer = asyncio.create_task(controller.producer())
            consumer = asyncio.create_task(controller.consumer())
            #await asyncio.gather(producer)
            await producer
        except Exception as e:
            print(e)
        finally:
            pass
    asyncio.run(main())