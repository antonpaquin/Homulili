import sys
import secret
import hashlib

uname = sys.argv[1]

md5 = hashlib.md5()
md5.update(uname.encode('utf-8'))
md5.update(secret.auth_key.encode('utf-8'))
print(md5.hexdigest())
