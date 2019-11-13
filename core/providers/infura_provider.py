#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3, HTTPProvider

class InfuraProvider:
    def __init__(self, api_key, network):
        self.name = self.__class__.__name__
        self.api_key = api_key
        self.port = ''
        self.address = self.select_network(network)
        self.uri = '{0}{1}'.format(self.address, self.api_key)

        self._properties = {
            'name': self.name,
            'api_key': self.api_key,
            'port': self.port,
            'address': self.address,
            'uri': self.uri
        }

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    def select_network(self, network):
        if network == 'mainnet':
            return 'https://mainnet.infura.io/v3/'
        return 'https://rinkeby.infura.io/v3/'

    def get_provider(self):
        try:
            provider = Web3(Web3.HTTPProvider(self.uri))
            print('Current Provider: ', provider.isConnected())
            return provider
        except Exception as err:
            print(err)

    def get_contract(self, contract_address, contract_abi):
        provider = Web3(Web3.HTTPProvider(self.uri))
        print('Current Provider: ', provider.isConnected())
        current_contract = provider.eth.contract(address=contract_address, abi=contract_abi)
        # print(current_contract.__dict__)
        # print(current_contract.address)
        current_abi_function = current_contract.functions.__dict__
        for item in current_abi_function['abi']:
            print(item['name'])
            print(item['inputs'])
            try:
                print(item['outputs'])
            except Exception as err:
                pass