#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Code Reference: https://medium.com/hackernoon/creating-a-python-ethereum-interface-part-1-4d2e47ea0f4d
# Safe Code Reference: https://github.com/gnosis/safe-contracts/blob/development/test/gnosisSafeDeploymentViaTx.js
# Safe Project Reference: https://github.com/gnosis/safe-contracts

import os

from eth_account import Account

project_directory = os.getcwd() + '/testing_assets/safe-contracts-1.1.0/'
contracts_sol_directory = project_directory + 'contracts/'
contracts_abi_directory = project_directory + 'build/contracts/'

proxy_abi = contracts_abi_directory + 'Proxy.json'
safe_address_deployment = '0xe982E462b094850F12AF94d21D470e21bE9D0E9C'
proxy_factory_address_deployment = '0xCfEB869F69431e42cdB54A4F4f105C19C080A601'


# Import Web3 Module
from web3 import Web3

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging
import json


def read_abi_file(path_to_abi):
    try:
        with open(path_to_abi) as f:
            info_json = json.load(f)
        print(info_json["contractName"],
              'ABI has been provided as an endpoint to generate the interface with the contract')
        abi = info_json["abi"]
        byte_code = info_json["bytecode"]
        return abi, byte_code
    except Exception as err:
        print(err)


def string_to_byte(data):
    """ String To Byte (Hex)

    :param data:
    :return:
    """
    if len(data) > 8:
        byte8 = data[:8]
    else:
        byte8 = data.ljust(8, '0')
    return bytes(byte8, 'utf-8')


ABI_PROXY, BYTE_CODE_PROXY = read_abi_file(proxy_abi)

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
                proxy_contract = current_provider.eth.contract(bytecode=BYTE_CODE_PROXY, abi=ABI_PROXY)

                try:
                    # Completing Setup
                    account0 = current_provider.eth.accounts[0]
                    account1 = current_provider.eth.accounts[1]
                    account2 = current_provider.eth.accounts[2]
                    list_of_accounts = [account0, account1, account2]

                    #master_safe_copy = current_contract.functions.setup(list_of_accounts, 3, '0x' + '0'*40, bytes('0x', 'utf-8'), account0, account0, 0, account0).transact({'from':account1})

                    self.logger.info('Master Safe Copy Setup  Done!!')
                    print('address to master_safe_copy: ', current_contract.address)
                    # print(current_contract.functions.getOwners().call())
                    # print(current_contract.functions.getThreshold().call())

                    # Setting up the contract address to the proxy to aim at
                    tx_hash = proxy_contract.constructor(current_contract.address).transact({'from': account1})
                    self.logger.info('Proxy Safe Setup Done!!')
                    tx_receipt = current_provider.eth.waitForTransactionReceipt(tx_hash)
                    new_proxy_trans = current_provider.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)

                    # define null_address
                    NULL_ADDRESS = '0x' + '0'*40
                    tx_proxy_receipt = new_proxy_trans.functions.setup(list_of_accounts, 3, NULL_ADDRESS, bytes('0x', 'utf-8'), NULL_ADDRESS, NULL_ADDRESS, 0, NULL_ADDRESS).transact({'from': account1})

                    # When ever we need to operate with the current contract, doing a operation
                    # that modefies the contract, 'transact()' must be used
                    # When ever we need to operate with the current contract, doing a operation
                    # that queries the contract, 'call()' must be used

                    print(new_proxy_trans.functions.NAME().call())
                    print(new_proxy_trans.functions.VERSION().call())
                    print(new_proxy_trans.functions.isOwner('0xe982E462b094850F12AF94d21D470e21bE9D0E9C').call())
                    print(new_proxy_trans.functions.isOwner('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call())
                    print(new_proxy_trans.functions.getThreshold().call())
                    print(new_proxy_trans.functions.getOwners().call())

                    account = Account.create()
                    print('generate account with address: ', account.address)

                    # Setup Method 1:
                    # - Deployment of GnosisSafe
                    #   + init via gnosis_safe_contract.setup().transact()
                    # - Deployment of Proxy
                    #   + init via proxy_contract.contructor().transact()

                    # Send Ether to the current safe, then transfer the Ether to another account
                    # Firmar con las accounts de la transaction
                except Exception as err:
                    print('SETUP FAILED ', err)

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
