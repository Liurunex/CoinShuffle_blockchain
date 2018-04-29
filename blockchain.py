# Blockchian to managing the chain, storing transactions, adding new blocks
"""
block = {
    'index': ...
    'timestamp': ...
    'proof': ...
    'previous_hash': ...
    'transactions': [
        {
            'sender': ...
            'recipient': ...
            'amount': ...
        }
    ],
}

transaction request = {
    'sender': my address
    'recipient': others' address
    'amount': ...
}
"""


from flask import Flask, jsonify, request
# from textwrap import dedent
from uuid import uuid4
from time import time
import hashlib
import json


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, previous_hash, proof):
        # Creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # reset current list of transaction
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # return index of the block which the transaction will be added to
        return self.last_block['index']+1

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    # decorator
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        proof hash(last_proof, proof) go with 4 leading zeros
        """
        # guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # Hashes a Block with SHA-256 hash
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # property decorator: set the func as class member
    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]


# instantiate Node
app = Flask(__name__)

# globally unique address
node_identifier = str(uuid4()).replace('-', '')

# instantiate the Blockchain
blockchain = Blockchain()


# /mine endpoint, GET request
@app.route('/mine', methods=['GET'])
def mine():
    # POW
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # sender is 0 to signify this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # appending the new block into chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


# /transactions/new endpoint, POST request
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # create new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


# /chain endpoint, return the full Blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# server runs on port 5000
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
