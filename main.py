#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.providers.constants.api_keys import api_key_dict
from core.providers.constants.test_contract import test_abi_contract, test_address_contract
from core.providers.infura_provider import InfuraProvider
from core.providers.ganache_provider import GanacheProvider

# Todo: place to map
path_to_safe = '/home/asigan/Desktop/safe-contracts-1.1.0/build/contracts/'
safe_address = '0x7C728214be9A0049e6a86f2137ec61030D0AA964'

def main():
    ganache_provider = GanacheProvider()
    print(ganache_provider['port'])
    print(ganache_provider['address'])
    print(ganache_provider['uri'])
    # ganache_provider.get_provider()
    # ganache_provider.get_contract(safe_address, path_to_safe)
    # ganache_provider.get_contract(test_address_contract, test_abi_contract)

    infura_api_key = api_key_dict['API_KEY']['infura']['0']
    infura_provider = InfuraProvider(infura_api_key, 'mainnet')
    infura_provider.get_provider()
    infura_provider.get_contract(test_address_contract, test_abi_contract)


if __name__ == '__main__':
    main()