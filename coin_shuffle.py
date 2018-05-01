import numpy as np
import json
import requests
import atexit
import time
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


def trigger_func():
    print("test")
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# initial the CoinShuffle server
app = Flask(__name__)
server = CoinShuffleClient()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=trigger_func,
    trigger=IntervalTrigger(seconds=2),
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