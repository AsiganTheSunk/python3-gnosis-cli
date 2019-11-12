#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Types
from typing import List, Dict
from typing import NewType
# Import Json Module
import json

# Import Web3 Module
from web3 import Web3, HTTPProvider

class InfuraProvider:
    def __init__(self):
        self.name = self.__class__.__name__
        self.api_keys = List[str]
        self.properties = {}

    def get_infura_provider(self):
        # Fill in your infura API key here
        infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY_GOES_HERE"
        web3 = Web3(Web3.HTTPProvider(infura_url))
        return

    def get_ganache_provider(self):
        return Web3(HTTPProvider('http://127.0.0.1:8545'))

    def read_abi_from(self, path):
        with open(path) as abi_file:
            d = json.load(abi_file)
            # print(d)
        # return


def main():
    infura_provider = InfuraProvider()
    safe_stable_version_1_0_0 = './safe/safe-contracts-1.0.0/build/contracts/GnosisSafe.json'
    safe_development_path = './safe/safe-contracts-development/build/contracts/GnosisSafe.json'
    safe_addr = '0xe982E462b094850F12AF94d21D470e21bE9D0E9C'
    safe_abi = infura_provider.read_abi_from(path=safe_stable_version_1_0_0)
    ganache_provider = infura_provider.get_ganache_provider()


    # Fill in your infura API key here
    infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY_GOES_HERE"
    # web3 = Web3(Web3.HTTPProvider(infura_url))
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    print(web3)
        # Contract(address=safe_addr, abi=safe_abi)

    return


if __name__ == '__main__':
    main()
