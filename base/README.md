# Modular Indy-Agent

## Getting Started

```
git clone https://github.com/hyperledger/indy-agent && cd indy-agent/base # Clone the repository
virtualenv .venv # Setup a python virtual environement
source .venv/bin/activate # start venv
pip install -r requirements.txt # install dependencies
./helper_scripts/create_wallet.py # Use this script to create a new wallet
# Paste the name of your new wallet in the config.yml file
./helper_scripts/setup_pool.py # Use this script to setup your pool config and test connection
# Paste the name of your pool config in the config.yml file
./index.js # When prompted, type in your agent key
```

In another terminal:

```
cd indy-agent/base
pytest # Test pack, unpack, and the "Hello World" static module
```

If you don't have a running pool:

```
git clone https://github.com/hyperledger/indy-sdk && cd indy-sdk
docker build -f ci/indy-pool.dockerfile -t indy_pool1.4 .
docker run -itd --name indy_pool1.4 -p 9701-9708:9701-9708 indy_pool1.4
./helper_scripts/setup_pool.py # Use 127.0.0.1 as the pool ip
```

### Note on using Docker

This project does have a Dockerfile and a docker-compose.yml file, though they are still a work in progress.  `base.dockerfile` is the base agent itself, and all customizations should be done in `custom.dockerfile`.  

TODO: Add ledger pool to docker-compose.yml. Until we add this, using a local pool will simply hang.

To run the project using docker, 

```
git clone https://github.com/hyperledger/indy-agent && cd indy-agent/base # Clone the repository
./helper_scripts/create_wallet.py # Use this script to create a new wallet
# Paste the name of your new wallet in the config.yml file
./helper_scripts/setup_pool.py # Use this script to setup your pool config and test connection
# Paste the name of your pool config in the config.yml file
docker-compose build
docker-compose run -p "3210:3210" agent
```

Note that Docker will have access to the .indy_client directory of the host.

## Configuration
The agent configuration file and has the following format: 

`indy-agent/base/config.yml`


```
version: 1
wallet:
  	name: wallet1
pool:
  	name: pool1
agent:
  	port: 3210 # Proposed standard agent port
modules:
	static:
	  	connections:
		    path: ../modules/connections.py # Path to executable file
		    message_types: # All messages of these types are passed to this module.
		    - did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/offer
		    - did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/request
		    - did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/response
		    - did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/acknowledge
		    permissions:
		    - wallet/*
		    - credentials/*
		    - proofs/validate
	  	...
	active:
	  	ui:
	  		port: 3000 # Port the active module is listening on
	  		message_types: # All messages of these types are passed to this module.
	  		- 
  			premissions:
	  		- all
```

All agent functionality is found in modules, and the agent itself is just a framework. 

### Static Modules
Static modules are simply scripts, written in any language, that are called when a message of the defined type is received.  They are called with 2 parameters, a token and the encoded and (likely) encrypted message itself. 

EX: `../modules/connections.py 12345abcde DAFaskhlsdfSFAFJKASDFUOIPRQ089789SADadfs980ersfs=`

### Active Modules
When the agent is started, it sends a unique token to the module at the port found in the config file.  That token is then used to authenticate (determine permissions of ) the module to the agent.

That module can then send messages to the agent (at port 3210 based on the above config) using that token.  The agent can also POST messages to the module at the assigned port.

## Agent Internal Messages
Since only the agent can access the wallet, often modules will need access to wallet data and other agent functionality.  This is done through internal agent messages.  These messages are posted to the agent just like any other message and are authenticated with the token.  They are not encrypted and have the following format:

```
{
	@type: did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/internal_messages/1.0/get_credentials,
	token: 12345abcde,
	// Any other fields as determined by the message type
}
```

### Agent Internal Message Definitions (INCOMPLETE)

##### send\_message

```
{
	@type: did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/internal_messages/1.0/send_message,
	...
}
```

##### connections/send_request

```
{
	@type: did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/internal_messages/1.0/connections/send_request,
	...
}
```

## Permissions
For now, the permissions define the SDK calls that a person is allowed to make.  All SDK calls are done through the agent, abstracting direct wallet and ledger access.

Available permissions include:

```
anoncreds.*
anoncreds.issuer_create_schema
anoncreds.issuer_create_and_store_credential_def
...

blob_storage.*
crypto.*
did.*
ledger.*
non_secrets.*
pairwise.*
payment.*
```

Note: pool and wallet APIs are not available.

These actions are performed by sending an internal message to the base agent.
