import json
import base64
import hashlib
from Cryptodome.Cipher import AES
import numpy as np
from PIL import Image


def generate_key(path="sample_image.jpg"):
    im = Image.open(path)
    shape = np.array(im).shape
    ding = int(np.product(np.array(im).reshape(np.product(shape)).shape))
    return hashlib.sha256(int.to_bytes(ding, 32, 'big')).digest()


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

    key = generate_key()
    print(key)

    enc, tag, nonce = encrypt(key, message)

    text = decrypt(key, enc, tag, nonce)

    print(f"{message} >> {enc} >> {text}")
