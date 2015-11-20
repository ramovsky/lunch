import json
import logging
import aiohttp
import aiohttp_jinja2
from aiohttp import web


log = logging.getLogger(__name__)


@aiohttp_jinja2.template('main.jinja2')
async def index(request):
    return {}


class JsonRpc:

    def hello(self):
        return 'hello'


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
                    answer = self._process_message(msg.data)
                    ws.send_str(answer)
                except ProtocolError as e:
                    ws.send_str(e.msg)

            elif msg.tp == aiohttp.MsgType.close:
                log.info('websocket connection closed')
            elif msg.tp == aiohttp.MsgType.error:
                log.info('ws connection closed with exception %s' %
                      ws.exception())

        return ws

    def _process_message(self, data):
        try:
            data = json.loads(data)
            assert type(data) == list
        except (ValueError, AssertionError):
            raise ProtocolError('wrong_command_format')

        command, *args = data
        if command.startswith('_'):
            raise protocolError('wrong_command')

        try:
            method = getattr(self._rpc, command)
        except AttributeError:
            raise ProtocolError('unknown_method')

        return method(*args)
