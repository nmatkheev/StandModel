from aiohttp import web, ClientSession
import asyncio
import random
from datetime import datetime
import logging
import requests

left = 1
right = 15

async def fetch(url, data, headers):
    async with ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            resp = await response.read()
            print("{} -- {}, processed".format(datetime.today().strftime("%H:%M:%S"), response.url))
            return datetime.now()


async def bound_fetch(url, _t1, data, headers):
    try:
        _t2 = await fetch(url, data, headers)
        _elapsed = (_t2 - _t1).seconds + (_t2 - _t1).microseconds * 1e-6
        return _elapsed
    except Exception as e:
        print(e)
        return -1


async def handler(request):
    data = await request.post()
    _semaphore = request.app['semaphore']
    _backends = request.app['backends']

    reqtype = 'heavy' if 'submit' in request.url.path else 'light'
    url = _backends['heavy'] if 'submit' in request.url.path else _backends['light']

    logger = logging.getLogger('my_logs')
    _t1 = datetime.now()
    with (await _semaphore):
        _elapsed = await bound_fetch(url, _t1, data=data, headers={'X-Backtype': reqtype})
        if _elapsed != -1:
            logger.info("OK,TYPE,{},TIME,{}".format(reqtype, _elapsed))
            return web.Response(body=b"ok")
        else:
            logger.info("FAIL,TYPE,{},TIME,".format(reqtype))
            return web.HTTPBadRequest()


