#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3

from web3.providers.rpc import HTTPProvider

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging

class GanacheProvider:
    def __init__(self, logging_lvl=INFO, gui=False):
        self.name = self.__class__.__name__
        self.port = self.select_port(gui)
        self.network_name = 'ganache'
        self.address = '127.0.0.1'
        self.uri = '{0}:{1}'.format(self.address, self.port)

        self.logger = CustomLogger(self.name, logging_lvl)

        # CustomLogger Format Definition
        formatter = logging.Formatter(fmt='%(asctime)s - [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # Custom Logger File Configuration: File Init Configuration
        file_handler = logging.FileHandler('./log/gnosis_console/gnosis_console_input.log', 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level=logging_lvl)

        # Custom Logger Console Configuration: Console Init Configuration
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level=logging_lvl)

        # Custom Logger Console/File Handler Configuration
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

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
        """ Get Contract
        This function

        :param contract_address:
        :param contract_abi:
        :return:
        """
        try:
            with Web3(HTTPProvider(self.uri)) as current_provider:
                current_provider = Web3(HTTPProvider(self.uri))
                current_status = current_provider.isConnected()
                if current_status:
                    self.logger.info('{0} is connected to {1} network'.format(self.name, self.network_name))

                    current_contract = current_provider.eth.contract(address=contract_address, abi=contract_abi)
                    current_abi_function = current_contract.functions.__dict__
                    # print(current_contract.__dict__)
                    # print(current_contract.address)
                    for item in current_abi_function['abi']:
                        print(item['name'])
                        print(item['inputs'])
                        try:
                            print(item['outputs'])
                        except Exception as err:
                            print(err)

                    self.logger.info('{0} is not connected to {1} network'.format(self.name, self.network_name))
        except Exception as err:
            print(err)