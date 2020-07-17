import logging
from rq import Queue
from redis import Redis

from aiohttp import web
from screenshoter import get_screenshot

redis_conn = Redis()
queue = Queue(connection=redis_conn)


FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=10,
    filename='logs/server/server.log',
    filemode='a',
)


async def screen_server(request):
    params = request.rel_url.query
    url = params.get('url')
    id = params.get('id')
    token = params.get('token')
    request_url = params.get('host')

    if url is None or id is None or token is None or request_url is None:
        return web.HTTPBadRequest(text='Нужные параметры отсутствуют')

    queue.enqueue(
        get_screenshot,
        args=(id, url, token, request_url),
        result_ttl=0,
        job_timeout=30
    )

    return web.HTTPOk(text='Ваш запрос принят')


app = web.Application()
app.router.add_route('GET', '/', screen_server)
