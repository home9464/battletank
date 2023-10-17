"""
Buttons:

0 - A
1 - B
2 - X
3 - Y
4 - left shoulder button
5 - right shoulder button
6 - SYS
7 - Menu
11 - Stadia
12 - Box

"""
import os
# this will fool the system to think it has video access
os.environ["SDL_VIDEODRIVER"] = "dummy"

import asyncio
import time

import pprint
import pygame
import threading


from turret import Turret
turretter = Turret()

class GoogleStadiaController:
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_X = 2
    BUTTON_Y = 3

    # 0: left axis: x, [-1, 1] 
    # 1: left axis: y, [-1, 1] 
    # 2: right axis: x, [-1, 1] 
    # 3: right axis: y, [-1, 1] 
    # 4: right trigger, [-1, 1], 
    # 5: left trigger, [-1, 1]

    AXIS_1_X = 0
    AXIS_1_Y = 1

    AXIS_2_X = 2
    AXIS_2_Y = 3

    AXIS_TRIGGER_X = 4
    AXIS_TRIGGER_Y = 5

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        # what events
        self.events = {'drive':None, 'move_gun':None, 'fire_gun':None, 'camera': None}

        # callback funcs on interested events
        self.events_callback = {k:[] for k in self.events}

        self.axis_left = {}

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

    async def listen(self):
        """Listen for events to happen"""
        index = 0 
        clock = pygame.time.Clock()
        while True:
            #event = pygame.event.wait() # blocking
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    #self.axis_left[event.axis] = int((int(event.value * 100) + 100) / 1.12)  # [-100, 100] -> [0, 180]
                    self.axis_left[event.axis] = event.value
            """
            for evt, callbacks in self.events_callback.items():
                for cb in callbacks:  # multiple callbacks on one event?
                    if self.events[evt] is not None:
                        cb(self.events[evt])
                        self.events[evt] = None
            """
            #pygame.event.clear()
            #print(index, self.events['move_gun'])
            #index += 1
            await asyncio.sleep(0)

    async def action(self):
        """Listen for events to happen"""
        x_offset = 0
        y_offset = 0

        slow_down_scale = 800
        while True:
            x = self.axis_left.get(2, 0)
            y = self.axis_left.get(3, 0)
            x_offset += x
            if x_offset <= -slow_down_scale or x_offset >= slow_down_scale:
                turretter.horizontal(x_offset // slow_down_scale)
                x_offset = 0
            
            y_offset += y
            if y_offset <= -slow_down_scale or y_offset >= slow_down_scale:
                turretter.vertical(y_offset // slow_down_scale)
                y_offset = 0
            await asyncio.sleep(0)


def controller_main():
    ps4 = GoogleStadiaController()
    ps4.init()
    ps4.listen()

def drive(args):
    direction, throttle = args
    print('I am driving', direction, throttle)

async def main():
    stadia = GoogleStadiaController()
    stadia.init()
    #stadia.register('drive', drive)
    try:
        task1 = asyncio.create_task(stadia.listen())
        task2 = asyncio.create_task(stadia.action())
        await task1
    except Exception as e:
        print(e)
    finally:
        pass
    

if __name__ == '__main__':
    asyncio.run(main())
