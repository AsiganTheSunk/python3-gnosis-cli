#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.providers.ganache_provider import NULL_ADDRESS

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

# Todo: Finish the multi sign Transaction for the proxy contract.
# note: The contracts will be compiled via subprocess using truffle compile this is maily because the current versions
#  for py-solcx and py-sol reports an error while trying to access the mock contracts in GnosisSafe Project.

# Import Web3
from web3 import Web3


def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def call_gnosis_console():
    # print('Launching Gnosis Console')
    # gnosis_safe_methods = ganache_provider.map_contract_methods(proxy_instance)
    # for item in gnosis_safe_methods:
    #     gnosis_safe_cli_completer.append(gnosis_safe_methods[item]['function_name'])
    #     # print(gnosis_safe_methods[item]['function_input'], '->', gnosis_safe_methods[item]['function_input'])
    # gnosis_cli = GnosisConsoleInput()
    # gnosis_cli.run(gnosis_safe_methods, proxy_instance, WordCompleter(gnosis_safe_cli_completer, ignore_case=True))
    return


def multi_sign_tx(signers, tx_hash):
    """

    :param self:
    :param signers:
    :param tx_hash:
    :return:
    """

    very_important_data = [Account.from_key(signers[0]), Account.from_key(signers[1])]
    print('Input signers', signers)
    # generar Account y ordenar por address.

    orderred_signers = sorted(very_important_data, key=lambda v: v.address.lower())
    print('Ordered Signers', orderred_signers)
    signature_bytes = b''
    for private_key in signers:
        tx_signature = Account.signHash(tx_hash, private_key)
        signature_bytes += tx_signature['signature']

    print('[ Output Signature ]: ' + signature_bytes.hex())
    return signature_bytes

# 0x00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000
# 0x519ac607c6c6a7efc4875850dd94ed8481b640690970f5cd7b6f131f3ef0f5450x23f57809a0938c7c61e4ebad27d7bc2580c5ac5592dd9086e6e478d5db2fbed10x000000000000000000000000000000000000000000000000000000000000001b0x55e191536a3a87340489f6b49839411bc8d253503d309c3fab1aaf3e9d1a64180x2f5bad903e2db05329f45b756e13c7a7db839937bef0f5f02c71802254a3cc510x000000000000000000000000000000000000000000000000000000000000001c

def gnosis_test():
    tx_history = TransactionHistoryManager()
    ganache_provider = GanacheProvider()
    contract_interface = ContractInterface(ganache_provider.get_provider(), PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    # deploy_contract() will call compile_source_files() if the contract is not yet compiled.
    contract_interface.compile_source_files()
    contract_artifacts = contract_interface.deploy_contract()

    print(contract_artifacts['GnosisSafe']['address'])
    print(contract_artifacts['Proxy']['address'])
    safe_instance = contract_interface.get_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_instance(contract_artifacts['Proxy'])

    gnosis_safe_module = GnosisSafeModule(ganache_provider.get_provider(), contract_artifacts)
    functional_safe = gnosis_safe_module.setup(safe_instance, proxy_instance)

    print('\n[ Testing Basic Calls ]')
    print('---------' * 10)
    print(functional_safe.functions.NAME().call())
    print(functional_safe.functions.VERSION().call())
    print(functional_safe.functions.isOwner('0xe982E462b094850F12AF94d21D470e21bE9D0E9C').call())
    print(functional_safe.functions.isOwner('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call())
    print(functional_safe.functions.getThreshold().call())
    print(functional_safe.functions.getOwners().call())
    print('Done.')

    print('\n[ Basic Transfer Calls Withing Ganache Accounts, Random Account & Proxy Safe ]')
    print('---------' * 10)

    account = Account.create()
    random_account_address = account.address
    random_private_key = account.privateKey

    print('[ Generate Account() ]')
    print(' (+) Random Address: ', random_account_address)
    print(' (+) Random Private Key: ', random_private_key)
    print('Done.\n')

    provider = ganache_provider.get_provider()
    account2 = provider.eth.accounts[2]
    account1 = provider.eth.accounts[1]
    private_key_account1 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'
    private_key_account2 = '0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c'

    print('-------' * 10)
    print('[ Summary ]: From Ganache Account To Random Account Transfer')
    print(' (+) Balance in Safe Proxy Account: ', provider.eth.getBalance(str(contract_artifacts['Proxy']['address'])))
    print(' (+) Balance in Random Account: ', provider.eth.getBalance(str(random_account_address)))
    print(' (+) Balance in Ganache Account: ', provider.eth.getBalance(str(account2)))
    print('Done.\n')

    # Tx Data
    tx_data0 = dict(
        nonce=provider.eth.getTransactionCount(str(account2)),
        gasPrice=provider.eth.gasPrice,
        gas=100000,
        to=str(random_account_address),
        value=provider.toWei(0.1, 'ether')
    )
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

    # Tx Data
    tx_data1 = dict(
        nonce=provider.eth.getTransactionCount(str(random_account_address)),
        gasPrice=provider.eth.gasPrice,
        gas=100000,
        to=str(contract_artifacts['Proxy']['address']),
        value=provider.toWei(.09, 'ether')
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

    # note: Send Money to a Newly created account in the network, and lastly beetween safes?
    # note: Make Tx from the Safe
    # reference: https://gnosis-safe.readthedocs.io/en/version_0_0_2/services/relay.html
    # reference: https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed/761#761
    # note: The proxy contract implements only two functions: The constructor setting the address of the master copy
    multi_sig_to = Account.create()
    multi_sig_address = multi_sig_to.address
    multi_sig_private_key = multi_sig_to.privateKey
    print('[ Generate Account() ]')
    print(' (+) 2ºRandom Address: ', multi_sig_address)
    print(' (+)) 2ºRandom Private Key: ', multi_sig_private_key)
    print('Done.\n')

    CREATE = 2
    DELEGATE_CALL = 1
    CALL = 0

    # VARIABLES IN THE MULTISIGN EXAMPLE
    address_to = multi_sig_address
    value = provider.toWei(0.8, 'ether')
    data = b''
    operation = CALL
    safe_tx_gas = 300
    base_gas = 10
    gas_price = 0
    address_gas_token = NULL_ADDRESS
    address_refund_receiver = NULL_ADDRESS
    nonce = functional_safe.functions.nonce().call()

    tx_hash_multi_sign = functional_safe.functions.getTransactionHash(
        address_to, value, data, operation, safe_tx_gas, base_gas, gas_price, address_gas_token, address_refund_receiver, nonce
    ).call()

    # very_important_data = [Account.from_key(private_key_account1)]
    very_important_data = [Account.from_key(private_key_account1), Account.from_key(private_key_account2)]
    print('Input signers', very_important_data)
    # generar Account y ordenar por address.

    orderred_signers = sorted(very_important_data, key=lambda v: v.address.lower())
    print('Ordered Signers', orderred_signers[0].privateKey, orderred_signers[0].address)
    print('Ordered Signers', orderred_signers[1].privateKey, orderred_signers[1].address)

    signature_bytes = b''
    for signers in orderred_signers:
        tx_signature = signers.signHash(tx_hash_multi_sign)
        signature_bytes += tx_signature['signature']
    print('[ Output Signature ]: ' + signature_bytes.hex())

    functional_safe.functions.approveHash(tx_hash_multi_sign).transact({'from': account1})
    functional_safe.functions.approveHash(tx_hash_multi_sign).transact({'from': account2})
    functional_safe.functions.execTransaction(
        address_to, value, data, CALL, safe_tx_gas, base_gas, gas_price, address_gas_token, address_refund_receiver, signature_bytes
    ).transact({'from': account1})

    print('-------' * 10)
    print('[ Summary ]: From Random Account To Proxy Safe Account Transfer')
    print(' + Balance in Safe Proxy Account: ', provider.eth.getBalance(str(contract_artifacts['Proxy']['address'])))
    print(' + Balance in Random Account: ', provider.eth.getBalance(str(address_to)))
    print('Done.\n')


    # todo: Build a payload with buildTrasaction with gas:0, gasPrices:0, ... to call for the AccountManager in the Safe.
    #  Then Call execTransaction() with addOwner, removeOwner, SwapOnwer, changeThreshold etc etc
    #  functional_safe.functions.addOwnerWithThreshold().call()
    #  functional_safe.functions.removeOwner().call()
    #  functional_safe.functions.swapOwner().call()

    # remark: Transaction Flow Change Threshold from 1 to 2
    #  Get Account 1

    #  Build Transaction
    transaction = functional_safe.functions.changeThreshold(2).buildTransaction({'from': orderred_signers[0].address})
    transaction.update({'gas': 0})
    transaction.update({'gasPrice': 0})
    transaction.update({'nonce': nonce})

    print(transaction)
    # Using the Payload from buildTransaction, getTransactionHash
    tx_change_threshold = functional_safe.functions.getTransactionHash(
        address_to, value, transaction['data'], operation, safe_tx_gas, base_gas, gas_price, address_gas_token, address_refund_receiver, nonce
    ).call()

    # Sign Transaction Hash
    tx_change_threshold_signature = orderred_signers[0].signHash(tx_change_threshold)
    print('[ Output Signature ]: ' + tx_change_threshold_signature['signature'].hex())

    # Approve Transaction Hash
    # functional_safe.functions.approveHash(tx_change_threshold).transact({'from':  current_account.address})
    # Launch Transaction Hash
    functional_safe.functions.execTransaction(
        address_to, value, transaction['data'], CALL, safe_tx_gas, base_gas, gas_price, address_gas_token, address_refund_receiver,
        tx_change_threshold_signature['signature']
    ).transact({'from': orderred_signers[0].address})


def main():
    gnosis_test()


if __name__ == '__main__':
    main()

