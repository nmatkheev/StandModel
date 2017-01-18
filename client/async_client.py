import os
import asyncio
import logging
from aiohttp import ClientSession
from datetime import datetime
from random import shuffle

DEBUG = False

logger = logging.getLogger()

if DEBUG:
    handler = logging.StreamHandler()
    root = ''
else:
    suffix = '/logs/'
    root = '/client/'
    handler = logging.FileHandler(filename=suffix+"client_{0}.log".format(datetime.now().strftime("%d%m_%H%M")))

formatter = logging.Formatter("%(levelname)s,%(asctime)s,%(message)s", datefmt='%d/%m/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


async def fetch(url, session):
    _t1 = datetime.now()
    if 'submit' in url:
        data = {
            'password': b'protect_me',
            'payload': b'Illusion of security',
            'file': open(root+'payload.pdf', 'rb')
        }
    else:
        data = {
            'password': b'protect_me',
            'file': open(root+'payload.pdf', 'rb')
        }
    async with session.post(url, data=data) as response:
    # async with session.get(url) as response:
        resp = await response.read()
        print("{} -- {}, processed".format(datetime.today().strftime("%H:%M:%S"), response.url))
        # return datetime.now()
        return datetime.now()-_t1

async def bound_fetch(sem, url, session):
    # async with sem:

    _reqtype = 'heavy' if 'submit' in url else 'light'
    try:
        print("{} -- {}, pending".format(datetime.today().strftime("%H:%M:%S"), url))
        _t2 = await fetch(url, session)
        # _elapsed = (_t2 - _t1).seconds + (_t2 - _t1).microseconds * 1e-6
        _elapsed = _t2.seconds + _t2.microseconds * 1e-6
        logging.warning("Success,Elapsed,{},Type,{}".format(_elapsed, _reqtype))
        return _reqtype, _elapsed
    except Exception as e:
        logging.exception(e, exc_info=True)
        logging.warning("Failed,Elapsed,,Type,{}".format(_reqtype))
        return _reqtype, 0.

async def run(_plan):
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(concurrency)
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for url in _plan:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
        return responses.result()

# to be in env vars:
if DEBUG:
    base_url = "http://172.18.1.10:8080/{}"
    # base_url = "http://localhost:8080/{}"
    # base_url = "http://pdf.stego.su/{}"
    overall_num = 10
    heavy_ratio = 0.5
    concurrency = 10
else:
    base_url = os.environ.get("FRONT")
    overall_num = int(os.environ.get("OVERALL"))
    heavy_ratio = float(os.environ.get("HEAVY_RATIO"))
    concurrency = int(os.environ.get("CONCURRENCY"))
# =================
plan = [base_url.format('submit') for x in range(int(overall_num * heavy_ratio))]
plan.extend([base_url.format('extract') for x in range(int(overall_num - overall_num * heavy_ratio))])
shuffle(plan)

loop = asyncio.get_event_loop()
_responses = loop.run_until_complete(run(plan))
print(_responses)
