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
import pickle
import struct

import cv2

assert sys.version_info >= (3, 5, 2)

# send video stream to this server (Coral Dev Board Mini) for image processing
SERVER_IP = '10.0.0.35'
SERVER_PORT = 8888

async def connect_server() -> None:
    """connect to server
    """
    while True:
        try:
            print(f'connect server -> {SERVER_IP}:{SERVER_PORT}')
            reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
            return reader, writer
        except Exception as err:
            print(f'failed to connect server -> {err}')
        await asyncio.sleep(1)


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
    video_width=1280
    video_height=720
    #video_width=640
    #video_height=480
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
    print('camera connected')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    while await event.wait():
        try:
            _, frame = cap.read()
            if video_color_gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            out_data = pickle.dumps(frame, 0)

            #frame = cv2.flip(frame, 0)  # vertical flip
            #frame = cv2.flip(frame, -1)  # flip both horizontally and vetically 

            # send the raw image to remote server for processing and expecting instructions
            out_data = pickle.dumps(frame)
            out_data = struct.pack(">L", len(out_data)) + out_data
            frame_writer.write(out_data)
            #print(len(out_data))
            #await frame_writer.drain()
            # wait for instructions from the remote server 
            #in_data = await frame_reader.read(64)
            #queue.put_nowait(in_data.decode())
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
