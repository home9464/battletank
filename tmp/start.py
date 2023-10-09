import asyncio
import random
import time

async def start(myQueue):
    await myQueue.put(random.randint(1,5))

async def stop(myQueue):
    await myQueue.put(None)

async def runner(myQueue):
    item = await myQueue.get()  # block if Q is empty
    if :
    while item is None:
            break
        item = await myQueue.get()
        print("Consumer: {} consumed article with id: {}".format(id, item))
    print('Stopped')

async def main():

    myQueue = asyncio.Queue()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(runner(myQueue))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    await start(myQueue)
    time.sleep(3)
    await stop(myQueue)

    # Wait until the waiter task is finished.
    await waiter_task

asyncio.run(main())