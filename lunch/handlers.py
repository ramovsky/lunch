import logging
import aiohttp
import aiohttp_jinja2
from aiohttp.web import json_response

from lunch.storage import TeamStorage


log = logging.getLogger(__name__)

ts = TeamStorage()


@aiohttp_jinja2.template('main.jinja2')
async def index(request):
    return {}


class RestaurantsHandler:

    @aiohttp_jinja2.template('places.jinja2')
    async def index(self, request):
        return {}

    async def add(self, request):
        # TODO: validate request
        body = await request.json()
        ts.add_restaurant(**body)
        return json_response(ts.get_resstaurans())

    async def get(self, request):
        return json_response(ts.get_resstaurans())

    async def delete(self, request):
        body = await request.json()
        ts.delete_restaurant(body['name'])
        return json_response(ts.get_resstaurans())
