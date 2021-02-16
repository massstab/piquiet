#!/usr/bin/env python3
import json
import socket
from piquiet.encryption import encrypt, decrypt, get_key


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
        print(len(enc))
        print(len(tag))
        print(len(nonce))
        self.s.sendall(enc)
        self.s.sendall(tag)
        self.s.sendall(nonce)
        self.s.sendall(b"\n")

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
            # if not data:
            #     # if nothing is received
            #     break
            o += data
            if b"\n" in data:
                # if end of packet is detecte§d
                break

        # replace end of packet
        print(o)
        o = o.replace(b"\n", b"")
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
    TCP = Server("linus")
    TCP.send("hi linus, this is a looooooooooooong message, hehe, "
             "hehehehehehehajdfhjkahsfkjhasdlf asdfasdf asdd")
    print(TCP.listen())
