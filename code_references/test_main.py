#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from prompt_toolkit.completion import WordCompleter

from core.gnosis_console_engine import GnosisConsoleEngine

proxy_factory_deterministic_address = '0xCfEB869F69431e42cdB54A4F4f105C19C080A601'
safe_gnosis_deterministic_address = '0xe982E462b094850F12AF94d21D470e21bE9D0E9C'

proxy_factory_abi = os.getcwd() + '/assets/safe-contracts-1.1.0/build/contracts/Proxy.json'
safe_gnosis_abi = os.getcwd() + '/assets/safe-contracts-1.1.0/build/contracts/GnosisSafe.json'

from core.utils.contract.contract_truffle import TruffleInterface
from core.utils.ganache_provider import GanacheProvider

# Import GnosisSafe Module
from core.utils.gnosis_safe_setup import GnosisSafeModule

gnosis_safe_cli_completer = [
    'safe_addr', 'add', 'after', 'all', 'before', 'check',
    'current_date', 'current_time', 'current_timestamp', 'current_block'
    'default', 'delete', 'exit', 'quit', 'without',
]

def call_gnosis_console(console_contract_artifacts):
    print('Launching Gnosis Console')
    gnosis_cli = GnosisConsoleEngine(console_contract_artifacts)
    gnosis_cli.run_console_session()


def init_scenario():
    # remark: not good "fix",
    PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'
    ganache_provider = GanacheProvider()
    provider = ganache_provider.get_provider()
    contract_interface = TruffleInterface(provider, PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    contract_artifacts = contract_interface.deploy_contract()

    # remark: Get Contract Artifacts for the Proxy & GnosisSafe
    safe_instance = contract_interface.get_new_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_new_instance(contract_artifacts['Proxy'])

    # remark: Get Interface to interact with the contract
    gnosis_safe_module = GnosisSafeModule(provider, contract_artifacts)
    functional_safe = gnosis_safe_module.setup(safe_instance, proxy_instance)

    tmp_contract_artifacts ={
        'instance': functional_safe,
        'abi': contract_artifacts['GnosisSafe']['abi'],
        'bytecode': contract_artifacts['GnosisSafe']['bytecode'],
        'address': contract_artifacts['GnosisSafe']['address']
    }

    console_contract_artifacts = ConsoleContractData()
    console_contract_artifacts.add_artifact(tmp_contract_artifacts, alias='Gnosis-Safe(v1.1.0)')
    call_gnosis_console(console_contract_artifacts.contract_data)

    stream = 'loadContract --alias=Gnosis-Safe(v1.1.0)'

    # stream = 'gAccount0.address'
    # console_session_accounts = ConsoleSessionAccounts()
    # console_session_accounts._evaluate_account_data(stream)

if __name__ == '__main__':
    init_scenario()

# INPUT TESTS
query_is_owner = 'isOwner --address=0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 --query'
execute_swap_owner = 'swapOwner --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002 --from=0x00000000000000000000000000000003 --execute'
query_get_owners = 'getOwners --query'
query_execTransaction_not_enough_args = 'execTransaction --queue --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002'

# contract_interface = ContractInterface(provider)
# safe_artifacts = contract_interface.get_artifacts(safe_gnosis_abi, safe_gnosis_deterministic_address)
# proxy_artifacts = contract_interface.get_artifacts(proxy_factory_abi, contract_to_point=safe_artifacts['address'])
# Get Interface to interact with the contract
# gnosis_safe_setup_module = GnosisSafeModule(provider, safe_artifacts)
# gnosis_safe_instance = gnosis_safe_setup_module.setup(safe_artifacts['instance'], proxy_artifacts['instance'])