#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import API Key
from core.providers.constants.api_keys import api_key_dict
from core.providers.constants.test_contract import test_abi_contract

# Import Web3 Module
from web3 import Web3, HTTPProvider

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging

class InfuraProvider:
    def __init__(self, network, api_key='', logging_lvl=INFO):
        self.name = self.__class__.__name__
        self.api_key = self.__get_api_key(api_key)
        self.port = ''
        self.network_name = network
        self.address = self.__get_network(network)
        self.uri = '{0}{1}'.format(self.address, self.api_key)

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
            'api_key': self.api_key,
            'port': self.port,
            'address': self.address,
            'uri': self.uri
        }

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    def __get_network(self, network):
        """ Get Network

        :param network:
        :return:
        """
        if network == 'mainnet':
            return 'https://mainnet.infura.io/v3/'
        return 'https://rinkeby.infura.io/v3/'

    def __get_api_key(self, _api_key):
        """ Get API Key
        This function retrieves a valid API Key from constant files in case no one was provided
        :param _api_key:
        :return:
        """
        if _api_key == '':
            return api_key_dict['API_KEY']['infura']['0']
        return _api_key

    def get_contract(self, contract_address, contract_abi):
        """ Get Contract
        This function

        :param contract_address:
        :param contract_abi:
        :return:
        """

        current_status = False
        current_provider = None
        try:
            self.logger.info('{0} stablishing connection to {1} network with infura API via {2}'.format(self.name, self.network_name, self.uri))
            try:
                current_provider = Web3(HTTPProvider(self.uri, request_kwargs={'timeout': 60}))
                current_status = current_provider.isConnected()
            except Exception as err:
                print('Unable to retrieve Infura Provider', err)

            try:
                if current_status is False:
                    self.logger.info('{0} is not connected to {1}'.format(self.name, self.network_name))
                    return

                self.logger.info('{0} has successfully established a connection to {1} network'.format(self.name, self.network_name))

                current_contract = current_provider.eth.contract(address=contract_address, abi=contract_abi)
                current_abi_function = current_contract.functions.__dict__
                # print(current_contract.__dict__)
                # print(current_contract.address)
                function_list_name = []
                function_list_inputs = []
                function_list_outputs = []
                for item in current_abi_function['abi']:
                    function_list_name.append(item['name'])
                    function_list_inputs.append(item['inputs'])
                    try:
                        current_output_item = item['outputs']
                    except Exception as err:
                        current_output_item = 'Empty'
                        print('error: ', err)
                        pass
                    finally:
                        function_list_outputs.append(current_output_item)
                self.logger.info('{0} has successfully retrieved {1} elements from current contract'.format(self.name, len(function_list_name)))
                # print(function_list_name)
                # print(function_list_inputs)
                # print(function_list_outputs)
                current_contract.functions.owner().call()
                # last_block = current_provider.eth.getBlock('latest')
                # print(last_block)
            except Exception as err:
                print(err)
        except Exception as err:
            print(err)
