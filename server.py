from aiohttp import web

from screenshoter import get_screenshot


async def screen_server(request):
    try:
        url = request.rel_url.query['url']
        screen = get_screenshot(url)
    except Exception:
        return web.Response(text="Hello, world")
    return web.Response(body=screen, content_type='image/jpeg')


app = web.Application()
app.router.add_route('GET', '/', screen_server)