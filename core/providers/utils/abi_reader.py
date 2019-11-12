#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Test ABI
from core.providers.utils.constants.test_abi import abi

# Import Web3 Package
from web3 import Web3

# Import Json Package
import json


class ABIReader:
    def __init__(self):
        self.name = self.__class__.__name__

    def map(self):
        pass

    def read_from(self, path):
        with open(path) as abi_file:
            d = json.load(abi_file)
            # print(d)
        # return


project_api_key = ' https://mainnet.infura.io/v3/b3fa360a82cd459e8f1b459b3cf9127c'
test_safe_addr = '0x522715235d66faeF072509697445A66B442faD88'

web3 = Web3(Web3.HTTPProvider(project_api_key))
# print(web3.isConnected())
# print(web3.eth.blockNumber)
balance = web3.eth.getBalance(test_safe_addr)


address = "0xf79cb3BEA83BD502737586A6E8B133c378FD1fF2"
contract = web3.eth.contract(address=address, abi=abi)

# print(contract.__dict__)
# print(contract.address)
current_abi_function = contract.functions.__dict__
for item in current_abi_function['abi']:
    print(item['name'])
    print(item['inputs'])
    try:
        print(item['outputs'])
    except Exception as err:
        pass
