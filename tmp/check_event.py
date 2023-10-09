import asyncio

COUNTER = 0
async def waiter(event):
    global COUNTER
    print('waiting for it ...')
    while await event.wait():
        COUNTER += 1
        #print('HELLO', COUNTER)
        await asyncio.sleep(0)
    print('CELAR')

async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    event.set()
    await asyncio.sleep(1)  # let is run for 3 seconds
    print('WORLD')
    #waiter_task.cancel()
    event.clear()
    #waiter_task.cancel()
    #await asyncio.sleep(3)
    # Wait until the waiter task is finished.
    print('Never finish')
    await waiter_task

asyncio.run(main())