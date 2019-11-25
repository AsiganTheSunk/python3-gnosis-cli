#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BlkInstance:
    """ Blk Instance

    """
    def __init__(self, address):
        self.name = self.__class__.__name__

        self.address = address  # validate
        self.block_number = ''
        self.nonce = ''
        self.tx = ''
        self.owners = ''
        self.abi = ''  # if on etherscan - return abi of the contract.
        self.functions = ''  # if abi success, map the functions
        self.receipt = ''  # only if you use this instance to make transactions in the blockchain this will be fill
        self._properties = {'name': self.name, 'tx': self.tx, 'address': self.address, 'owners': self.owners,
                            'abi': self.abi, 'functions': self.functions, 'receipt': self.receipt}

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    def set_address(self, _address):
        self.address = _address

    def set_block(self, _block_number):
        self.block_number = _block_number

    def set_nonce(self, _nonce):
        self.nonce = _nonce

    def set_tx(self, _tx):
        self.tx = _tx

    def set_owners(self, _owners):
        self.owners = _owners

    def set_abi(self, _abi):
        self.abi = _abi

    def set_function(self, _function):
        self.functions = _function

    def set_receipt(self, _receipt):
        self.receipt = _receipt

