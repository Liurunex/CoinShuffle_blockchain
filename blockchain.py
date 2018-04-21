# Blockchian to managing the chain, storing transactions, adding new blocks
'''
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
'''


from time import time
import json
import  hashlib


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

    # decorator
    @staticmethod
    def hash(block):
        # Hashes a Block with SHA-256 hash
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
