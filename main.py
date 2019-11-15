#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.providers.constants.api_keys import api_key_dict
from core.providers.constants.test_contract import test_abi_contract, test_address_contract
from core.providers.infura_provider import InfuraProvider
from core.providers.ganache_provider import GanacheProvider
import json
import os
import subprocess
# Todo: place to map
# path_to_safe = '/home/asigan/Desktop/safe-contracts-1.1.0/build/contracts/Proxy.json'
# safe_address = '0x7C728214be9A0049e6a86f2137ec61030D0AA964'
# safe_team_address = '0x6B1133AeCdF2CeB239CE2b88C0375421786323c4'
# safe_address0 = '0x1A5F9352Af8aF974bFC03399e3767DF6370d82e4'

project_directory = os.getcwd() + '/testing_assets/safe-contracts-1.1.0/'
contracts_sol_directory = project_directory + 'contracts/'
contracts_abi_directory = project_directory + 'build/contracts/'
proxy_factory_abi = contracts_abi_directory + 'ProxyFactory.json'
safe_address_deployment = '0xe982E462b094850F12AF94d21D470e21bE9D0E9C'
proxy_factory_address_deployment = '0xCfEB869F69431e42cdB54A4F4f105C19C080A601'

gnosis_safe_abi = contracts_abi_directory + 'GnosisSafe.json'
proxy_abi = contracts_abi_directory + 'Proxy.json'
proxy_interface_abi = contracts_abi_directory + 'IProxy.json'
proxy_factory_abi = contracts_abi_directory + 'ProxyFactory.json'
mock_contract_abi = contracts_abi_directory + 'MockContract.json'
mock_token_abi = contracts_abi_directory + 'Token.json'

from core.gnosis_console_input import GnosisConsoleInput
from prompt_toolkit.completion import WordCompleter

gnosis_safe_cli_completer = [
    'safe_addr', 'add', 'after', 'all', 'before', 'check',
    'current_date', 'current_time', 'current_timestamp',
    'default', 'delete', 'exit', 'quit', 'without'
]


def compile_contracts(contracts_path):
    TRUFFLE_COMPILE = 'truffle compile'
    TRUFFLE_SOFT_MIGRATE = 'truffle migrate'
    TRUFFLE_HARD_MIGRATE = 'truffle migrate --reset'

    try:
        subprocess.Popen('cd {contract_path}; {truffle_compile}'.format(
            contract_path=contracts_path, truffle_compile=TRUFFLE_COMPILE), stdout=subprocess.PIPE, shell=True)
        return True
    except Exception as err:
        print(err)
        return False


def read_abi_file(path_to_abi):
        try:
            with open(path_to_abi) as f:
                info_json = json.load(f)
            print(info_json["contractName"], 'ABI has been provided as an endpoint to generate the interface with the contract')
            abi = info_json["abi"]
            return abi
        except Exception as err:
            print(err)


def main():
    # Compile Contracts
    compile_contracts(contracts_sol_directory)
    print('Current PATH: ', gnosis_safe_abi)
    ABI_SAFE = read_abi_file(gnosis_safe_abi)
    ABI_PROXY_FACTORY = read_abi_file(proxy_factory_abi)
    import time
    time.sleep(1)
    ganache_provider = GanacheProvider()

    # Todo: make a list on build directory if it does not exist when the function is called, the contracts will
    #  be compiled via subprocess using truffle compile this is maily because the current versions for py-solcx
    #  and py-sol reports an error while trying to access the mock contracts.

    proxy_instance = ''
    proxy_interface_instance = ''
    mock_contract_instance = ''
    mock_token_instance = ''

    current_contract_instance, gnosis_safe_interface = ganache_provider.get_contract_interface(safe_address_deployment, ABI_SAFE)


    # for item in gnosis_safe_interface:
    #     gnosis_safe_cli_completer.append(gnosis_safe_interface[item]['function_name'])
    #     print(gnosis_safe_interface[item]['function_input'])
    #
    # print(gnosis_safe_cli_completer)
    # gnosis_cli = GnosisConsoleInput()
    # current_provider = ganache_provider.get_current_provider()
    # gnosis_cli.run(WordCompleter(gnosis_safe_cli_completer, ignore_case=True), gnosis_safe_interface, current_contract_instance)

    # infura_provider = InfuraProvider('mainnet')
    # infura_provider.get_contract(test_address_contract, test_abi_contract)


if __name__ == '__main__':
    main()

