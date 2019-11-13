#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3, HTTPProvider


class GanacheProvider:
    def __init__(self, gui=False):
        self.name = self.__class__.__name__
        self.port = self.select_port(gui)
        self.address = '127.0.0.1'
        self.uri = '{0}:{1}'.format(self.address, self.port)
        self.provider = self.get_provider()

        self._properties = {
            'name': self.name,
            'port': self.port,
            'address': self.address,
            'uri': self.uri,
            'provider': self.provider
        }

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    @staticmethod
    def select_port(gui):
        if gui:
            return '8545'
        return '7545'

    def get_provider(self):
        try:
            provider = Web3(HTTPProvider(self.uri))
            print('Current Provider: ', provider.isConnected())
            return provider
        except Exception as err:
            print(err)

    def get_contract(self, contract_address, contract_abi):
        current_contract = Web3.eth.contract(address=contract_address, abi=contract_abi)

        # print(contract.__dict__)
        # print(contract.address)
        current_abi_function = current_contract.functions.__dict__
        for item in current_abi_function['abi']:
            print(item['name'])
            print(item['inputs'])
            try:
                print(item['outputs'])
            except Exception as err:
                pass