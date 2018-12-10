"""
Module to handle credential management.
"""


import json
import base64
import aiohttp
from indy import crypto, did, pairwise


import serializer.json_serializer as Serializer
from model import Message
from message_types import UI, CRED, FORWARD
from helpers import serialize_bytes_json, bytes_to_str, str_to_bytes


async def get_all(msg: Message, my_agent) -> Message:
	conn_name = msg.content['name']
	#wallet = my_agent.WALLET

	return Message(
		type=UI.GET_ALL,
		id=my_agent.ui_token,
		content={'name': conn_name})

async def send_offer(msg: Message, my_agent) -> Message:
	conn_name = msg.content['name']

	return Message(
		type=UI.OFFER_SENT,
		id=my_agent.ui_token,
		content={'name': conn_name})

async def accept_credential(msg: Message, my_agent) -> Message:
	conn_name = msg.content['name']

	return Message(
		type=UI.CREDENTIAL_ACCEPTED,
		id=my_agent.ui_token,
		content={'name': conn_name})

async def send_request(msg: Message, my_agent) -> Message:
	conn_name = msg.content['name']

	return Message(
		type=UI.REQUEST_SENT,
		id=my_agent.ui_token,
		content={'name': conn_name})

async def receive_request(msg: Message, my_agent) -> Message:
	conn_name = msg.content['name']

	return Message(
		type=UI.REQUEST_ACCEPTED,
		id=my_agent.ui_token,
		content={'name': conn_name})



