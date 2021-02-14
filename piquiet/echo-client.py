#!/usr/bin/env python3

import socket
from piquiet.rsa import encrypt, decrypt

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = "hello world"
        enc = encrypt(message)
        t = ""
        for e in enc:
            t += str(e)
        enc = int(t)
        s.sendall(int.to_bytes(enc, 32, "big"))
        data = int.from_bytes(s.recv(1024),"big")
        data = str(data)
        d = [int(data[i:i + 4]) for i in range(0, len(data), 4)]

    return decrypt(d)


if __name__ == "__main__":
    print(f"Received: {listen()}")
