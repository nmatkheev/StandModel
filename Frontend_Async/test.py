import asyncio

sem = asyncio.Semaphore(1)

async def acquire():
    for x in range(2):
        await sem
        print(x)

loop = asyncio.get_event_loop()
loop.run_until_complete(acquire())