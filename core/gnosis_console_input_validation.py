#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing Custom Logger & Logging Modules
from core.logger.custom_logger import CustomLogger
from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
from logging import INFO, DEBUG, WARNING
import logging

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

    @staticmethod
    def input_api_key_validation(api_key):
        """ Input API Key Validation
        This function will validate the input API Key validation
        :param api_key:
        :return:
        """
        return

    @staticmethod
    def input_address_validation(address):
        """ Input Address Validation
         This function will validate the input address validation
            :param address:
            :return:
        """
        return

    @staticmethod
    def input_contract_validation(contract):
        """ Input Contract Validation
        This function will validate the input contract validation
            :param contract:
            :return:
        """
        return

    @staticmethod
    def input_network_validation(network, network_id, network_params):
        """ Input Network Validation
        This function will validate the input network/network id, if both are provided. If network does not support
        network params they will not be validated and a warning will be prompted.
        :param network:
        :param network_id:
        :param network_params:
        :return:
        """
        return
