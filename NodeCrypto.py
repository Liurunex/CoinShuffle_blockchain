from Crypto import Random
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify

import json


def generate_keys():
    random_gen = Random.new().read
    return RSA.generate(1024, random_gen)


def public_key(keys):
    res_key = hexlify(keys.publickey().exportKey('DER'))
    return res_key


def encryption(p_key, data):
    rsa_key = RSA.importKey(unhexlify(p_key))
    e_res = rsa_key.encrypt(data.encode(), 32)[0]
    return hexlify(e_res)


def decryption(keys, e_msg):
    return keys.decrypt(unhexlify(e_msg)).decode()


if __name__ == '__main__':
    # Crypto Test
    keypair = generate_keys()
    pubkey = public_key(keypair)
    msg = "127.0.0.1:5001dasddas"
    print('-------\n pubkey:' + str(pubkey))
    #print('-------\n msg is : ' + msg)

    # json hexlify result test
    atest = []
    atest.append(pubkey)
    bstr = pubkey.decode()
    key = bstr.encode()
    atest.append(key)
    print(atest[0] == atest[1])
    encrypted_msg = encryption(atest[1], msg)
    decrypted_msg = decryption(keypair, encrypted_msg)
    print('-------\n encrypted res: ' + str(encrypted_msg))
    print('-------\n decrypted res: ' + decrypted_msg)