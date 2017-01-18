from aiohttp import web
import asyncio
import random
import datetime
import logging


left = 1
right = 5


async def handler(request):
    # do without semaphore
    data = await request.post()
    _semaphore = request.app['semaphore']
    logger = logging.getLogger('my_logs')
    _type = request.headers['X-Backtype']

    print(_semaphore._value)
    with (await _semaphore):
        if _type == 'heavy':
            busytime = random.randint(left, right)
        else:
            busytime = 1
        await asyncio.sleep(busytime)
        logger.info("OK,TYPE,{},TIME,{}".format(_type, busytime))
    print("{} -- {}, processed".format(datetime.datetime.today().strftime("%H:%M:%S"), _type))
    return web.Response(body=b"ok")
