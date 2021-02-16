#!/usr/bin/env python3
import json
import socket
from piquiet.encryption import encrypt, decrypt, get_key


class Server:

    def __init__(self, server):
        self.hostname, self.port = self.get_config(server)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def get_config(server, path="connection.config"):
        with open(path, 'r') as f:
            c = json.load(f)
        return c[server]["hostname"], c[server]["port"]

    def send(self, message):
        key = get_key()
        enc, tag, nonce = encrypt(key, message.encode())
        self.s.connect((self.hostname, self.port))
        self.s.sendall(enc)
        self.s.sendall(b"\t")
        self.s.sendall(tag)
        self.s.sendall(b"\t")
        self.s.sendall(nonce)
        self.s.sendall(b"\n")

    def listen(self):
        key = get_key()
        o = b""
        while True:
            data = self.s.recv(1024)
            if not data:
                break
            o += data
            if b"\n" in data:
                break
        o = o.replace(b"\n", b"")
        print(o)
        enc, tag, nonce = o.split(b'\t')
        data = decrypt(key, enc, tag, nonce)
        return data


if __name__ == "__main__":
    TCP = Server("dave")
    # TCP.send("hi dave, this is a super long message. ueble sache maloney..
    # cool stuff.. yes.. und denn ischsi verruuckt worde.. heute hast du aber hunger, mann")
    TCP.send("hi dave, this is a short message")
    print(TCP.listen())
