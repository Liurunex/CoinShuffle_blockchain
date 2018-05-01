import numpy as np
import json
from flask import Flask, jsonify, request
import requests


# CoinShuffle
class CoinShuffleClient:
    def __init__(self):
        self.nodes = list()
        self.public_keys = list()
        # trigger list shuffle
        self.shuffle_order = list()
        self.shuffle_flag = False


# initial the CoinShuffle server
app = Flask(__name__)
server = CoinShuffleClient()


@app.route('/initial/nodes', methods=['POST'])
def add_nodes():
    values = request.get_json()

    node = values.get('node')
    if node is None:
        return "Error: Please supply a valid list of nodes", 400

    server.nodes.append(node)

    response = {
        'message': 'CoinShuffle Server: new nodes have been added',
        'total_nodes': list(server.nodes),
    }
    print(list(server.nodes))
    return jsonify(response), 201


# /shuffle/result, send CoinShuffle result to CoinShuffle server, POST request
@app.route('/shuffle/send_result', methods=['POST'])
def send_result():
    pass


# constant port 5000 for CoinShuffle Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)