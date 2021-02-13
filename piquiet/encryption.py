import json


def get_key():
    with open('private.key', 'r') as f:
        d = json.load(f)
    return d["key"]


def encrypt(text, key=None):
    if key is None: key = get_key()
    b = text.encode()
    i = int.from_bytes(b, "big")
    return i * key


def decrypt(i, key=None):
    if key is None: key = get_key()
    i = i // key
    b = int.to_bytes(i, 32, "big")
    text = b.decode("utf-8")
    return text


if __name__ == "__main__":
    c = encrypt("hello world")
    t = decrypt(c)
    print(c, t)
