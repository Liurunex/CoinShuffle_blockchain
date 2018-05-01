import numpy as np
import json
import NodeCrypto
from flask import Flask, jsonify, request
from Crypto import Random
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify
import requests

# CoinShuffle


def generate_keypair():
    random_gen = Random.new().read
    return RSA.generate(1024, random_gen)


def public_key(keypair):
    return hexlify(keypair.publickey().exportKey('DER'))


class CoinShuffleClient:
    def __init__(self):
        self.keypair = NodeCrypto.generate_key()
        self.ek = NodeCrypto.public_key(self.keypair)

    def submit_ek_to_server(self, addr):
        requests.post(addr + '/coinshuffle/submitkey', data = {'public_key' : self.ek, 'address' : self.addr})


# initial the CoinShuffle server
app = Flask(__name__)
server = CoinShuffleClient()


# /shuffle/result, send CoinShuffle result to CoinShuffle server, POST request
@app.route('/shuffle/send_result', method=['POST'])
def send_result():
    pass


# constant port 5000 for CoinShuffle Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)