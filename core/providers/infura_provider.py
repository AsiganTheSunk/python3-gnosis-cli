#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3, HTTPProvider

class InfuraProvider:
    def __init__(self, api_key, network):
        self.name = self.__class__.__name__
        self.api_key = api_key
        self.port = ''
        self.address = (lambda _address: 'https://mainnet.infura.io/v3/' if network is 'mainnet' else 'https://rinkeby.infura.io/v3/')
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

    def get_provider(self):
        return Web3(Web3.HTTPProvider(self.uri))

