#!/usr/bin/env python3
import json
import socket
from piquiet.encryption import encrypt, decrypt, get_key
import sys
import time


class Server:

    def __init__(self, server):
        """
        Class to connect to dave's or linus' raspberry pi server

        :param server: name of server to connect to
        :type server: String
        """
        self.hostname, self.port = self.get_config(server)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.hostname, self.port))

    @staticmethod
    def get_config(server, path="connection.config"):
        """
        Static method to get the configuration for the server connection

        :param server: name of server to connect to
        :type server: String
        :param path: path of the configuration file
        :type path: String
        :return: hostname, port
        :rtype: String, Int
        """
        with open(path, 'r') as f:
            c = json.load(f)
        return c[server]["hostname"], c[server]["port"]

    def send(self, message):
        """
        Encrypt and send message to the server

        :param message: unencrypted message to send
        :type message: String
        """
        key = get_key()
        # encrypt the message
        enc, tag, nonce = encrypt(key, message.encode())
        # send the encrypted message + tag + nonce ended by \n
        if len(enc + tag + nonce + b"\x00") > 128:
            raise Exception("Message is too long!")
        self.s.send(enc)
        self.s.send(tag)
        self.s.send(nonce)
        self.s.send(b"\x00")

    def listen(self):
        """
        Receive and decrypt a message from the server

        :return: decrypted message
        :rtype: String
        """
        key = get_key()
        o = b""
        while True:
            data = self.s.recv(1024)
            o += data
            if data[-1:] == b"\x00":
                break

        # replace end of packet
        o = o[:-1]
        print(o)
        # split the packet into three items
        # tag and nonce are always of length 16, enc is the rest.
        nonce = o[-16:]
        tag = o[-32:-16]
        enc = o[:-32]
        # decrypt the message
        data = decrypt(key, enc, tag, nonce)
        return data


if __name__ == "__main__":
    # can use the send command once, and the receive command to get the echo
    # TODO: longer messages require multiple packets (length 1024),
    #  implement splitting the message and receiving multiple packets separated by \n
    for i in range(1000):
        TCP = Server("linus")
        TCP.send("hi linus, this is a test")
        print(TCP.listen())
        time.sleep(1)
