import json
import base64
import hashlib
from Cryptodome.Cipher import AES
import numpy as np
from PIL import Image


def generate_key_from_image(path="sample_image.jpg"):
    im = Image.open(path)
    shape = np.array(im).shape
    ding = int(np.product(np.array(im).reshape(np.product(shape)).shape))
    return hashlib.sha256(int.to_bytes(ding, 32, 'big')).hexdigest()


def generate_key_from_string():
    s = input("type something random:")
    return hashlib.sha256(s.encode()).hexdigest()


def encrypt(k, data):
    cipher = AES.new(k, AES.MODE_EAX)
    ciphertext, t = cipher.encrypt_and_digest(data)
    return ciphertext, t, cipher.nonce


def decrypt(k, ciphertext, t, n):
    cipher = AES.new(k, AES.MODE_EAX, nonce=n)
    data = cipher.decrypt(ciphertext)
    try:
        cipher.verify(t)
        return data
    except ValueError:
        return False


if __name__ == "__main__":
    message = b"hello world"

    key = generate_key_from_string()
    print(key)
    key = bytearray.fromhex(key)

    enc, tag, nonce = encrypt(key, message)

    text = decrypt(key, enc, tag, nonce)

    print(f"{message} >> {enc} >> {text}")
