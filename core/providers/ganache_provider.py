#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Code Reference: https://medium.com/hackernoon/creating-a-python-ethereum-interface-part-1-4d2e47ea0f4d
# Safe Code Reference: https://github.com/gnosis/safe-contracts/blob/development/test/gnosisSafeDeploymentViaTx.js
# Safe Project Reference: https://github.com/gnosis/safe-contracts

# Import Web3 Module
from web3 import Web3

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging

from core.providers.interface import ContractInterface

class GanacheProvider:
    def __init__(self, logging_lvl=INFO, gui=False):
        self.name = self.__class__.__name__
        self.port = self.select_port(gui)
        self.network_name = 'ganache'
        self.address = 'http://127.0.0.1'
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
            'uri': self.uri
        }

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    @staticmethod
    def select_port(gui):
        ''' Select Port
        Select the current GanacheProvider port based on input values
        :param gui:
        :return:
        '''
        if gui:
            return '7545'

        return '8545'

    def get_current_provider(self):
        return Web3(Web3.HTTPProvider(self.uri, request_kwargs={'timeout': 60}))

    def get_contract_interface(self, contract_address, contract_abi):
        """ Get Contract Interface
        This function

        :param contract_address:
        :param contract_abi:
        :return:
        """
        current_contract = None
        current_provider = None
        current_status = False
        functions_contract_data = {}
        try:
            try:
                current_provider = Web3(Web3.HTTPProvider(self.uri, request_kwargs={'timeout': 60}))
                current_status = current_provider.isConnected()
                self.logger.info('{0} stablishing connection to {1} network via {2}'.format(self.name, self.network_name, self.uri))
            except Exception as err:
                print('{provider} unable to retrieve provider'.format(provider=self.name), err)
            try:
                if current_status is False:
                    self.logger.info('{0} is not connected to {1}'.format(self.name, self.network_name))
                    return {}
                self.logger.info('{0} has successfully established a connection to {1} network'.format(self.name, self.network_name))
                current_contract = current_provider.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)

                item_name = ''
                item_input = ''

                for index, item in enumerate(current_contract.functions.__dict__['abi']):
                    try:
                        item_name = item['name']
                    except KeyError:
                        continue
                    try:
                        item_input = item['inputs']
                    except KeyError:
                        item_input = ''

                    functions_contract_data[index] = {
                        'function_name': item_name,
                        'function_call_clean': 'current_contract.functions.{0}({1}).call',
                        'function_call': 'current_contract.functions.{}().call'.format(item['name']),
                        'function_input': item_input
                    }

            except Exception as err:
                print(err)
            self.logger.info('{0} has successfully retrieved {1} elements from current contract'.format(self.name, len(
                functions_contract_data)))
            return current_contract, functions_contract_data

            # current_threshold = current_contract.functions.getThreshold().call()
            # print('Current Threshold: ', current_threshold)
            # current_account = current_provider.eth.accounts[1]
            # # print(current_provider.eth.accounts[0])
            # current_owners = current_contract.functions.isOwner('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call()
            # print('isOwner: ', current_owners)
            # current_name = current_contract.functions.NAME().call()
            # print('Name: ', current_name)
            # current_version = current_contract.functions.VERSION().call()
            # print('Version: ', current_version)
            # current_modules = current_contract.functions.setup().call()
            # print('Version: ', current_modules)

        except Exception as err:
            print(err)
