import secret
from cryptography.fernet import Fernet
import json
import base64

crypto = Fernet(bytes.fromhex(secret.auth_key))

permissions = json.dumps({
    'create': True,
    'read': True,
    'update': True,
    'delete': True,
    'index': True,
    'command': True,
}).encode('utf-8')

token = base64.b64encode(crypto.encrypt(permissions)).decode()
print(token)
