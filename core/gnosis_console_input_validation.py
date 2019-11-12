#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class GnosisConsoleInputValidation:
    """ Gnosis Console Input

    """
    def __init__(self):
        self.name = self.__class__.__name__

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
