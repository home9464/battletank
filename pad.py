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

import pprint
import pygame
import threading

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
        self.events = {
            'drive':None, 'turret_left_right':None, 'gun_up_down':None, 'fire':None
        }

        # callback funcs on interested events
        self.events_callback = {k:[] for k in self.events}
        #print(self.events_callback)


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
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            event = pygame.event.wait()
            print(event)
            """
            #for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    #self.axis_data[event.axis] = round(event.value,2)
                    if event.axis == GoogleStadiaController.AXIS_2_X:
                        self.events['turret_left_right'] = round(event.value, 2)
                    if event.axis == GoogleStadiaController.AXIS_2_Y:
                        self.events['gun_up_down'] = round(event.value, 2)
                    #if event.axis == GoogleStadiaController.AXIS_TRIGGER_X:
                    #    self.event_value['gun_x'] = event.value
                    #if event.axis == GoogleStadiaController.AXIS_TRIGGER_Y:
                    #    self.event_value['gun_y'] = event.value
                elif event.type == pygame.JOYBUTTONDOWN:
                    #self.button_data[event.button] = True
                    if event.button == GoogleStadiaController.BUTTON_A:
                        self.events['fire'] = True
                elif event.type == pygame.JOYBUTTONUP:
                #    self.button_data[event.button] = False
                    if event.button == GoogleStadiaController.BUTTON_A:
                        self.events['fire'] = False
                elif event.type == pygame.JOYHATMOTION:
                    #self.hat_data[event.hat] = event.value
                    self.events['drive'] = event.value
                await asyncio.sleep(0)
            """

    async def execute(self):
        #index = 0
        while True:
            print('CONSUME')
            #os.system('clear')
            #print(index, self.events)
            #index += 1
            #turn = 0.0
            for evt, callbacks in self.events_callback.items():
                for cb in callbacks:  # multiple callbacks on one event?
                    if self.events[evt] is not None:
                        cb(self.events[evt])
                        #self.events[evt] = None            
            await asyncio.sleep(0)

def controller_main():
    ps4 = GoogleStadiaController()
    ps4.init()
    ps4.listen()

def drive(args):
    direction, throttle = args
    print('I am driving', direction, throttle)

def fire(args):
    print('Fire!!!!', args)

INDEX1  = 0
INDEX2  = 0
def move_turret(args):
    global INDEX1
    if -0.3 > args or args > 0.3:
        print(INDEX1, 'turret', args)
        INDEX1 += 1

def move_gun(args):
    global INDEX2
    print(INDEX2, 'gun', args)
    INDEX2 += 1

async def main():
    stadia = GoogleStadiaController()
    stadia.init()
    stadia.register('drive', drive)
    stadia.register('turret_left_right', move_turret)
    #stadia.register('gun_up_down', move_gun)
    #stadia.register('fire', fire)
    stadia.listen()
    try:
        listener = asyncio.create_task(stadia.listen())
        executor = asyncio.create_task(stadia.execute())
        await listener
    except Exception as e:
        print(e)
    finally:
        pass
    

if __name__ == '__main__':
    asyncio.run(main())
