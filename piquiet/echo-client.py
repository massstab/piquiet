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
        self.s.setblocking(False)
        self.packet_length = 10
        self.max_length = 128
        self.separator = b"\x00\x01\x01\x00"

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
        packets = [message[i:i + self.packet_length] for i in range(0, len(message), self.packet_length)]
        for k, p in enumerate(packets):
            # print(f"sending: {p}")
            self.send_packet(p)

    def send_packet(self, message):
        """
        Encrypt and send message to the server

        :param message: unencrypted message to send
        :type message: String
        """
        key = get_key()
        # encrypt the message
        enc, tag, nonce = encrypt(key, message.encode())
        # send the encrypted message + tag + nonce ended by self.separator
        header = f"{len(enc):03}, {len(tag):03}, {len(nonce):03}".encode()
        if len(header + enc + tag + nonce) > self.max_length:
            raise Exception("Message is too long!")
        self.s.send(header)
        self.s.send(enc)
        self.s.send(tag)
        self.s.send(nonce)
        # print(enc + tag + nonce + self.separator)

    def listen(self):
        """
        Receive and decrypt a message from the server

        :return: decrypted message
        :rtype: String
        """
        key = get_key()
        o = b""
        while True:
            try:
                data = self.s.recv(1024)
                o += data
            except BlockingIOError:
                output = ""
                while len(o) > 0:
                    # get data from header
                    header = o[:13].decode().split(",")
                    enc_len = int(header[0])
                    tag_len = int(header[1])
                    nonce_len = int(header[2])
                    # split message according to header
                    enc = o[13:13 + enc_len]
                    tag = o[13 + enc_len:13 + enc_len + tag_len]
                    nonce = o[13 + enc_len + tag_len:13 + enc_len + tag_len + nonce_len]
                    # decrypt the message
                    d = decrypt(key, enc, tag, nonce)
                    output += d.decode()
                    # delete the first packet from received string
                    o = o[13 + enc_len + tag_len + nonce_len:]
                if output != "":
                    print(output)
        return output

    def close(self):
        self.s.close()


if __name__ == "__main__":
    # can use the send command once, and the receive command to get the echo
    TCP = Server("linus")
    TCP.send("Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod "
             "tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
             "quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. "
             "Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
             "Excepteur sint obcaecat cupiditat non proident, sunt in culpa "
             "qui officia deserunt mollit anim id est laborum.")
    TCP.listen()
    TCP.close()
