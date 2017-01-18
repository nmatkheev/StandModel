import asyncio
import logging
import logging.config
import sys
import datetime
import socket
__package__ = ''
from aiohttp import web
from routes import setup_routes
from log_config import LOGGING, DEBUG
import os

if not DEBUG:
    CONCURRENT_REQ = int(os.environ['REQ_CONCUR'])
    PORT = int(sys.argv[1])
    light_back = os.environ['light']
    heavy_back = os.environ['heavy']
else:
    CONCURRENT_REQ = 1
    # PORT = int(sys.argv[1])
    PORT = 8080
    light_back = 'http://localhost:8081'
    heavy_back = 'http://localhost:8082'


def init(loop):
    app = web.Application(loop=loop)
    setup_routes(app)
    app['backends'] = {'heavy': heavy_back, 'light': light_back}
    return app


logging.config.dictConfig(LOGGING)
loop = asyncio.get_event_loop()
app = init(loop)
web.run_app(app, port=PORT)
