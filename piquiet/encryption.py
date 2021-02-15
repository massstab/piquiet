import json
import base64
import hashlib
from Cryptodome.Cipher import AES


def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag, nonce


def decrypt(key, ciphertext, tag, nonce):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return data
    except ValueError:
        return False


if __name__ == "__main__":
    message = b"hello world"

    key = hashlib.sha256(b"Nobody").digest()
    print(key)

    enc, tag, nonce = encrypt(key, message)

    text = decrypt(key, enc, tag, nonce)
    print(f"{message} >> {enc} >> {text}")
