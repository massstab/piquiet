def encrypt(text, key):
    b = text.encode()
    i = int.from_bytes(b, "big")
    return i * key


def decrypt(i, key):
    i = i // key
    b = int.to_bytes(i, 64, "big")
    text = b.decode("utf-8")
    return text


if __name__ == "__main__":
    key = 1234213908490281309481
    c = encrypt("hello world", key)
    t = decrypt(c, key)
    print(c, t)
