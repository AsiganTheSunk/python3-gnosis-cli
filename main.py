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


def string_to_bytes32(data):
    """ String To Bytes32 (Hex)

    :param data:
    :return:
    """
    if len(data) > 32:
        bytes32 = data[:32]
    else:
        bytes32 = data.ljust(32, '0')
    return bytes(bytes32, 'utf-8')


def multi_sign_tx(_signers, _tx_hash):
    """

    :param self:
    :param _signers:
    :param _tx_hash:
    :return:
    """
    account = Account()
    signature_bytes_aux = ''
    for private_key in _signers:
        tx_signature = account.signHash(_tx_hash, private_key)
        print(tx_signature['r'], len(str(tx_signature['r'])), hex(tx_signature['r']))
        print(tx_signature['s'], len(str(tx_signature['s'])), hex(tx_signature['s']))
        print(tx_signature['v'], len(str(tx_signature['v'])), hex(tx_signature['v']))
        signature_bytes_aux += hex(tx_signature['r'] + tx_signature['s'] + tx_signature['v'])
        # signature_bytes_aux += int(tx_signature['r']).to_bytes(32, byteorder='big') + int(tx_signature['s']).to_bytes(32, byteorder='big') + int(tx_signature['v']).to_bytes(32, byteorder='big')
    print(signature_bytes_aux)
    return bytes(signature_bytes_aux, 'utf-8')

def gnosis_test():
    tx_history = TransactionHistoryManager()
    ganache_provider = GanacheProvider()
    # review: Fix Type Warning expected str recieved List[str]
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
    account1 = provider.eth.accounts[1]
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
    private_key_account1 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'
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

    # note: Send Money to a Newly created account in the network, and lastly beetween safes?
    nonce = provider.eth.getTransactionCount(str(contract_artifacts['Proxy']['address']))
    print('Proxy Address Nonce: ', nonce)
    _multi_sig_to = Account.create()
    racc_multi_sig_address = _multi_sig_to.address
    racc_multi_sig_private_key = _multi_sig_to.privateKey
    print('Generate Account()')
    print(' + 2ºRandom Address: ', racc_multi_sig_address)
    print(' + 2ºRandom Private Key: ', racc_multi_sig_private_key)
    print('Done.\n')

    DELEGATE_CALL = 1
    CALL = 0

    tx_hash_to_multi_sign = functional_safe.functions.getTransactionHash(racc_multi_sig_address, provider.toWei(0.8, 'ether'), b'', DELEGATE_CALL, 10000, 100000, 1000, NULL_ADDRESS, NULL_ADDRESS, nonce).call()
    print('TxMultiSignHash: ' + str(tx_hash_to_multi_sign))
    # transaction_hash = codecs.decode(tx_multi_sign_hash, 'hex_codec')
    signers = [private_key_account1, private_key_account2]
    multi_signature = multi_sign_tx(signers, tx_hash_to_multi_sign)
    print('MultiSignature: ' + str(multi_signature))

    functional_safe.functions.approveHash(tx_hash_to_multi_sign).transact({'from': account1})
    functional_safe.functions.approveHash(tx_hash_to_multi_sign).transact({'from': account2})
    functional_safe.functions.execTransaction(racc_multi_sig_address, provider.toWei(0.8, 'ether'), b'', DELEGATE_CALL, 10000, 100000, 1000, NULL_ADDRESS, NULL_ADDRESS, multi_signature).transact({'from': account1})

    # reference: https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed/761#761
    # bug: TypeError while passing the txHash for the operation to approve

    # Sign Operation: Onwer1, Onwer2 with each private key respectively

    # Transaction Flow:
    # reference: https://gnosis-safe.readthedocs.io/en/version_0_0_2/services/relay.html

    # print('Onwer 1 Sign', owner1_signed_message)
    # print('Owner 2 Sign', owner2_signed_message)
    # print('Done.\n')
    # note: The proxy contract implements only two functions: The constructor setting the address of the master copy
    # and the fallback function forwarding all transactions sent to the proxy via a DELEGATECALL to the master copy and
    # returning all data returned by the DELEGATECALL.

    # print(nonce_safe)
    # txHash = new_proxy_trans.functions.getTransactionHash().call()
    # aprove_tx = ''
    # Based On the Threshold
    # owner1_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
    # owner2_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
    # new_proxy_trans.functions.approveHash(txHash).transact()
    # new_proxy_trans.functions.approveHash(txHash).transact()
    # new_proxy_trans.functions.execTransaction()

    # print('Launching Gnosis Console')
    # gnosis_safe_methods = ganache_provider.map_contract_methods(proxy_instance)
    # for item in gnosis_safe_methods:
    #     gnosis_safe_cli_completer.append(gnosis_safe_methods[item]['function_name'])
    #     # print(gnosis_safe_methods[item]['function_input'], '->', gnosis_safe_methods[item]['function_input'])
    # gnosis_cli = GnosisConsoleInput()
    # gnosis_cli.run(gnosis_safe_methods, proxy_instance, WordCompleter(gnosis_safe_cli_completer, ignore_case=True))


def main():
    gnosis_test()


if __name__ == '__main__':
    main()

