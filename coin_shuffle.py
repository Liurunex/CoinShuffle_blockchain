import numpy as np
import json
import requests
import atexit
import time
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify, request


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


def trigger_func():
    if len(server.nodes) < 3:
        print("CoinShuffle trigger: ")
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    else:
        # reset pub_keys
        server.shuffle_flag = True
        for index, node in enumerate(server.nodes):
            response = requests.get(f'http://{node}/send_pubkey')
            pub_key_str = response.json()['pubkey']
            server.public_keys[index] = pub_key_str
        # start the shuffling by picking a random node: it's the last encryption node
        index = random.randint(0, len(server.nodes)-1)
        ordered_nodes = []
        while len(ordered_nodes) != len(server.nodes):
            ordered_nodes.append(server.nodes[index])
            index += 1
            if index == len(server.nodes):
                index = 0
        messages = []
        requests.post(f'http://{ordered_node[-1]}/shuffle/process', json={
            'ordered_nodes': ordered_nodes,
            'public_keys': server.public_keys,
            'messages': messages
        })


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=trigger_func,
    trigger=IntervalTrigger(seconds=10),
    id='CoinShuffle_job',
    name='CoinShuffle periodical job',
    replace_existing=True)
atexit.register(lambda: scheduler.shutdown())


@app.route('/initial/nodes', methods=['POST'])
def add_nodes():
    values = request.get_json()

    node = values.get('node')
    if node is None:
        return "Error: CoinShuffle Server: Please supply a valid list of nodes", 400

    server.nodes.append(node)
    server.public_keys.append(None)
    server.shuffle_order.append(len(server.nodes)-1)

    response = {
        'message': 'CoinShuffle Server: new nodes have been added',
        'total_nodes': list(server.nodes),
    }
    print(list(server.nodes))
    return jsonify(response), 201


# /shuffle/result, send CoinShuffle result to CoinShuffle server, POST request
@app.route('/shuffle/send_result', methods=['POST'])
def send_result():
    response = {'msg': 'msg'}
    return response, 201


@app.route('/test', methods=['POST'])
def test():
    values = request.get_json()
    message = values.get('message')
    print("-------CSserver: ")
    print(type(message))
    print(message)

    response = {
        'msg': 'test'
    }
    return jsonify(response), 201


# constant port 5000 for CoinShuffle Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)