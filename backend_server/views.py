from aiohttp import web
import asyncio
import random
import datetime
import logging

# TODO убрать логирование в монго и перенести в файл

left = 1
right = 15


async def submit(request):
    data = await request.post()
    busytime = random.randint(left, right)
    _semaphore = request.app['semaphore']
    logger = logging.getLogger('my_logs')
    with (await _semaphore):
        logger.info("SUBMIT,accepted,uuid,%s,TIME,%d",
                    data['uuid'], 0)
        await asyncio.sleep(busytime)
        logger.info("SUBMIT,processed,uuid,%s,TIME,%d",
                    data['uuid'], busytime)
    return web.Response(body=b"ok")


async def extract(request):
    data = await request.post()
    busytime = random.randint(left, right)
    _semaphore = request.app['semaphore']
    logger = logging.getLogger('my_logs')

    with (await _semaphore):
        logger.info("EXTRACT,accepted,uuid,%s,TIME,%d",
                    data['uuid'], 0)
        await asyncio.sleep(busytime)
        logger.info("EXTRACT,processed,uuid,%s,TIME,%d",
                    data['uuid'], busytime)

    return web.Response(body=b"ok")

