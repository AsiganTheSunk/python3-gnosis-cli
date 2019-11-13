#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging
from core.constants.default_messages import CONTRACT_ADDRESS_LENGTH, TX_ADDRESS_LENGTH, INFURA_API_KEY_LENGTH, ETHERSCAN_API_KEY_LENGTH
import re

class GnosisConsoleInputValidation:
    """ Gnosis Console Input

    """
    def __init__(self, logging_lvl=INFO):
        self.name = self.__class__.__name__
        self.logger = CustomLogger(self.name, logging_lvl)

        # CustomLogger Format Definition
        formatter = logging.Formatter(fmt='%(asctime)s - [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # Custom Logger File Configuration: File Init Configuration
        file_handler = logging.FileHandler('./log/gnosis_console/gnosis_console_input_validation.log', 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level=logging_lvl)

        # Custom Logger Console Configuration: Console Init Configuration
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level=logging_lvl)

        # Custom Logger Console/File Handler Configuration
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def input_api_key_validation(self, api_key):
        """ Input API Key Validation
        This function will validate the input API Key validation
        :param api_key:
        :return:
        """

        try:
            valid_api_key = re.search('[aA-zZ,0-9]*', api_key).group(0)
            if len(api_key) is INFURA_API_KEY_LENGTH and valid_api_key != '':
                self.logger.info('Infura API Key Detected')
            elif len(api_key) is ETHERSCAN_API_KEY_LENGTH and valid_api_key != '':
                self.logger.info('Etherscan API Key Detected')
            else:
                self.logger.info('No API Key Detected')
        except Exception as err:
            print(err)
        return '-1'

    # Todo: since the values for the current address and api key are standard just move the values to the constant
    #  directory and import them.
    def input_address_validation(self, address):
        """ Input Address Validation
         This function will validate the input address determining if the current value points a directory or if it's a
         address for a blockchain network.
         For References purposes:
            Tx Address: 0x3fbd9cdb8c51278062014032c50ea2ec66cc52f4c8be4136c3d416e2783d3b32
            Contract Address:  0xb23397f97715118532c8c1207F5678Ed4FbaEA6c

            :param address: this could be 0x or path to the contract if it's a local file being tested with ganache
            :return:
        """

        try:
            input_address = re.search('[aA-zZ,0-9]*', address).group(0)
            if len(address) is CONTRACT_ADDRESS_LENGTH and input_address != '':
                self.logger.info('Contract Address Detected')
            elif len(address) is TX_ADDRESS_LENGTH and input_address != '':
                self.logger.info('Tx Address Detected')
            else:
                self.logger.info('No Address Detected')
        except Exception as err:
            print(err)
        return

    def input_network_validation(self, network, network_id, network_params):
        """ Input Network Validation
        This function will validate the input network/network id, if both are provided. If network does not support
        network params they will not be validated and a warning will be prompted.
            :param network:
            :param network_id:
            :param network_params:
            :return:
        """
        if network != '':
            if network.lower() == 'ganache':
                self.logger.info('Ganache Network Detected')
                if network_params != {}:
                    self.logger.info('Ganache Param Network Detected')
            elif network.lower() == 'mainnet':
                self.logger.info('Mainnet Network Detected')
            elif network.lower() == 'rinkeby':
                self.logger.info('Rinkeby Network Detected')

        # Todo: Found Network Id's to be evalutated here if the network "name" it's not provided
        elif network_id != -1:
            self.logger.info('Nothing to watch here!')

        # validate the network o network id to launch the provider later.
        # if ganache and not online, launch te current ganache cli with the provided parameters.
        return
