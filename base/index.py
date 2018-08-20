#!/usr/bin/env python3

from src.handler import http_handler
from src.utils import get_pool_genesis_txn_path, run_coroutine, PROTOCOL_VERSION
from indy import anoncreds, crypto, did, ledger, pool, wallet
from indy.error import ErrorCode, IndyError
from aiohttp import web
import logging, sys, yaml, json, time, asyncio, code

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

with open('config.yml') as f:
    config = yaml.safe_load(f)


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 3000

if len(sys.argv) > 2:
    key = sys.argv[2]
else:
    key = ""


async def health_handler(request):
    return web.Response(text="Success")


async def pool_setup():
    pool_name = config['pool']['name']
    logger.info("Open Pool Ledger: {}".format(pool_name))
    pool_genesis_txn_path = get_pool_genesis_txn_path(pool_name)
    pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})

    # Set protocol version 2 to work with Indy Node 1.4
    await pool.set_protocol_version(PROTOCOL_VERSION)

    try:
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
            pass

    # Test Connection
    pool_handle = await pool.open_pool_ledger(pool_name, None)
    await pool.close_pool_ledger(pool_handle)


async def wallet_setup():
    wallet_name = config['wallet']['name']
    wallet_key = config['wallet']['key']
    wallet_config = json.dumps({"id": wallet_name})
    wallet_credentials = json.dumps({"key": wallet_key})
    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass

    # Test wallet config
    wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    await wallet.close_wallet(wallet_handle)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run_coroutine(pool_setup, loop)
    run_coroutine(wallet_setup, loop)

    app = web.Application()
    app.add_routes([
        web.get('/', health_handler),
        web.post('/', http_handler)
    ])

    web.run_app(app, host='0.0.0.0', port=port)