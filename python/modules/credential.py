"""
Module to handle credential management.
"""


import json
import base64
import aiohttp
from indy import crypto, did, pairwise, anoncreds


import serializer.json_serializer as Serializer
from model import Message
from message_types import UI, CRED, FORWARD
from helpers import serialize_bytes_json, bytes_to_str, str_to_bytes


class Credential(Module):

	def __init__(self, agent):
		self.agent = agent
		self.router = SimpleRouter()
		
		self.router.register(CRED.OFFER, self.offer_received)
        self.router.register(CRED.REQUEST, self.request_received)
        self.router.register(CRED.CREDENTIAL, self.credential_received)

        self.router.register(CRED_UI.SEND_OFFER, self.send_offer)
        self.router.register(CRED_UI.SEND_REQUEST, self.send_request)
        self.router.register(CRED_UI.SEND_CREDENTIAL, self.send_credential)

    async def route(self, msg: Message) -> Message:
        return await self.router.route(msg)


	async def prepare_credential(msg: Message, my_agent) -> Message:
		
		# 1 genSchema
		# 2 genKeys
		# 3 issueAccumulator

		# define schema

		schema_name = msg.content['name']

		attrs = {}

		tags = {}

		(schema_id, schema_json) = await anoncreds.issuer_create_schema(msg.did, schema_name, 1.0, attrs)

		(cred_def_id, cred_def_json) = await anoncreds.issuer_create_and_store_credential_def(my_agent.wallet_handle, msg.did, schema_json, tag)

		"""
		return Message(
			type=UI.CREDENTIAL_PREPARED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def send_offer(msg: Message, my_agent) -> Message:

		cred_def_id = msg.content['cred_def_id']

		cred_offer_json = await anoncreds.issuer_create_credential_offer(my_agent.wallet_handle, cred_def_id)

		"""
		return Message(
			type=UI.OFFER_SENT,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def receive_offer(msg: Message, my_agent) -> Message:

		"""
		return Message(
			type=UI.OFFER_RECEIVED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def send_request(msg: Message, my_agent) -> Message:
		cred_offer_json = msg.content['cred_offer']
		cred_def_json = msg.content['cred_def']
		# 4 createClaimRequest

		master_secret_id = {}

		(cred_req_json, cred_req_metadata_json) = await anoncreds.prover_create_credential_req(my_agent.wallet_handle, msg.did, cred_offer_json, cred_def_json, master_secret_id)

		"""
		return Message(
			type=UI.REQUEST_SENT,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def receive_request(msg: Message, my_agent) -> Message:

		"""
		return Message(
			type=UI.REQUEST_RECEIVED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""


	async def issue_credential(msg: Message, my_agent) -> Message:
		cred_offer = msg.content['offer']
		cred_request = msg.content['request']

		# 5 issueClaim

		cred_json = await anoncreds.issuer_create_credential(my_agent.wallet_handle, cred_offer_json, cred_req_json, attrs)

		"""
		return Message(
			type=UI.CREDENTIAL_ISSUED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def send_credential(msg: Message, my_agent) -> Message:

		"""
		return Message(
			type=UI.CREDENTIAL_SENT,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def receive_credential(msg: Message, my_agent) -> Message:

		# 6 processClaim

		cred_id = await anoncreds.prover_store_credential(wallet_handle, cred_req_metadata_json, cred_json, cred_def_json)

		"""
		return Message(
			type=UI.CREDENTIAL_RECEIVED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""

	async def view_credential(msg: Message, my_agent) -> Message:
		cred_id = msg.content['id']

		cred_json = await anoncreds.prover_get_credential(my_agent.wallet_handle, cred_id)

		"""
		return Message(
			type=UI.CRED_VIEWED,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""


	async def get_all(msg: Message, my_agent) -> Message:

		credentials_json = await anoncreds.prover_get_credentials(my_agent.wallet_handle, None)

		"""
		return Message(
			type=UI.GET_ALL,
			id=my_agent.ui_token,
			content={'name': conn_name})
		"""


	"""
	# NOTE: will be tough to define before Proofs module is built
	async def verify_credential(msg: Message, my_agent) -> Message:

		# 8 verify

		valid = await anoncreds.verifier_verify_proof(proof_request_json, proof_json, schemas_json, credential_defs_json, rev_reg_defs_json, rev_regs_json)
		

		return Message(
			type=UI.CREDENTIAL_VERIFIED,
			id=my_agent.ui_token,
			content={'name': conn_name})
	"""