from Crypto import Random
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify


def generate_keys():
    random_gen = Random.new().read
    return RSA.generate(1024, random_gen)


def public_key(keys):
    res_key = hexlify(keys.publickey().exportKey('DER'))
    return res_key.decode()


# input: public_key (type: byte string), plaintext (type: encoded())
# output: string
def encryption(p_key, data):
    rsa_key = RSA.importKey(unhexlify(p_key))
    e_res = rsa_key.encrypt(data, 32)[0]
    return hexlify(e_res).decode()


# input: key_pair (type: RSA keys), cipher_text (hexlify())
# output: byte_string
def decryption(keys, e_msg):
    res = keys.decrypt(unhexlify(e_msg))
    return hexlify(res).decode()


if __name__ == '__main__':
    # Crypto Test
    key_1 = generate_keys()
    key_2 = generate_keys()
    key_3 = generate_keys()
    msg = "127.0.0.1:5001"

    pk_1 = public_key(key_1)
    pk_2 = public_key(key_2)
    pk_3 = public_key(key_3)

    emsg = encryption(pk_1.encode(), msg.encode())
    emsg = encryption(pk_2.encode(), unhexlify(emsg.encode()))
    emsg = encryption(pk_3.encode(), unhexlify(emsg.encode()))

    print("---------------")
    dmsg = decryption(key_3, emsg.encode())
    dmsg = decryption(key_2, dmsg.encode())
    dmsg = decryption(key_1, dmsg.encode())

    print(unhexlify(dmsg.encode()).decode() == msg)
    print(unhexlify(dmsg.encode()).decode())
    # json hexlify result test
    '''
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
    '''