#!/usr/bin/env python3
import asyncio, json
from indy import wallet
from indy.error import IndyError, ErrorCode
from getpass import getpass

name = input('Enter Wallet Name: ')
key = getpass('Enter Wallet Key: ')
key2 = getpass('Re-Enter Wallet Key: ')

if key != key2:
    print('Wallet keys don\'t match!')
    exit(1)

async def setup_wallet(name, key):
    wallet_config = json.dumps({"id": name})
    wallet_credentials = json.dumps({"key": key})
    try:
        await wallet.create_wallet(wallet_config, wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            print('A wallet named {} already exists'.format(name))
            exit(1);

    # Test wallet config
    wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
    await wallet.close_wallet(wallet_handle)
    print('Wallet {} created successfully!'.format(name))


loop = asyncio.get_event_loop()
loop.run_until_complete(setup_wallet(name, key))
loop.close()
