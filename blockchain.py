import json
import time
import socket
from web3 import Web3, HTTPProvider,TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract contract_Register {
	string public name;
	string public time;
	string public product;

	function setLog(string a, string b, string c) public {
		name = a;
		time = b;
		product = c;
	}

	 function getLog() constant returns (string, string, string) {
                return (name, time, product);
        }
	
}

'''


def Register(arg):
	_name = arg['name']
	_time = arg['time']
	_product = arg['product']
	print ("====== REQUEST RESGISER ======\n")
	compiled_sol = compile_source(contract_source_code) # Compiled source code
	contract_interface = compiled_sol['<stdin>:contract_Register']

	provider = HTTPProvider('http://0.0.0.0:9945')
	w3 = Web3(provider)

	contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
	tx_hash = contract.deploy(transaction={'from': w3.eth.coinbase, 'gas':1000000})
	print ('tx_hash : ' + tx_hash)
	while w3.eth.getTransactionReceipt(tx_hash) is None:
		time.sleep(0.1)

	contract_address = w3.eth.getTransactionReceipt(tx_hash).contractAddress
	print ('contract_address' + contract_address)
	print ("==============================\n\n")
	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
	time.sleep(3)
	return {"contract_addr":contract_address}

def Search(arg):
	contract_address = arg['contract_addr']
	compiled_sol = compile_source(contract_source_code) # Compiled source code
	contract_interface = compiled_sol['<stdin>:contract_Register']

	print ("====== REQUEST SEARCH ======\n")
	provider = HTTPProvider('http://0.0.0.0:9945')
	w3 = Web3(provider)

	contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
	tx_hash = contract.deploy(transaction={'from': w3.eth.coinbase, 'gas':500000})
	print ('tx_hash : ' + tx_hash)
	
	print ('contract_address : ' + str(contract_address))
	print ("==============================\n\n")
	contract_instance = w3.eth.contract(contract_interface['abi'], str(contract_address), ContractFactoryClass=ConciseContract)

	value = contract_instance.getLog()
	return {"name":value[0],"time":value[1],"product":value[2]}
	


if __name__=="__main__":
	s = socket.socket()
	host = "0.0.0.0"
	port = 9947				
	s.bind((host, port))		
	print (host)
	s.listen(5)				 
	while True:
		c, addr = s.accept()
		print('Got connection from', addr)
		arg = json.loads(c.recv(1024).decode())
		if arg["function"] == "register":
			result = Register(arg)
		elif arg["function"] == "search":
			result = Search(arg)	
		
		c.send((json.dumps(result) + "\n").encode())
		c.close()

