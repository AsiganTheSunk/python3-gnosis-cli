#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Todo: Lexer per init of console, type of session, so emun to flag the type focusing on usability in the future
# Todo: Module loader, so it can run the setup for the contract you want to operate with
# Todo: Report the pos of the word to the lexer so it can know if it's dealing with a call to a function or an param
# Todo: Build the suffix + affix list for the management of simple contracts
# Todo: Improve function mapping so it can properly separate Events(Emit's) from the contract methods from the actual functions
# Todo: Maybe Add a listener for the Events done by the contract atleast locally so it can be studied how it behaves
# Todo: Add Interface for the Common Contract Operations Setup(), Transact() etc etc so it can be called from the console
#   If None are provided, the console will assume an standar way of operation for the basic known transaction procedures
# Todo: Move Current "Setup" for the GnosisSafe to it's proper module
# Todo: Move Current "Transact" overrider to the GnosisSafe module
# Todo: Only add to the temporal lexer valid addresses (it has been operated with)

# validator = Validator.from_callable(
#     is_valid_address, error_message='Not a valid address (Does not contain an 0x).', move_cursor_to_end=True
# )

query_is_owner = 'isOwner --address=0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 --query'
execute_swap_owner = 'swapOwner --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002 --from=0x00000000000000000000000000000003 --execute'
query_get_owners = 'getOwners --query'
query_execTransaction_not_enough_args = 'execTransaction --queue --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002'


# # remark: transact with arguments
# # note: could be autofilled if not provided and set in the console session
# #
#
# # kwown arguments gas:, gasPrices:, nonce:, from:
#
# #     # nonce = functional_safe.functions.nonce().call()
# #     # transaction = functional_safe.functions.changeThreshold(3).buildTransaction({'from': orderred_signers[0].address})
# #     # transaction.update({'gas': base_gas})
# #     # transaction.update({'gasPrice': gas_price})
# #     # transaction.update({'nonce': nonce})
#
# # note: --from=, --gas=, nonce=, gasprice=
#
# import re
#
# def is_alphanumeric_addres(stream):
#     data = re.search(r'^(0x)?[0-9a-f]{40}$', stream).group(0)
#     print('data', data)
#     return
#
# # def validated(stream):
# #     # remark: evaluate the data been passed to the contracts by searching it's current value,key
# #     if is_alphanumeric_addres(stream):
# #         return
# #     return
#
# is_valid_address = r'^(0x)?[0-9a-f]{40}$'
# is_62_valid_address = r'^(0x)?[0-9a-f]{62}$'
#
# def print_kwargs(**kwargs):
#     new_values = ''
#     for key, value in kwargs.items():
#         if key.strip('_') in ['from', 'gas']: # and validated(key, value):
#             new_values += '\'{0}\':{1},'.format(key.strip('_'), value)
#             print(new_values)
#     return new_values
#
# aux = print_kwargs(_from="Shark", gas=4.5)
#
# data_to_print = 'data_to_be_printed.transact{%s}' % (aux[:-1])
# print(data_to_print)
#
# from ethereum import utils
#
# def checksum_encode(addr): # Takes a 20-byte binary address as input
#     o = ''
#     v = utils.big_endian_to_int(utils.sha3(addr.hex()))
#     for i, c in enumerate(addr.hex()):
#         if c in '0123456789':
#             o += c
#         else:
#             o += c.upper() if (v & (2**(255 - 4*i))) else c.lower()
#         print(o)
#     return '0x'+o
#
# def some_args(arg_1, arg_2, arg_3):
#     print("arg_1:", arg_1)
#     print("arg_2:", arg_2)
#     print("arg_3:", arg_3)
#
# my_list = [2, 3]
# some_args(1, *my_list)
#
# # Doble input:
# # for i in range(0, n):
# #     ele = [input(), int(input())]
#
# # https://ethereum.stackexchange.com/questions/1374/how-can-i-check-if-an-ethereum-address-is-valid
# # ^(0x)?[0-9a-f]{40}$
# # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md#implementation
#
# from hexbytes import HexBytes
# from web3 import Web3
#
# def test(addrstr):
#     assert(addrstr == Web3.toChecksumAddress(addrstr))
#
# print(Web3.toChecksumAddress('0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed'))
# print(Web3.toChecksumAddress('0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359'))
# print(Web3.toChecksumAddress('0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB'))
# print(Web3.toChecksumAddress('0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb'))
#
# from web3 import Web3
# execute = True
#
# # Currency Utility
# # Gather all the --Gwei, --Kwei etc etc sum up them and give the ''
# if execute:
#     Web3.fromWei(1000000000000000000, 'Gwei')
# #Web3.toWei()
# #Web3.fromWei()
#
# # Address Utility
# Web3.isAddress('0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed')
# Web3.isChecksumAddress('0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed')
#
# payload_options = ['alias', 'from', 'gas', 'gasPrice']
# transaction_payload_options = ['alias', 'from', 'gas', 'gasPrice', 'nonce', '']
#

from gnosis.eth.ethereum_client import EthereumClient
from gnosis.eth.contracts import contracts
from gnosis.safe.tests.safe_test_case import Safe


from eth_account import Account
local_account = Account.privateKeyToAccount('0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')
ethereum_client = EthereumClient()

contract_data = Safe.deploy_master_contract(ethereum_client, local_account)
print(contract_data)

# def send(function_, *tx_args, event=None, tx_params=None):
#     """Contract agnostic transaction function with extras
#
#     Builds a transaction, estimates its gas and compares that to max_tx_gas
#     defined on init. Sends the transaction, waits for the receipt and prints
#     a number of values about the transaction. If an event is supplied, it
#     will capture event output, clean it, and return it.
#
#     Parameters:
#         function_(str): name of the function in your contract you wish to
#         send the transaction to
#         tx_args(list): non-keyworded function arguments to be supplied
#         in the order they are defined in contract source
#         event(str): name of event (if any) you expect to be emmitted from
#         contract
#         tx_params(dict): optional dictionary for overloading the
#         default deployment transaction parameters. See web3.py's
#         eth.sendTransaction for more info.
#
#     Returns:
#         receipt(AttributeDict): immutable dict containing various
#         transaction outputs
#         cleaned_events(dict): optional output of cleaned event logs
#     """
#
#     fxn_to_call = getattr(self.contract_instance.functions, function_)
#     built_fxn = fxn_to_call(*tx_args)
#
#     gas_estimate = built_fxn.estimateGas(transaction=tx_params)
#     print(f"Gas estimate to transact with {function_}: {gas_estimate}\n")
#
#     if gas_estimate < self.max_tx_gas:
#
#         print(f"Sending transaction to {function_} with {tx_args} as arguments.\n")
#
#         tx_hash = built_fxn.transact(transaction=tx_params)
#
#         receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
#
#         print((
#             f"Transaction receipt mined with hash: {receipt['transactionHash'].hex()} "
#             f"on block number {receipt['blockNumber']} "
#             f"with a total gas usage of {receipt['cumulativeGasUsed']}\n"
#         ))
#
#         # if event is not None:
#         #
#         #     event_to_call = getattr(self.contract_instance.events, event)
#         #     raw_log_output = event_to_call().processReceipt(receipt)
#         #     #indexed_events = clean_logs(raw_log_output)
#         #
#         #     return receipt, indexed_events
#
#         # else:
#         return receipt
#
#     else:
#         print("Gas cost exceeds {}".format(self.max_tx_gas))
