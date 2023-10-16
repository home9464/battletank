### test camera

https://www.raspberrypi.com/documentation/computers/camera_software.html


```bash
# 10 seconds video
libcamera-vid -t 10000 -o test.h264
```

```python
import cv2
video_width=640
video_height=480
cap = cv2.VideoCapture(1)  # USB camera
cap.set(3, video_width)  # width, max 3280
cap.set(4, video_height)  # height, max 2464
cap.read()
```


# https://www.aranacorp.com/en/stream-video-from-a-raspberry-pi-to-a-web-browser/


