import asyncio
import logging
import logging.config
import sys
import datetime
import socket

from aiohttp import web
from routes import setup_routes
from log_config import get_logconf, DEBUG
import os


if not DEBUG:
    CONCURRENT_REQ = int(os.environ['REQ_CONCUR'])
    PORT = int(sys.argv[1])
else:
    CONCURRENT_REQ = 1
    PORT = int(sys.argv[1])


def init(loop):
    app = web.Application(loop=loop)
    setup_routes(app)
    app['semaphore'] = asyncio.Semaphore(CONCURRENT_REQ)
    return app


logging.config.dictConfig(get_logconf(PORT))
loop = asyncio.get_event_loop()
app = init(loop)
web.run_app(app, port=PORT)
