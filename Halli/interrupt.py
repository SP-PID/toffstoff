import asyncio
import board
import countio

stop = False

async def catch_interrupt(pin):
    global stop
    """Print a message when pin goes low."""
    with countio.Counter(pin) as interrupt:
        while True:
            if interrupt.count > 0:
                interrupt.count = 0
                print("interrupted!")
                stop = True
            await asyncio.sleep(0)

async def print_forever():
    global stop
    while True:
        if stop:
            break
        print("I´m a robot, FUCK YEAH..")
        await asyncio.sleep(0.2)

async def main():
    interrupt_task = asyncio.create_task(catch_interrupt(board.D2))
    normal_task = asyncio.create_task(print_forever())
    await asyncio.gather(interrupt_task)

asyncio.run(main())