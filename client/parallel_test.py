import grequests
import requests
import logging
import uuid
import random
import time
import socket
import datetime
from django.utils.encoding import smart_str, smart_text

DEBUG = False

if DEBUG:
    suffix = ""
    store = ""
else:
    suffix = "/logs/"
    store = "/client/"

logging.basicConfig(format="%(levelname)s,%(asctime)s,%(message)s",
                    filename=suffix+"client_{0}_{1}.log".format(socket.gethostname(),
                                                   datetime.datetime.now().strftime("%d%m_%H%M")))
# BASE_URL = 'http://node_frontend:8000'
BASE_URL = 'http://172.18.1.10:8000'
# BASE_URL = 'http://localhost:8000'


def elapsed(r, *args, **kwargs):
    logging.warning("Request,Success,Elapsed,%s,Status,%s,URL,%s", r.elapsed, r.status_code, r.url)


def exception_handler(request, exception):
    logging.warning("Request,Failed,%s", exception)


_ids = [uuid.uuid1() for x in range(5)]
counts = [x for x in range(10)]

megalist = list(zip(_ids, counts))

while True:
    reqs = [grequests.post(BASE_URL + "/submit/",
                           data={
                               'password': smart_str(u'protect_me'),
                               'payload': smart_str(u'Illusion of security'),
                               'commit': smart_str(u'Вкрапить / Embed'),
                           },
                           files={'docfile': (
                           'payload.pdf', open(store+'payload.pdf', 'rb'), 'application/pdf', {'Expires': '0'})},
                           hooks=dict(response=elapsed))
            if y % 2 == 0 else
            grequests.post(BASE_URL + "/extract/",
                           data={
                               'password': smart_str(u'protect_me'),
                               'commit': smart_str(u'Извлечь / Extract')
                           },
                           files={'docfile': (
                           'payload.pdf', open(store+'payload.pdf', 'rb'), 'application/pdf', {'Expires': '0'})},
                           hooks=dict(response=elapsed))
            for (x, y) in megalist]

    grequests.map(reqs, exception_handler=exception_handler)
    time.sleep(random.randint(10, 20))
