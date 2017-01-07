import os
import grequests
import requests
import logging
import uuid
import random
import time
import socket
import datetime
from django.utils.encoding import smart_str

DEBUG = False

if DEBUG:
    suffix = ""
    store = ""
else:
    suffix = "/logs/"
    store = "/client/"

logging.basicConfig(format="%(levelname)s,%(asctime)s,%(message)s",
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=suffix+"client_{0}_{1}.log".format(socket.gethostname(),
                                                   datetime.datetime.now().strftime("%d%m_%H%M")))

if DEBUG:
    BASE_URL = 'http://localhost:8000'
else:
    BASE_URL = 'http://node.frontend.com:8000'


def elapsed(r, *args, **kwargs):
    logging.warning("Request,Success,uuid,%s,Elapsed,%s,Status,%s,URL,%s", "", r.elapsed.seconds, r.status_code, r.url)


def exception_handler(request, exception):
    _uuid = str(request.kwargs['data']['uuid'])
    logging.warning("Request,Failed,uuid,%s,Elapsed,0,Status,0,URL,%s", _uuid, request.url)

try:
    N = int(os.environ['CONCURRENCY'])
except:
    N = 10

megalist = [x for x in range(N)]

while True:
    reqs = [
            grequests.post(BASE_URL + "/submit/",
                           data={
                               'password': smart_str(u'protect_me'),
                               'payload': smart_str(u'Illusion of security'),
                               'uuid': uuid.uuid1(),
                               'commit': smart_str(u'Вкрапить / Embed'),
                           },
                           files={'docfile': (
                           'payload.pdf', open(store+'payload.pdf', 'rb'), 'application/pdf', {'Expires': '0'})},
                           hooks=dict(response=elapsed))
            if y % 2 == 0 else
            grequests.post(BASE_URL + "/extract/",
                           data={
                               'password': smart_str(u'protect_me'),
                               'uuid': uuid.uuid1(),
                               'commit': smart_str(u'Извлечь / Extract')
                           },
                           files={'docfile': (
                           'payload.pdf', open(store+'payload.pdf', 'rb'), 'application/pdf', {'Expires': '0'})},
                           hooks=dict(response=elapsed))
            for y in megalist]

    grequests.map(reqs, exception_handler=exception_handler)
    time.sleep(random.randint(10, 20))
