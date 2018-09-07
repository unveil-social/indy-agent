from aiohttp import web
from .utils import unpack, get_config
from subprocess import call
import logging, json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = get_config()

async def handler(msg):
    # FIXME: Validate message format. Has type attr, etc.
    if False: #internally handled
        print('stub')
    else:
        # FIXME: Call Active Modules
        #import pdb; pdb.set_trace()
        for static_module in config['modules']['static']:
            module = config['modules']['static'][static_module]
            for message_type in module['message_types']:
                if msg['type'] == message_type:
                   call([module['path'], 'faketoken', json.dumps(msg)]) 


async def http_handler(request):
    data = request._payload._buffer[0].decode('utf-8')
    #import pdb; pdb.set_trace()
    msg = await unpack(data)
    logger.info("Received Message: {}".format(json.dumps(msg))) 
    await handler(msg)
    return web.Response(text="Accepted", status=202)



