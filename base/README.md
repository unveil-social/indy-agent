# Node.js Indy-Agent v2 Design
## Configuration
The agent configuration is found at `~/.indy_agent_config.yml` and has the following format: 

```yaml
version: 1.6.0 # Agent version

wallet:
  name: wallet1 # defaults to wallet1
  key: badpass1 # defaults to empty string.  In future versions this will not be found in the config.
pool:
  name: pool1 # defaults to pool1
  ip: 52.40.231.144 # defaults to 127.0.0.1
  ports: 9701-9708 # defaults to 9701-9708
port: 24 # Proposed standard agent port
static_modules:
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
active_modules:
  ui:
  	path: ../modules/ui.js # Path to executable file that starts process
  	message_types: # All messages of these types are passed to this module.
  	- 
  	premissions:
  	- *
```

All agent functionality is found in modules, and the agent itself is just a framework. 

### Static Modules
Static modules are simply scripts, written in any language, that are called when a message of the defined type is received.  They are called with 2 parameters, a token and the encoded and (likely) encrypted message itself. 

EX: `../modules/connections.py 12345abcde DAFaskhlsdfSFAFJKASDFUOIPRQ089789SADadfs980ersfs=`

### Active Modules
When the agent is started, it starts each active module as a subprocess, assigns it a port, and gives it a unique token.  

EX: `../modules/connections.py 3000 12345abcde`.  

That module can then send messages to the agent (at port 24 based on the above config) using that token.  The agent can also POST messages to the module at the assigned port.

## Agent Internal Messages
Since only the agent can access the wallet, often modules will need access to wallet data and other agent functionality.  This is done through internal agent messages.  These messages are posted to the agent just like any other message and are authenticated with the token.  They are not encrypted and have the following format:

```
{
	@type: did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/internal_messages/1.0/get_credentials,
	token: 12345abcde,
	// Any other fields as determined by the message type
}
```

### Agent Internal Message Definitions

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




#Notes
* I need to check the setup of the agent on startup
* I need the process to persist beyond the life of the shell
* I need `agent cli` to start the indy cli to be able to manage the agent
