import logging
import os
import subprocess

from aiohttp import web


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

    if url is None or id is None or token is None:
        return web.HTTPBadRequest(text='Нужные параметры отсутствуют')

    try:
        dirname = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(dirname, 'screenshoter.py')
        subprocess.run(
            ['python', f'{script_path}', f'{id}', f'{url}', f'{token}', '&'],
            shell=True,
            timeout=60
        )
    except subprocess.SubprocessError as e:
        return web.HTTPInternalServerError(text=f'Ошибка на сервере: {e}')

    return web.HTTPOk(text='Ваш запрос принят')


app = web.Application()
app.router.add_route('GET', '/', screen_server)
