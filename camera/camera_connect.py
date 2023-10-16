#pylint: disable=missing-docstring, C0301, E1101, W0703

"""
# 1. install dependencies
sudo apt install -y libatlas-base-dev
pip install opencv-python==3.4.17.61
pip install numpy==1.22.2
pip install schedule==1.1.0


# 2. autostart when system rebooted

```bash
# 1. use contab
crontab -e
# 2. append this line to the end, save then exit
@reboot /usr/bin/python /home/pi/Desktop/pi_cam_stream_client.py
# 3. reboot the board
```

# 3. enable camera
```bash
sudo raspi-config
"3. Interface Options"  -> "I1 Legacy Camera" -> "Yes" -> "Finish" -> "Reboot"
```

"""
import os
import sys
import time
import asyncio
import datetime
import socket
import logging

import cv2

assert sys.version_info >= (3, 5, 2)

# send video stream to this server (Coral Dev Board Mini) for image processing
SERVER_IP = '10.0.0.35'
SERVER_PORT = 8888

#from station import RemoteControlWeaponSystem

async def action_worker(rcws, queue):
    """act upon an instruction retrieved from a Queue
    """
    while True:
        item = await queue.get()
        x, y = item.strip().split(',')
        if not (x == 'None' and y == 'None'):
            x_offset = int(x)
            y_offset = int(y)
            print(f'offset: x: {x_offset}, y: {y_offset}')
            if abs(x_offset) <= 40 and abs(y_offset) <= 40:
                rcws.shoot()
                print('shoot')
            rcws.left() if x_offset > 0 else rcws.right()
            rcws.up() if y_offset > 0 else rcws.down()
        # Notify the queue that the "work item" has been processed.
        queue.task_done()


async def connect_server() -> None:
    """connect to remote server which will receive the image, analyze the image and return instructions based on the image
    (e.g. move gun (x,y) then fire upon a suspected object)
    """
    while True:
        try:
            print(f'connect server -> {SERVER_IP}:{SERVER_PORT}')
            reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
            return reader, writer
        except Exception as err:
            print(f'failed to connect server -> {err}')
        await asyncio.sleep(1)

async def read_frame(data:list, reader, payload_size):
    """to be used by remote server to decode the frame sent from this client
    """
    content = data[0]
    while len(data[0]) < payload_size:
        packet = await reader.read(4*1024) # 4K
        if not packet:
            break
        data[0] += packet
    packed_msg_size = data[0][:payload_size]
    data[0] = data[0][payload_size:]
    msg_size = struct.unpack(">L",packed_msg_size)[0]

    while len(data) < msg_size:
        data[0] += await reader.read(4*1024)
        
    frame_data = data[0][:msg_size]
    data[0] = data[0][msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    return cv2.imdecode(frame, cv2.IMREAD_COLOR) if frame is not None else frame


async def camera_streaming(event, queue) -> None:
    """
    start streamning if event.set() is called
    stop streamning if event.clear() is called
    supported resolution:
    
    480*640,
    720*1080
    1080*1920

    max_width = 3280
    max_height = 2464
    """
    start_time = time.time()
    #video_width=1280
    #video_height=720
    video_width=640
    video_height=480
    #video_width=1920
    #video_height=1080

    video_color_gray=False
    frame_reader, frame_writer = await connect_server()
    print('server connected')

    # start camera
    cap = cv2.VideoCapture(0)
    cap.set(3, video_width)  # width, max 3280
    cap.set(4, video_height)  # height, max 2464
    #cap.set(5, 24)  # 1 Frames Per Second
    cap.set(5, 1)  # 1 Frames Per Second
    print('camera connected???')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    in_data = [b""]
    payload_size = struct.calcsize(">L")
    while await event.wait():
        try:
            _, frame = cap.read()
            print(frame.shape)
            if video_color_gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
            #print(frame.shape)
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            out_data = pickle.dumps(frame, 0)
            #frame = cv2.flip(frame, 0)  # 0, vertical flip, -1 horizontally and vetically 
            # send the raw image to remote server for processing and expecting instructions
            out_data = struct.pack(">L", len(out_data)) + out_data
            frame_writer.write(out_data)
            #print(len(out_data))
            #await frame_writer.drain()
            # wait for instructions from the remote server 
            #in_data = await frame_reader.read(64)
            #queue.put_nowait(in_data.decode())
            """
            in_frame = read_frame(in_data, reader, payload_size)
            if in_frame is not None:
                cv2.imshow('jpg', in_frame)
                cv2.waitKey(1)
            """
        except Exception as err:
            print(err)
            frame_reader, frame_writer = await connect_server()

    cap.release()
    cv2.destroyAllWindows()
    frame_writer.close()
    await frame_writer.wait_closed()


async def main():
    queue = asyncio.Queue()
    event = asyncio.Event()

    tasks = []
    camera_task = asyncio.create_task(camera_streaming(event, queue))
    tasks.append(camera_task)

    print('Started')
    event.set()
    await asyncio.sleep(3)  # let is run for 10 seconds
    await asyncio.gather(*tasks, return_exceptions=True)
    #waiter_task.cancel()
    """
    event.clear()
    print('Stopped')
    await asyncio.sleep(3)  # let is run for 10 seconds
    print('Started')
    event.set()
    await asyncio.sleep(3)  # let is run for 10 seconds
    #waiter_task.cancel()
    event.clear()
    print('Stopped')
    await waiter_task
    """

if __name__ == '__main__':
    asyncio.run(main())
