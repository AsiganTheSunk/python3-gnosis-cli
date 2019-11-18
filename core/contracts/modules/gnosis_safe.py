#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Web3 Module
from web3 import Web3
from eth_account import Account

# Import Constant
from core.providers.constants.contract_contants import NULL_ADDRESS

# Import Contract Reader
from core.providers.utils.build_contract_reader import BuildContractReader

class GnosisSafeModule:
    """ Gnosis Safe Module
    This module will provide the set of functions needed to interact with the Gnosis Safe through the commandline
    """
    def __init__(self, _provider, logger):
        self.name = self.__class__.__name__
        self.provider = _provider
        self.build_contract_reader = BuildContractReader()
        self.logger = logger


    def __setup_accounts(self):
        return


    def setup(self, _provider, contract_abi, contract_address):
        """ Setup
        This function will setup the Gnosis Safe Contract

            :param _provider:
            :param contract_abi:
            :param contract_address:
            :return:
        """
        current_provider = _provider.get_current_provider()
        gnosis_safe_contract_abi, gnosis_safe_contract_bytecode = self.build_contract_reader.read_from()
        gnosis_proxy_contract_abi, gnosis_safe_contract_bytecode = self.build_contract_reader.read_from()

        gnosis_safe_contract = current_provider.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)
        gnosis_proxy_contract = current_provider.eth.contract(bytecode=BYTE_CODE_PROXY, abi=ABI_PROXY)

        try:
            # Completing Setup
            account0 = current_provider.eth.accounts[0]
            account1 = current_provider.eth.accounts[1]
            account2 = current_provider.eth.accounts[2]
            list_of_accounts = [account0, account1, account2]

            # master_safe_copy = current_contract.functions.setup(list_of_accounts, 3, '0x' + '0'*40, bytes('0x', 'utf-8'), account0, account0, 0, account0).transact({'from':account1})

            self.logger.info('Master Safe Copy Setup  Done!!')
            print('address to master_safe_copy: ', gnosis_safe_contract.address)
            # print(current_contract.functions.getOwners().call())
            # print(current_contract.functions.getThreshold().call())

            # Setting up the contract address to the proxy to aim at
            tx_hash = gnosis_proxy_contract.constructor(gnosis_safe_contract.address).transact({'from': account1})
            self.logger.info('Proxy Safe Setup Done!!')
            tx_receipt = current_provider.eth.waitForTransactionReceipt(tx_hash)
            new_proxy_trans = current_provider.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)

            tx_proxy = new_proxy_trans.functions.setup(
                list_of_accounts, 2, NULL_ADDRESS, bytes('0x', 'utf-8'),
                NULL_ADDRESS, NULL_ADDRESS, 0, NULL_ADDRESS
            ).transact({'from': account1})

            new_proxy_address = str(tx_receipt.contractAddress)
            print('Proxy Addr: ', new_proxy_address)

        except Exception as err:
            print(err)
        return

    def standard_safe_query(self):
        return

    def standard_safe_transaction(self, _provider, _account_to, _account_from_private_key, _account_from, _ether_value=1):
        """ Standard Safe Transaction
        This function will ...

            :param _provider:
            :param _account_to:
            :param _account_from_private_key:
            :param _account_from:
            :param _ether_value:
            :return:
        """
        try:
            signed_txn = _provider.eth.account.signTransaction(
                dict(
                    nonce=_provider.eth.getTransactionCount(str(_account_from)),
                    gasPrice=_provider.eth.gasPrice,
                    gas=100000,
                    to=str(_account_to),
                    value=_provider.toWei(_ether_value, 'ether')
                    ), _account_from_private_key
            )
            signed_txn_hash = _provider.eth.sendRawTransaction(signed_txn.rawTransaction)
            return signed_txn_hash
        except Exception as err:
            print(err)
        return 'signed_txn_hash'

    def safe_transaction(self):
        return

    def safe_query(self):
        return


    def aux(self, current_provider, contract_address, contract_abi):
        BYTE_CODE_PROXY = ''
        ABI_PROXY = ''
        current_contract = None
        current_provider = None
        current_status = False
        functions_contract_data = {}

        # self.logger.info('{0} has successfully established a connection to {1} network'.format(self.name, self.network_name))
        current_contract = current_provider.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=contract_abi)
        proxy_contract = current_provider.eth.contract(bytecode=BYTE_CODE_PROXY, abi=ABI_PROXY)

        try:
            # Completing Setup
            account0 = current_provider.eth.accounts[0]
            account1 = current_provider.eth.accounts[1]
            account2 = current_provider.eth.accounts[2]
            list_of_accounts = [account0, account1, account2]

            # master_safe_copy = current_contract.functions.setup(list_of_accounts, 3, '0x' + '0'*40, bytes('0x', 'utf-8'), account0, account0, 0, account0).transact({'from':account1})

            # self.logger.info('Master Safe Copy Setup  Done!!')
            print('address to master_safe_copy: ', current_contract.address)
            # print(current_contract.functions.getOwners().call())
            # print(current_contract.functions.getThreshold().call())

            # Setting up the contract address to the proxy to aim at
            tx_hash = proxy_contract.constructor(current_contract.address).transact({'from': account1})
            # self.logger.info('Proxy Safe Setup Done!!')
            tx_receipt = current_provider.eth.waitForTransactionReceipt(tx_hash)
            new_proxy_trans = current_provider.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)

            # define null_address
            NULL_ADDRESS = '0x' + '0' * 40
            tx_proxy = new_proxy_trans.functions.setup(list_of_accounts, 2, NULL_ADDRESS, bytes('0x', 'utf-8'), NULL_ADDRESS,
                                                       NULL_ADDRESS, 0, NULL_ADDRESS).transact({'from': account1})

            import time

            time.sleep(1)
            new_proxy_address = str(tx_receipt.contractAddress)
            print('Proxy Addr: ', new_proxy_address)

            print('Testing Basic Calls')
            print(new_proxy_trans.functions.NAME().call())
            print(new_proxy_trans.functions.VERSION().call())
            print(new_proxy_trans.functions.isOwner('0xe982E462b094850F12AF94d21D470e21bE9D0E9C').call())
            print(new_proxy_trans.functions.isOwner('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1').call())
            print(new_proxy_trans.functions.getThreshold().call())
            print(new_proxy_trans.functions.getOwners().call())

            account = Account.create()

            new_account_address = account.address
            new_account_private_key = account.privateKey

            # note: block of multisign
            #  txHash = await gnosisSafe.getTransactionHash(to, value, data, operation, 0, 0, 0, 0, 0, nonce)
            nonce_safe = new_proxy_trans.nonce()
            print(nonce_safe)
            # # txHash = new_proxy_trans.functions.getTransactionHash().call()
            aprove_tx = ''
            # Based On the Threshold
            # owner1_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
            # owner2_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
            # new_proxy_trans.functions.approveHash(txHash).transact()
            # new_proxy_trans.functions.approveHash(txHash).transact()
            new_proxy_trans.functions.execTransaction()

            print('tx_transaction: ', )
            print('Generate Account() with Random Address: ', new_account_address)

            print('-------' * 10)
            print('Current Balance for Safe Proxy Account: ', current_provider.eth.getBalance(str(tx_receipt.contractAddress)))
            print('Current Balance for New Account: ', current_provider.eth.getBalance(str(new_account_address)))
            print('Current Balance for Ganache Account: ', current_provider.eth.getBalance(str(account2)))
            print('-------' * 10)

            private_key_account2 = '0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c'
            signed_txn = current_provider.eth.account.signTransaction(dict(
                nonce=current_provider.eth.getTransactionCount(str(account2)),
                gasPrice=current_provider.eth.gasPrice,
                gas=100000,
                to=str(new_account_address),
                value=current_provider.toWei(1, 'ether')
            ),
                private_key_account2)

            signed_txn_hash = current_provider.eth.sendRawTransaction(signed_txn.rawTransaction)

            print('-------' * 10)
            print('Current Balance for Safe Proxy Account: ', current_provider.eth.getBalance(str(tx_receipt.contractAddress)))
            print('Current Balance for New Account: ', current_provider.eth.getBalance(str(new_account_address)))
            print('Current Balance for Ganache Account: ', current_provider.eth.getBalance(str(account2)))
            print('-------' * 10)

            new_acc_signed_txn = current_provider.eth.account.signTransaction(dict(
                nonce=current_provider.eth.getTransactionCount(str(new_account_address)),
                gasPrice=current_provider.eth.gasPrice,
                gas=100000,
                to=str(tx_receipt.contractAddress),
                value=current_provider.toWei(0.9, 'ether')
            ),
                new_account_private_key)

            new_acc_signed_txn_hash = current_provider.eth.sendRawTransaction(new_acc_signed_txn.rawTransaction)

            print('-------' * 10)
            print('Current Balance for Safe Proxy Account: ', current_provider.eth.getBalance(str(tx_receipt.contractAddress)))
            print('Current Balance for New Account: ', current_provider.eth.getBalance(str(new_account_address)))
            print('Current Balance for Ganache Account: ', current_provider.eth.getBalance(str(account2)))
            print('-------' * 10)

            # deterministic_accounts = self.get_account_information()
            try:
                print()
                # new_proxy_trans.functions

                # safe_signed_txn = current_provider.eth.account.signTransaction(dict(
                #     nonce=current_provider.eth.getTransactionCount(str(tx_receipt.contractAddress)),
                #     gasPrice=current_provider.eth.gasPrice,
                #     gas=100000,
                #     to=str(tx_receipt.contractAddress),
                #     value=current_provider.toWei(0.9, 'ether')
                # ),
                #     private_key_account2)
                #
                # new_acc_signed_txn_hash = current_provider.eth.sendRawTransaction(safe_signed_txn.rawTransaction)
            except Exception as err:
                print('This should fail')
                print(err)
            #
            # accountTarget = str(tx_receipt.contractAddress)
            # accountList = [
            #     deterministic_accounts['account_1']['address'],
            #     deterministic_accounts['account_2']['address']]
            # privatekeys = [
            #     deterministic_accounts['account_1']['private_key'],
            #     deterministic_accounts['account_2']['private_key']
            # ]
            #
            # for i in range(0, len(accountList)):
            #     transaction = {
            #         'to': accountTarget,
            #         'value': current_provider.toWei(1, 'ether'),
            #         'gas': 200000,
            #         'gasPrice': current_provider.eth.gasPrice,
            #         'nonce': current_provider.eth.getTransactionCount(current_provider.toChecksumAddress(accountList[i])),
            #         'chainId': 1
            #     }
            #
            #     signed = current_provider.eth.account.signTransaction(transaction, privatekeys[i])
            #     current_provider.eth.sendRawTransaction(signed.rawTransaction)

            # note: Tx Transfer from Safe:
            #  CALL=0 Withdraw
            #  nonce = await gnosisSafe.nonce()
            #  txHash = await gnosisSafe.getTransactionHash(to, value, data, operation, 0, 0, 0, 0, 0, nonce)
            #  executeDataWithoutSignatures = gnosisSafe.contract.execTransaction.getData(to, value, data, operation, 0, 0, 0, 0, 0, "0x")
            #  approveData = gnosisSafe.contract.approveHash.getData(txHash)
            #  for i in accounts:
            #       sigs += "000000000000000000000000" + i.replace('0x', '') + "0000000000000000000000000000000000000000000000000000000000000000" + "01"
            #  executeDataUsedSignatures = gnosisSafe.contract.execTransaction.getData(to, value, data, operation, 0, 0, 0, 0, 0, sigs)
            #  tx = gnosisSafe.execTransaction(to, value, data, operation, 0, 0, 0, 0, 0, sigs, {from: txSender})
            #  _
            #  executeTransaction('executeTransaction withdraw 0.5 ETH', [accounts[0], accounts[2]], accounts[0], web3.toWei(0.5, 'ether'), "0x", CALL)
            #  _
            #  ethSign = async function(account, hash) {
            #     return new Promise(function(resolve, reject) {
            #     web3.currentProvider.sendAsync({
            #         jsonrpc: "2.0",
            #         method: "eth_sign",
            #         params: [account, hash],
            #         id: new Date().getTime()
            #     }, function(err, response)

