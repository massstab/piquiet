#!/usr/bin/env python3
import json
import socket
from piquiet.encryption import encrypt, decrypt, get_key


def get_config(server, path="connection.config"):
    with open(path, 'r') as f:
        c = json.load(f)
    return c[server]["hostname"], c[server]["port"]


def listen(hostname, port):
    key = get_key()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        message = "hello dave you little man"
        enc, tag, nonce = encrypt(key, message.encode())
        s.sendall(enc)
        s.sendall(b"\n")
        s.sendall(tag)
        s.sendall(b"\n")
        s.sendall(nonce)
        s.sendall(b"\n")
        print(enc, tag, nonce)
        o = s.recv(1024)
        print(enc)
        o += s.recv(1024)
        print(tag)
        enc, tag, nonce, _ = o.split(b'\n')
        data = decrypt(key, enc, tag, nonce)
    return data


if __name__ == "__main__":
    print(f'Received: {listen(*get_config("dave"))}')
