import json
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

def get_key():
    with open('private.key', 'r') as f:
        d = json.load(f)
    return d["key"]


def encrypt(t, key=None):
    if key is None: key = get_key()
    b = t.encode()
    i = int.from_bytes(b, "big")
    return i * key


def decrypt(i, key=None):
    if key is None: key = get_key()
    i = i // key
    b = int.to_bytes(i, 32, "big")
    t = b.decode("utf-8")
    return t


if __name__ == "__main__":
    message = "hello world"
    enc = encrypt(message)
    text = decrypt(enc)
    print(f"{message} >> {enc} >> {text}")
