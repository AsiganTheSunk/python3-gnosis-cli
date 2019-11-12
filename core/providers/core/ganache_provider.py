#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3, HTTPProvider

class GanacheProvider:
    def __init__(self, api_key, gui=False):
        self.name = self.__class__.__name__
        self.api_key = api_key
        self.port = (lambda x: '8545' if gui else '7545')
        self.address = '127.0.0.1'
        self.uri = '{0}:{1}'.format(self.address, self.port)

        self._properties = {'name': self.name, 'port': self.port, 'address': self.address, 'uri': self.uri,
                            'api_key': self.api_key}

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    def get_provider(self):
        return Web3(Web3.HTTPProvider(self.uri))
