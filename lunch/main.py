import jinja2
import asyncio
import os.path
import aiohttp_jinja2
from aiohttp import web

config = dict(host='127.0.0.1', port=9999)


@aiohttp_jinja2.template('main.jinja2')
def handler(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


async def init(loop, config):
    app = web.Application(loop=loop)
    folder = os.path.dirname(__file__) + '/templates'
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(folder))
    app.router.add_route('GET', '/', handler)

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
