import jinja2
import asyncio
import os.path
import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .handlers import index, WebSockHandler


config = dict(host='127.0.0.1', port=9999)


async def init(loop, config):
    app = web.Application(
        loop=loop,
        middlewares=[session_middleware(
            EncryptedCookieStorage(b'12345678901234561234567890123456'))]
    )

    folder = os.path.dirname(os.path.dirname(__file__))
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(folder+ '/templates'))
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/ws/', WebSockHandler())
    app.router.add_static('/static/', folder + '/static')

    srv = await loop.create_server(app.make_handler(),
                                   **config)
    return srv


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, config))
    print("Server started at http://{host}:{port}".format(**config))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
