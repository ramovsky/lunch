import json
import logging
import aiohttp
import aiohttp_jinja2
from aiohttp import web

from lunch.users import get_user


log = logging.getLogger(__name__)


@aiohttp_jinja2.template('main.jinja2')
async def index(request):
    return {}


@aiohttp_jinja2.template('places.jinja2')
async def places(request):
    return {}


class JsonRpc:

    def auth(self, user, id):
        return dict(sessions=[])


class ProtocolError(Exception):

    def __init__(self, msg):
        self.msg = msg


class WebSockHandler:

    def __init__(self, rpc=None):
        self._rpc = JsonRpc()

    async def __call__(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        while not ws.closed:
            msg = await ws.receive()
            if msg.tp == aiohttp.MsgType.text:
                log.info('WS msg received %s', msg.data)
                try:
                    answer = self._process_message(ws, msg.data)
                    ws.send_str(answer)
                except ProtocolError as e:
                    ws.send_str(e.msg)

            elif msg.tp == aiohttp.MsgType.close:
                log.info('websocket connection closed')
            elif msg.tp == aiohttp.MsgType.error:
                log.info('ws connection closed with exception %s' %
                      ws.exception())

        return ws

    def _process_message(self, ws, data):
        try:
            data = json.loads(data)
            assert type(data) == list
        except (ValueError, AssertionError):
            raise ProtocolError('wrong_command_format')

        command, args = data
        if command.startswith('_'):
            raise ProtocolError('wrong_command')

        if command == 'auth':
            id = args['id']
            ws.set_cookie('auth', id)

        try:
            method = getattr(self._rpc, command)
        except AttributeError:
            raise ProtocolError('unknown_method')

        user = get_user(ws.cookies['auth'].value)
        return json.dumps(method(user, **args))
