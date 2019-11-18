#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import GnosisSafe Module
from core.contracts.modules.gnosis_safe import GnosisSafeModule

# Import Provider Packages
from core.providers.infura_provider import InfuraProvider
from core.providers.ganache_provider import GanacheProvider

# Import Contract Interface
from core.contracts.contract_interface import ContractInterface

# Import Prompt Toolkit Packages
from core.gnosis_console_input import GnosisConsoleInput
from prompt_toolkit.completion import WordCompleter

import os

# Import Eth Account Package
from eth_account import Account

# Import Transaction History Manager Package
from core.transaction_history_manager import TransactionHistoryManager

# Import Gnosis CLI
import gnosis_cli as cli

PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'
CONTRACT_SOL_DIRECTORY = PROJECT_DIRECTORY + 'contracts/'
CONTRACT_BUILD_DIRECTORY = PROJECT_DIRECTORY + 'build/contracts/'

gnosis_safe_cli_completer = [
    'safe_addr', 'add', 'after', 'all', 'before', 'check',
    'current_date', 'current_time', 'current_timestamp', 'current_block'
    'default', 'delete', 'exit', 'quit', 'without',
]

# note: The contracts will be compiled via subprocess using truffle compile this is maily because the current versions
#  for py-solcx and py-sol reports an error while trying to access the mock contracts in GnosisSafe Project.
def gnosis_test():
    tx_history = TransactionHistoryManager()
    ganache_provider = GanacheProvider()
    # review: Fix Type Warning expected str recieved List[str]
    contract_interface = ContractInterface(ganache_provider.get_provider(), PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    # deploy_contract() will call compile_source_files() if the contract is not yet compiled.
    contract_artifacts = contract_interface.deploy_contract()

    print(contract_artifacts['GnosisSafe']['address'])
    print(contract_artifacts['Proxy']['address'])
    safe_instance = contract_interface.get_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_instance(contract_artifacts['Proxy'])

    gnosis_safe_module = GnosisSafeModule(ganache_provider.get_provider(), contract_artifacts)
    functional_safe = gnosis_safe_module.setup(safe_instance, proxy_instance)

    print('\nTesting Basic Calls')
    print('---------' * 10)
    print(functional_safe.functions.NAME().call())
    print(functional_safe.functions.VERSION().call())
    print(functional_safe.functions.isOwner('0xe982E462b094850F12AF94d21D470e21bE9D0E9C').call())
    print(functional_safe.functions.isOwner('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call())
    print(functional_safe.functions.getThreshold().call())
    print(functional_safe.functions.getOwners().call())
    print('Done.')

    print('\nBasic Transfer Calls Withing Ganache Accounts, Random Account & Proxy Safe')
    print('---------' * 10)

    account = Account.create()
    random_account_address = account.address
    random_private_key = account.privateKey

    print('Generate Account()')
    print(' + Random Address: ', random_account_address)
    print(' + Random Private Key: ', random_private_key)
    print('Done.\n')

    provider = ganache_provider.get_provider()
    account2 = provider.eth.accounts[2]
    print('-------' * 10)
    print('From Ganache Account To Random Account Transfer')
    print(' + Balance in Safe Proxy Account: ', provider.eth.getBalance(str(contract_artifacts['Proxy']['address'])))
    print(' + Balance in Random Account: ', provider.eth.getBalance(str(random_account_address)))
    print(' + Balance in Ganache Account: ', provider.eth.getBalance(str(account2)))
    print('Done.\n')

    tx_data0 = dict(
        nonce=provider.eth.getTransactionCount(str(account2)),
        gasPrice=provider.eth.gasPrice,
        gas=100000,
        to=str(random_account_address),
        value=provider.toWei(1, 'ether')
    )
    private_key_account2 = '0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c'
    signed_txn = provider.eth.account.signTransaction(tx_data0, private_key_account2)
    tmp_txn_hash = provider.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    receipt_txn_hash = provider.eth.waitForTransactionReceipt(tmp_txn_hash)
    tx_history.add_tx_to_history(ganache_provider['name'], account2, receipt_txn_hash, tx_data0)

    print('-------' * 10)
    print('[ Summary ]: From Ganache Account To Random Account Transfer')
    print(' + Balance in Safe Proxy Account: ', provider.eth.getBalance(str(contract_artifacts['Proxy']['address'])))
    print(' + Balance in Random Account: ', provider.eth.getBalance(str(random_account_address)))
    print(' + Balance in Ganache Account: ', provider.eth.getBalance(str(account2)))
    print('Done.\n')

    tx_data1 = dict(
        nonce=provider.eth.getTransactionCount(str(random_account_address)),
        gasPrice=provider.eth.gasPrice,
        gas=100000,
        to=str(contract_artifacts['Proxy']['address']),
        value=provider.toWei(0.9, 'ether')
    )

    random_acc_signed_txn = provider.eth.account.signTransaction(tx_data1, random_private_key)
    random_acc_tmp_txn_hash = provider.eth.sendRawTransaction(random_acc_signed_txn.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    random_acc_receipt_txn_hash = provider.eth.waitForTransactionReceipt(random_acc_tmp_txn_hash)

    tx_history.add_tx_to_history(ganache_provider['name'], random_account_address, random_acc_receipt_txn_hash, tx_data1)
    print('-------' * 10)
    print('[ Summary ]: From Random Account To Proxy Safe Account Transfer')
    print(' + Balance in Safe Proxy Account: ', provider.eth.getBalance(str(contract_artifacts['Proxy']['address'])))
    print(' + Balance in Random Account: ', provider.eth.getBalance(str(random_account_address)))
    print(' + Balance in Ganache Account: ', provider.eth.getBalance(str(account2)))
    print('Done.\n')
    print('-------' * 10)
    print('[ Summary ]: Transaction History')
    print(tx_history.history)
    print('Done.\n')
    gnosis_safe_methods = ganache_provider.map_contract_methods(proxy_instance)

    for item in gnosis_safe_methods:
        gnosis_safe_cli_completer.append(gnosis_safe_methods[item]['function_name'])
        # print(gnosis_safe_methods[item]['function_input'], '->', gnosis_safe_methods[item]['function_input'])
    gnosis_cli = GnosisConsoleInput()
    gnosis_cli.run(gnosis_safe_methods, proxy_instance, WordCompleter(gnosis_safe_cli_completer, ignore_case=True))

def main():
    gnosis_test()


if __name__ == '__main__':
    main()

