import json
import time
from web3 import Web3, HTTPProvider,TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract History {
	string public name;
	string public time;
	string public product;

    function setLog(string a, string b, string c) public constant returns(string, string,string ) {
        name = a;
	time = b;
	product = c;
    }
    
    
    function getLog() constant returns (string, string, string) {
	return (name, time, product);
    }
}
'''



compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:History']

provider = HTTPProvider('http://0.0.0.0:9945')
w3 = Web3(provider)

contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.deploy(transaction={'from': w3.eth.coinbase, 'gas':1000000})

print ('tx_hash : ' + tx_hash)

while w3.eth.getTransactionReceipt(tx_hash) is None:
	time. sleep(0.1)	

contract_address = w3.eth.getTransactionReceipt(tx_hash).contractAddress
print ('contract_address' + contract_address)
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

contract_instance.setLog("test", "123", "pro",transact={'from': w3.eth.coinbase,'gas':3000000})
time.sleep(3)
print (contract_instance.getLog())
print('Contract value: {}'.format(contract_instance.getLog()))
