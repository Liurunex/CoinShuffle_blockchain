import requests
import atexit
import time
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify, request


# CoinShuffle
class CoinShuffleServer:
    def __init__(self):
        self.nodes = list()
        self.public_keys = list()
        # trigger list shuffle
        self.shuffle_order = list()
        self.shuffle_flag = False
        self.shuffle_res = None


# initial the CoinShuffle server
app = Flask(__name__)
server = CoinShuffleServer()


def trigger_func():
    if len(server.nodes) < 2:
        print("CoinShuffle trigger: ")
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    else:
        # reset pub_keys
        server.shuffle_flag = True
        for index, node in enumerate(server.nodes):
            response = requests.get(f'http://{node}/shuffle/Phase_1')
            pub_key_str = response.json()['pubkey']
            server.public_keys[index] = pub_key_str
        print('CoinShuffle Server: Phase 1 done')

        # start the shuffling by picking a random node to start
        index = random.randint(0, len(server.nodes)-1)
        ordered_nodes = []
        while len(ordered_nodes) != len(server.nodes):
            ordered_nodes.append(server.nodes[index])
            index += 1
            if index == len(server.nodes):
                index = 0

        # send the shuffle to first node

        print(f"CoinShuffle Server: send initial shuffle request to {ordered_nodes[0]}")
        print(ordered_nodes)
        shuffle_message = []
        requests.post(url=f'http://{ordered_nodes[0]}/shuffle/Phase_2', json={
            'current_index': 0,
            'ordered_nodes': ordered_nodes,
            'public_keys': server.public_keys,
            'shuffle_message': shuffle_message
        })

        print(f"CoinShuffle Server: start verification")

        # send result back to nodes to verify
        verify_res = True
        print(server.shuffle_res)
        for node in server.nodes:
            print(f'{node} try to do verify')
            response = requests.post(url=f'http://{node}/shuffle/verify', json={'result_list': server.shuffle_res})
            res = response.json()['Result']
            if res is False:
                verify_res = False
                break

        # rerun and find the malicious user
        if verify_res is False:
            print("CoinShuffle Server: Verification failed")
        else:
            # start creating the shuffled transaction
            print("CoinShuffle Server: Verification done, enter transaction phase")

        server.shuffle_flag = False
        print(f'CoinShuffle Server: Phase 3 Done as {verify_res}')

        # assume now verification result is True
        # send result back to node 
        for node in server.nodes:
            print(f'sending shuffle res back to {node}, prepare for msg and vote')
            requests.post(url=f'http://{node}/shuffle/receive', json={'result_list': server.shuffle_res})



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
    print(f"CoinShuffle Server: received a node {node}")
    print(list(server.nodes))
    return jsonify(response), 201


# /shuffle/result, CoinShuffle received result from node, POST request
@app.route('/shuffle/Phase_3', methods=['POST'])
def receive_result():
    values = request.get_json()
    shuffle_res = values.get('shuffle_res')
    server.shuffle_res = shuffle_res
    print("CoinShuffle Server: received shuffled result, start Phase_3 ")
    print(shuffle_res)

    response = {'msg': 'CoinShuffle Server: wait for verification'}
    return jsonify(response), 201


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