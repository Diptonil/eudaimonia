import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Must be 16 characters long
k2 = hashlib.sha256('example_key_16  '.encode()).digest()


# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def encrypt(raw, key):
    BS = AES.block_size

    def pad(s):
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


# unpad = lambda s: s[:-ord(s[-1:])]
def decrypt(enc, key):

    def unpad(s):
        return s[:-ord(s[-1:])]

    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))
