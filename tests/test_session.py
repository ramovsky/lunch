import sys
import json
import asyncio
import aiohttp
import unittest

sys.path.append('..')

from lunch.main import init


config = dict(host='127.0.0.1', port=8091)


class TestSession(unittest.TestCase):

    def setUp(self):
        asyncio.set_event_loop(None)
        loop = asyncio.new_event_loop()
        self.run = loop.run_until_complete
        self._srv = self.run(init(loop, config))
        self._client = aiohttp.ClientSession(loop=loop)
        self._loop = loop

    def tearDown(self):
        self._client.close()
        self._srv.close()
        self.run(self._srv.wait_closed())
        self._loop.stop()
        self._loop.run_forever()
        self._loop.close()

    async def communicate(self, url, data={}, method='GET', code=200):
        args = {}
        if data:
            args['data'] = json.dumps(data).encode('utf-8')
            args['headers'] = {'Content-Type': 'application/json'}

        response = await self._client.request(
            method,
            'http://{host}:{port}{url}'.format(url=url, **config),
            **args)
        self.assertEqual(code, response.status)
        data = await response.text()
        return data

    def test_shit(self):
        print(self.run(self.communicate('/')))

    def test_shit2(self):
        print(self.run(self.communicate('/')))
