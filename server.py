from aiohttp import web

from screenshoter import get_screenshot


async def screen_server(request):
    url = request.rel_url.query['url']
    screen = get_screenshot(url)
    return web.Response(body=screen, content_type='image/jpeg')


app = web.Application()
app.router.add_route('GET', '/', screen_server)