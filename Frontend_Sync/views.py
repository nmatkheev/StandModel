from aiohttp import web
import asyncio
import random
from datetime import datetime
import logging
import requests

left = 1
right = 15


async def handler(request):
    data = await request.post()
    _semaphore = request.app['semaphore']
    _backends = request.app['backends']

    reqtype = 'heavy' if 'submit' in request.url.path else 'light'
    url = _backends['heavy'] if 'submit' in request.url.path else _backends['light']

    logger = logging.getLogger('my_logs')
    _t1 = datetime.now()
    print("Accepted operation. To go: {}, time: {}".format(url,_t1.strftime("%H:%M:%S")))
    with (await _semaphore):
        try:
            r = requests.post(url, data=data, headers={'X-Backtype': reqtype})
            _t2 = datetime.now()
            td = _t2 - _t1
            elaps = td.seconds + td.microseconds * 1e-6
            logger.info("OK,TYPE,{},TIME,{}".format(reqtype, elaps))
            return web.Response(body=b"ok")
        except Exception as e:
            print(e)
            logger.info("FAIL,TYPE,{},TIME,".format(reqtype))
            return web.HTTPBadRequest()  # Response(body=b"bad")


