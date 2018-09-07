#!/usr/bin/env python3
import asyncio, json, signal
from os import environ
from pathlib import Path
from tempfile import gettempdir
from indy import pool
from indy.error import ErrorCode, IndyError

PROTOCOL_VERSION = 2

pool_name = input("Enter Pool Name: ")

async def main():
    # Set protocol version 2 to work with Indy Node 1.4
    await pool.set_protocol_version(PROTOCOL_VERSION)

    print("Testing connection...")
    try:
        pool_handle = await pool.open_pool_ledger(pool_name, '{"timeout": 2}')
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerTimeout:
            print("Failed to connect to pool.  Is your IP Address correct?")
        exit(1)
    print("Successfully connected to ledger pool")
    await pool.close_pool_ledger(pool_handle)

def exit_handler(sig, frame):
    print('\b\bExiting...')
    exit(0)

signal.signal(signal.SIGINT, exit_handler)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
