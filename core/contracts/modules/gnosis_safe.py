#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# reference: (Ethereum Interface) https://medium.com/hackernoon/creating-a-python-ethereum-interface-part-1-4d2e47ea0f4d
# reference: (Safe Code) https://github.com/gnosis/safe-contracts/blob/development/test/gnosisSafeDeploymentViaTx.js
# reference: (Safe Project) https://github.com/gnosis/safe-contracts

# Import Web3 Module
from web3 import Web3
from eth_account import Account

# Import Constant
from core.providers.constants.contract_contants import NULL_ADDRESS

# Import Contract Reader
from core.providers.utils.build_contract_reader import BuildContractReader

# note: Contract Operations
#  + When ever we need to operate with the current contract, doing a operation
#  that modifies the contract, 'transact()' must be used
#  + When ever we need to operate with the current contract, doing a operation
#  that queries the contract, 'call()' must be used

# note: Setup Method 1:
#  - Deployment of GnosisSafe
#    + init via gnosis_safe_contract.setup().transact()
#  - Deployment of Proxy
#   + init via proxy_contract.contructor().transact()

class GnosisSafeModule:
    """ Gnosis Safe Module
    This module will provide the set of functions needed to interact with the Gnosis Safe through the commandline
    """
    def __init__(self, _provider, _contract_artifacts, logger=''):
        self.name = self.__class__.__name__
        self.provider = _provider
        self.build_contract_reader = BuildContractReader()
        self.logger = logger
        self.provider = _provider
        self.contract_artifacts = _contract_artifacts

    def __setup_accounts(self):
        return


    def setup(self, gnosissafe_instance, proxy_instance):
        """ Setup
        This function will finish the setup the Gnosis Safe Contract through the proxy contract
            :return:
        """
        try:
            # Setup for GnosisSafe & Proxy Accounts
            account0 = self.provider.eth.accounts[0]
            account1 = self.provider.eth.accounts[1]
            account2 = self.provider.eth.accounts[2]
            list_of_accounts = [account0, account1, account2]

            gnosissafe_instance.functions.setup(list_of_accounts, 3, NULL_ADDRESS, b'', NULL_ADDRESS, NULL_ADDRESS, 0, NULL_ADDRESS).transact({'from': account0})
            proxy_instance.functions.setup(list_of_accounts, 2, NULL_ADDRESS, b'', NULL_ADDRESS, NULL_ADDRESS, 0, NULL_ADDRESS).transact({'from': account0})
            return proxy_instance
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

    # todo:
    # def multi_sign_transaction(self):
        # pasarle el proxy
        # pasarle la cuenta random con saldo
        # getHash de la operacion que queremos


    # new_account_address = account.address
    # new_account_private_key = account.privateKey
    # note: block of multisign
    #  txHash = await gnosisSafe.getTransactionHash(to, value, data, operation, 0, 0, 0, 0, 0, nonce)
    # nonce_safe = new_proxy_trans.nonce()
    # print(nonce_safe)
    # txHash = new_proxy_trans.functions.getTransactionHash().call()
    # aprove_tx = ''
    # Based On the Threshold
    # owner1_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
    # owner2_sign = account.signHash(message_hash=txHash, private_key=account.privateKey)
    # new_proxy_trans.functions.approveHash(txHash).transact()
    # new_proxy_trans.functions.approveHash(txHash).transact()
    # new_proxy_trans.functions.execTransaction()

    # deterministic_accounts = self.get_account_information()
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
