#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.providers.constants.api_keys import api_key_dict
from core.providers.constants.test_contract import test_abi_contract, test_address_contract
from core.providers.infura_provider import InfuraProvider
from core.providers.ganache_provider import GanacheProvider

import json

# Todo: place to map
path_to_safe = '/home/asigan/Desktop/safe-contracts-1.1.0/build/contracts/Proxy.json'
safe_address = '0x7C728214be9A0049e6a86f2137ec61030D0AA964'

safe_team_address = '0x6B1133AeCdF2CeB239CE2b88C0375421786323c4'

safe_address0 = '0x1A5F9352Af8aF974bFC03399e3767DF6370d82e4'


def main():
    # ganache_provider = GanacheProvider()
    # print(ganache_provider['port'])
    # print(ganache_provider['address'])
    # print(ganache_provider['uri'])
    # ganache_provider.get_contract(safe_address, path_to_safe)

    # with open('contract_abi.json', 'r', encoding='utf-8') as abi_file:
    #     contract_abi = json.loads(abi_file.read())
    #
    #     ganache_provider.get_contract(safe_address, contract_abi)

    # bug: provider does not seem to get the .eth module generating a exception
    infura_provider = InfuraProvider('mainnet')
    infura_provider.get_contract(test_address_contract, test_abi_contract)

    # infura_provider = InfuraProvider('rinkeby')
    # infura_provider.get_contract(test_address_contract, test_abi_contract)

if __name__ == '__main__':
    main()
