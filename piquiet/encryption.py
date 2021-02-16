import json
import hashlib
from Cryptodome.Cipher import AES
import numpy as np
from PIL import Image


def generate_key_from_image(path="sample_image.jpg"):
    """
    Generate a key from an image and store it in the .keys/AES.key file

    :param path: image path
    :type path: String
    :return: key
    :rtype: bytearray
    """
    im = Image.open(path)
    shape = np.array(im).shape
    ding = int(np.product(np.array(im).reshape(np.product(shape)).shape))
    k = hashlib.sha256(int.to_bytes(ding, 32, 'big')).hexdigest()
    d = {"key": str(k)}
    with open('.keys/AES.key', 'w') as f:
        json.dump(d, f)
    print(k)
    return bytearray.fromhex(k)


def generate_key_from_string():
    """
    Generate a key from an image and store it in the .keys/AES.key file

    :return: key
    :rtype: bytearray
    """
    s = input("type something random:")
    k = hashlib.sha256(s.encode()).hexdigest()
    d = {"key": str(k)}
    with open('.keys/AES.key', 'w') as f:
        json.dump(d, f)
    print(k)
    return bytearray.fromhex(k)


def get_key(path=".keys/AES.key"):
    """
    Load key from .keys/AES.key file

    :param path: file path
    :type path: String
    :return: key
    :rtype: bytearray
    """
    with open(path, 'r') as f:
        k = json.load(f)
    return bytearray.fromhex(k["key"])


def encrypt(k, data):
    """
    Encrypt data with the given key

    :param k: key
    :type k: bytearray
    :param data: data
    :type data: bytearray
    :return: ciphertext, tag and nonce
    :rtype: bytearray, bytearray, bytearray
    """
    cipher = AES.new(k, AES.MODE_EAX)
    ciphertext, t = cipher.encrypt_and_digest(data)
    return ciphertext, t, cipher.nonce


def decrypt(k, ciphertext, t, n):
    """
    Decrypt the ciphertext using the key, tag and nonce. Validate using the tag.
    Return False if invalid.

    :param k: key
    :type k: bytearray
    :param ciphertext: encrypted data
    :type ciphertext: bytearray
    :param t: tag
    :type t: bytearray
    :param n: nonce
    :type n: bytearray
    :return: message or False
    :rtype: String or Boolean
    """
    cipher = AES.new(k, AES.MODE_EAX, nonce=n)
    data = cipher.decrypt(ciphertext)
    try:
        cipher.verify(t)
        return data
    except ValueError:
        return False


if __name__ == "__main__":
    # key = generate_key_from_string()      # uncomment to generate key

    # load the key
    key = get_key()

    read_nohub()

    # encrypt the message
    # enc, tag, nonce = encrypt(key, message)

    # decrypt the message
    # text = decrypt(key, enc, tag, nonce)
    #
    # print(f"{message} >> {enc} >> {text}")
