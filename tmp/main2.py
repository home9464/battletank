import sys
import random
import functools
import asyncio

from camera import cam_app

async def main():
    print("press Ctl-C to exit")
    try:
        camera_straming = asyncio.create_task(cam_app.run(host='0.0.0.0', port=5000, debug=True, threaded=False))
        await camera_straming
        #await controller_consumer
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        pass

if __name__ == '__main__':
    asyncio.run(main())
