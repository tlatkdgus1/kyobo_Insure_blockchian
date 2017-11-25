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

# web3.py instance
provider = HTTPProvider('http://0.0.0.0:9945')
w3 = Web3(provider)
# Instantiate and deploy contract
contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
contract_address = "0xcbcbc9fc0eabf0a3c2eaed69ebace988e1f58139"
print ('contract_address : ' + str(contract_address))
# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
# Getters + Setters for web3.eth.contract object
time.sleep(3)
print (contract_instance.getLog())
print('Contract value: {}'.format(contract_instance.getLog()))
