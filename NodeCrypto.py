from Crypto.PublicKey import RSA
import argparse


def generate_key(id, code):
    key = RSA.generate(2048)
    # private key
    encryted_key = key.exportKey(passphrase=code, pkcs=8)
    with open(f'./privateKey_directory/{id}_private_rsaKey.bin', 'wb') as f:
        f.write(encryted_key)
    with open(f'./publicKey_directory/{id}_rsa_public_rsaKey.pem', 'wb') as f:
        f.write(key.publickey().exportKey())


def encryption():
    pass


def decryption():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Input a unique port number')
    args = parser.parse_args()
    port = args.port

    generate_key(port, 'whoKnows')