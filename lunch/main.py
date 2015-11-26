import jinja2
import logging
import asyncio
import aiohttp_jinja2
from aiohttp import web

import lunch.config as config
from lunch.handlers import index, WebSockHandler


logging.basicConfig(level=logging.DEBUG)


async def init(loop, config):
    app = web.Application(loop=loop)

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(config.templates_dir)
    )
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/ws/', WebSockHandler())
    app.router.add_static('/static/', config.static_dir)

    srv = await loop.create_server(app.make_handler(), **config.host)
    return srv


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop, config))
    print("Server started at http://{host}:{port}".format(**config.host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
