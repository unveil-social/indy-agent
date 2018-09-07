#!/usr/bin/env python3.6
import sys, json

REQUEST = 'did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/request'
RESPONSE = 'did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/response'
ACK = 'did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/acknowledge'

if len(sys.argv) != 3:
    print("Invalid parameters")
    exit(1)
token = sys.argv[1]
message = sys.argv[2]
message = json.loads(message)

if message['type'] == REQUEST:
    print('Request')
elif message['type'] == RESPONSE:
    print('Response')
elif message['type'] == ACK:
    print('Ack')
else:
    print('Unknown Message Type')
    exit(1)
