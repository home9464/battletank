#111!/usr/bin/env python
# -*- coding: utf-8 -*

#sudo apt-get install python3-flask
#pip3 install opencv-python
import asyncio

from flask import Flask, render_template, Response
import cv2

cam_app = Flask(__name__)
#app.config["CACHE_TYPE"] = "null"

@cam_app.route('/')
async def index():
    """Video streaming home page."""
    await asyncio.sleep(0)
    return render_template('./index.html')

def gen():
    video_width=640
    video_height=480
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)  # USB camera
    vs.set(3, video_width)  # width, max 3280
    vs.set(4, video_height)  # height, max 2464
    while True:
        ret,frame=vs.read()
        if ret==True and frame is not None:
            frame = cv2.circle(frame, (video_width//2, video_height//2), 200, (0,0,255), thickness=2, lineType=8, shift=0)
            frame = cv2.flip(frame, 0)
            x_point1 = ((video_width//2)-20, video_height//2)
            x_point2 = ((video_width//2)+20, video_height//2)
            y_point1 = (video_width//2, (video_height//2)-20)
            y_point2 = (video_width//2, (video_height//2)+20)
            cv2.line(frame, x_point1, x_point2, (0, 0, 255), 3)  #crosshair horizontal
            cv2.line(frame, y_point1, y_point2, (0, 0, 255), 3)  #crosshair horizontal
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame=jpeg.tobytes()
            #await asyncio.sleep(0)
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
    vs.release()
    cv2.destroyAllWindows() 

@cam_app.route('/video_feed')
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    #loop = asyncio.get_event_loop()
    #result = loop.run_until_complete()
    await asyncio.sleep(0)
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
