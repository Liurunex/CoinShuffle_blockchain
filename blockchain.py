# Blockchian to manage the chain, store transactions and add new blocks

"""
block = {
    'index': ...
    'timestamp': ...
    'proof': ...
    'previous_hash': ...  Immutability
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
from urllib.parse import urlparse
from uuid import uuid4
from time import time

import requests
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        # creates a new Block and adds it to the chain
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
        # adds a new transaction to the list of transactions
        # go into the next mined Block
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # return index of the block which the transaction will be added to
        return self.last_block['index'] + 1

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1
        return proof

    def register_node(self, address):
        # add new node to node list
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # check hash
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False
            # check PoW
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False
            # iteration
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # consensus algorithm: replacing chain with longest one in network
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        # verify the chains from all nodes in network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # check length and chain's validation
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # replace chain if found
        if new_chain:
            self.chain = new_chain
            print("class_resolve_conflicts return True")
            return True
        else:
            print("class_resolve_conflicts return False")
            return False

    # decorator
    # property decorator: set the func as class member
    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # Hashes a Block with SHA-256 hash
        # must make sure that the Dictionary is Ordered, 
        # or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        # proof hash(last_proof, proof) go with 4 leading zeros
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Blockchain as an API 

# instantiate the Node
app = Flask(__name__)

# globally unique address
node_identifier = str(uuid4()).replace('-', '')

# instantiate the Blockchain
blockchain = Blockchain()


# /mine endpoint, GET request
@app.route('/mine', methods=['GET'])
def mine():
    # PoW
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

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
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    # status code: 200
    return jsonify(response), 200


# /transactions/new endpoint, POST request
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    # status code: 201
    return jsonify(response), 201


# /chain endpoint, return the full Blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    # status code: 200
    return jsonify(response), 200



# Consensus

# /nodes/register, adding neighbouring nodes
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


# /nodes/resolve, resolving conflicts
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)