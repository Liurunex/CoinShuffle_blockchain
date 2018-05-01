import numpy as np
import json
import Crypto
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
        self.keypair  = util.generate_keypair()
        self.ek = util.public_key(self.keypair)

    def submit_ek_to_server(self, addr):
        requests.post(addr + '/coinshuffle/submitkey', data = {'public_key' : self.ek, 'address' : self.addr})