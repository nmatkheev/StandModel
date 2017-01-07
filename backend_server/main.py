import asyncio
import logging
import logging.config
import sys
import datetime
import socket

from aiohttp import web
from routes import setup_routes
from log_config import LOGGING
import os

try:
    CONCURRENT_REQ = int(os.environ['REQ_CONCUR'])
    PORT = int(sys.argv[1])
except:
    CONCURRENT_REQ = 1
    PORT = 8080


def init(loop):
    app = web.Application(loop=loop)
    setup_routes(app)
    app['semaphore'] = asyncio.Semaphore(CONCURRENT_REQ)
    return app


filename = socket.gethostname()+"_"+datetime.datetime.now().strftime("%d%m%y_%H%M%S")+".log"

logging.config.dictConfig(LOGGING)
loop = asyncio.get_event_loop()
app = init(loop)
web.run_app(app, port=PORT)
