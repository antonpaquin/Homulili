from cryptography.fernet import Fernet
import json
import base64

from . import secret

crypto = Fernet(bytes.fromhex(secret.auth_key))

auth_token = base64.b64encode(crypto.encrypt(json.dumps({
    'create': True,
    'read': True,
    'update': True,
    'delete': True,
    'index': True,
    'command': True,
}).encode('utf-8'))).decode()

auth_header = {
    'auth_token': auth_token,
}
