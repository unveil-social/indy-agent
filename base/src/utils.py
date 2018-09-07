import yaml, base64, json
from indy import crypto
from aiohttp import web


CONFIG_PATH = 'config.yml'
config = None

def get_config():
    global config
    if not config:
        with open(CONFIG_PATH) as f:
            try:
                config = yaml.safe_load(f)
            except:
                print("Config YAML validation failed");
                exit(1);
            # FIXME: Validate config
    return config


def encode(msg):
    return base64.urlsafe_b64encode(msg.encode('utf-8')).hex()


def decode(msg):
    return base64.urlsafe_b64decode(bytes.fromhex(msg)).decode('utf-8')


async def pack(msg, theirVerKey = None, myVerKey = None, wallet_handle = None):
    # JSON to String
    msg = json.dumps(msg)

    # Determine algorithm and encrypt
    if msg and not theirVerKey and not myVerKey and not wallet_handle:
        alg = 'x-plain'
        pre_encoded_msg = msg
    elif msg and theirVerKey and not myVerKey and not wallet_handle:
        alg = 'x-anon'
        pre_encoded_msg = await crypto.anon_crypt(theirVerkey, msg.encode('utf-8'))
    elif msg and theirVerKey and myVerKey and wallet_handle:
        alg = 'x-auth'
        pre_encoded_msg = await crypto.auth_crypt(wallet_handle, myVerKey, theirVerKey, msg.encode('utf-8'))
    else:
        print("""
Error: Invalid usage of pack() function
pack(msg, null)  ⇒ JOSEhdr & “.” & base64url(msg)
pack(msg, toKey) ⇒ JOSEhdr & “.” & base64url( anonCrypt(msg, toKey) )
pack(msg, toKey, myPubKey, myPrivKey, walletHandle) ⇒ JOSEhdr & “.” & base64url( authCrypt(msg, toKey, myPubKey, myPrivKey) )
        """)
   
    # Setup JOSE header
    jose_header = {"typ":"x-b64nacl","alg":alg}
    if theirVerKey:
        jose_header['vk'] = theirVerKey
    #FIXME: Setup logger
    print('jose_header: {}'.format(jose_header))

    # Base64url encode
    encoded_jose_header = encode(json.dumps(jose_header))
    encoded_msg = encode(pre_encoded_msg)
    
    return encoded_jose_header + '.' + encoded_msg


async def unpack(encrypted_msg, wallet_handle = None):
    encrypted_msg_parts = encrypted_msg.split('.')
    jose_header = json.loads(decode(encrypted_msg_parts[0]))
    encrypted_msg = decode(encrypted_msg_parts[1])
    
    if jose_header['alg'] == 'x-plain':
        msg = encrypted_msg
    else:
        recipient_verkey = jose_header.vk
        if jose_header['alg'] == 'x-anon':
            msg = await crypto.anon_decrypt(wallet_handle, recipient_verkey, encrypted_msg)
        elif jose_header['alg'] == 'x-auth':
            msg = await crypto.auth_decrypt(wallet_handle, recipient_verkey, encrypted_msg)
    
    # Parse JSON
    return json.loads(msg)    


def exit_handler(sig, frame):
    print('\b\bShutting down agent... ')
    #global pool_handle, wallet_handle
    #loop.call_soon_threadsafe(loop.stop)
    #FIXME: Unable to close pool and wallet
    #loop.run_until_complete(pool.close_pool_ledger(pool_handle))
    #loop.run_until_complete(wallet.close_wallet(wallet_handle))
    #loop.close()
    exit(0)


async def health_handler(request):
    return web.Response(text="Success")
