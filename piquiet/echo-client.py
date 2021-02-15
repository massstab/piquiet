#!/usr/bin/env python3
import json
import socket


def get_config(server, path="connection.config"):
    with open(path, 'r') as f:
        c = json.load(f)
    return c[server]["hostname"], c[server]["port"]


def listen(hostname, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        s.sendall(b'Hello, world')
        data = s.recv(1024)
    return repr(data)


if __name__ == "__main__":
    print(f'Received: {listen(*get_config("dave"))}')
