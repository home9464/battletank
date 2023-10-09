"""

libvpx-dev libopus-dev

linux-libc-dev,
libavcodec-dev,
libavdevice-dev,
libavfilter-dev,
libavformat-dev,
libavresample-dev,
libavutil-dev,
libv4l-dev,
"""
#pylint: disable=missing-docstring, C0301, E1101, W0703

import os
import sys
import time
import asyncio
import datetime
import struct
import pickle

import cv2

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8888

async def read_frame(data:list, reader, payload_size):
    content = data[0]
    while len(content) < payload_size:
        packet = await reader.read(4*1024) # 4K
        if not packet:
            break
        content += packet
    packed_msg_size = content[:payload_size]
    content = content[payload_size:]
    msg_size = struct.unpack(">L",packed_msg_size)[0]

    while len(content) < msg_size:
        content += await reader.read(4*1024)
        
    frame_data = content[:msg_size]
    data[0] = content[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    return cv2.imdecode(frame, cv2.IMREAD_COLOR) if frame is not None else frame


async def handle_cam(reader, writer):
    """called whenever a new client connection is established
    """
    data = b""
    payload_size = struct.calcsize(">L")
    print(payload_size)
    while True:
        try:
            #frame = await read_frame(data, reader, payload_size)
            while len(data) < payload_size:
                packet = await reader.read(512*1024) # 4K
                if not packet:
                    break
                data += packet
            if not data:
                continue
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L",packed_msg_size)[0]

            while len(data) < msg_size:
                data += await reader.read(512*1024)
        
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            
            if frame is not None:
                #frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                #(video_height, video_width, channels) = frame.shape
                print(frame.shape)
                #cv2.imshow('jpg', frame)
                #cv2.waitKey(1)
            #await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionResetError, ConnectionAbortedError) as err:
            #asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of undefined expected bytes
            raise err

        except Exception as err:
            raise err
            #cv2.destroyAllWindows()

async def main():
    """main entrypoint

    """
    while True:
        try:
            server = await asyncio.start_server(handle_cam,
                                        SERVER_IP,
                                        SERVER_PORT,
                                        limit=1024*1024*8)
            print(f'Serving on {SERVER_IP}:{SERVER_PORT}')
            async with server:
                await server.serve_forever()
        except Exception as err:  # try to recover from any exceptions by re-establishing connection
            print(f'Unhandled: {err}')
    #print(dir(server))
    #await asyncio.sleep(60)
    #server.close()
    #await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
