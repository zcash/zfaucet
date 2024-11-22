import os.path
import sys

from pyZcash.rpc.ZDaemon import *
from pyZcash.settings import *

def test_daemon():
	zd = ZDaemon()

	# Network tests
	print((zd.getBlockHash(100)))
	print((zd.getBlockByHash(zd.getBlockHash(100))))
	print((zd.getBlockByHeight(100)))
	print((zd.getNetworkHeight()))
	print((zd.getNetworkDifficulty()))
	print((zd.getVersion()))
	print((zd.getConnectionCount()))

	# Taddr Wallet tests
	print((zd.getbalance()))
	print((zd.listunspent()))
	print((zd.getnewaddress()))

	# Zaddr wallet tests
	print((zd.z_getnewaddress()))
	zaddrs = zd.z_listaddresses()
	print(zaddrs)
	zaddr_received = zd.z_listreceivedbyaddress(zaddr)
	print(zaddr_received)

	# TODO: test z_sendmany, and use regtest

if __name__ == "__main__":
	test_daemon()
