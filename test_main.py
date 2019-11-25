#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


proxy_factory_deterministic_address = '0xCfEB869F69431e42cdB54A4F4f105C19C080A601'
safe_gnosis_deterministic_address = '0xe982E462b094850F12AF94d21D470e21bE9D0E9C'

proxy_factory_abi = os.getcwd() + '/assets/safe-contracts-1.1.0/build/contracts/Proxy.json'
safe_gnosis_abi = os.getcwd() + '/assets/safe-contracts-1.1.0/build/contracts/GnosisSafe.json'

from core.utils.gnosis_console_session_accounts import ConsoleSessionAccounts
from core.utils.contract.contract_truffle import ContractInterface
from core.providers.ganache_provider import GanacheProvider

# Import GnosisSafe Module
from core.utils.gnosis_safe_setup import GnosisSafeModule

def init_scenario():
    # contract_interface = ContractInterface(provider)
    # safe_artifacts = contract_interface.get_artifacts(safe_gnosis_abi, safe_gnosis_deterministic_address)
    # proxy_artifacts = contract_interface.get_artifacts(proxy_factory_abi, contract_to_point=safe_artifacts['address'])
    # Get Interface to interact with the contract
    # gnosis_safe_setup_module = GnosisSafeModule(provider, safe_artifacts)
    # gnosis_safe_instance = gnosis_safe_setup_module.setup(safe_artifacts['instance'], proxy_artifacts['instance'])

    PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'
    ganache_provider = GanacheProvider()
    provider = ganache_provider.get_provider()

    contract_interface = ContractInterface(provider, PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    contract_artifacts = contract_interface.deploy_contract()

    # remark: Get Contract Artifacts for the Proxy & GnosisSafe
    safe_instance = contract_interface.get_new_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_new_instance(contract_artifacts['Proxy'])

    # remark: Get Interface to interact with the contract
    gnosis_safe_module = GnosisSafeModule(provider, contract_artifacts)
    functional_safe = gnosis_safe_module.setup(safe_instance, proxy_instance)


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