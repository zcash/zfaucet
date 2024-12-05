import os

# Address and port of local zcashd testnet RPC ports
NODE_ENDPOINT = os.getenv('NODE_ENDPOINT')

#Timeout needs to be high for any pour operations
TIMEOUT = 600

#Default fee to use on network for txs.
DEFAULT_FEE = os.getenv('DEFAULT_FEE', 0.015)

# node config
RPCUSER = os.getenv('RPCUSER')
RPCPASSWORD = os.getenv('RPCPASSWORD')
