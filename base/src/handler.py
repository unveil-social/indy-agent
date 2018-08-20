from aiohttp import web
from indy import anoncreds, crypto, did, ledger, pool, wallet
from src.utils import unpack
import json, yaml, subprocess
with open('config.yml') as f:
    config = yaml.safe_load(f)


async def http_handler(request):
    data = json.loads(request._payload._buffer[0])
    return web.Response(text="Accepted")

