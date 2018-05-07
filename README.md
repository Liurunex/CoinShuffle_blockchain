# CoinShuffle with Blockchain
independent project 

# set the blockchain enviroment
check thie page for instruction: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

# How to run
Please first initiate the coinshuffle server (coin_shuffle.py), then you can intiate duplicate blockchain nodes to start. The coinshuffle server was configured with constant local address 127.0.0.1:5000, please don't use this specific address to run the node. 

To start the blockchian, you can simply run the shell 'python3 blockchain.py -p {address}'. The node will initiate itself on the address you assign to it, otherwise it will run on the default address 127.0.0.1:5001. Please note that you need duplicate the blockchain.py with independent name in order to run next node service.

Basically, the inital node will automatecally register itself with the coinshuffle server, and the server will run the coinshuffle process in a interval of 10s.

# How to interactive with coinshuffle server and the blockchain
Check thie page for basic blockchain interactive APIs: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

Many API has been implemented inside. We have write comment and description for those APIs in detail. Please dig in the blockchain.py and coin_shuffle.py for more detail, 
