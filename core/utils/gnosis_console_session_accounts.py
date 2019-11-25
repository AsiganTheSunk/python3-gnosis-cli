#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Eth Account Package
from eth_account import Account

# Import Deterministic Ganache Account Information (Address, Private Key)
from core.constants.ganache_constants import DETERMINISTIC_ACCOUNT_INFORMATION as ganache_data

# Import HexBytes Package
from hexbytes import HexBytes

class ConsoleSessionAccounts:
    def __init__(self):
        self.account_data = {'NULL': {'address': '0x' + '0' * 40, 'private_key': HexBytes('')}}
        self._setup_ganache_accounts()
        self._setup_random_accounts()

    def add_account(self, address, private_key='', alias='uAccount'):
        if private_key != '':
            tmp_account = Account.from_key(private_key)
            self.account_data[alias + str(len(self.account_data)-1)] = {'address': tmp_account.address, 'private_key': tmp_account.privateKey}
            return self.account_data
        else:   # Todo: Validate Address
            self.account_data[alias + str(len(self.account_data)-1)] = {'address': address, 'private_key': HexBytes(private_key)}
            return self.account_data

    def _setup_random_accounts(self, account_number=10):
        for index in range(1, account_number, 1):
            tmp_account = Account.create()
            self.account_data['rAccount' + str(index)] = {'address': tmp_account.address, 'private_key': tmp_account.privateKey}
        return self.account_data

    def _setup_ganache_accounts(self):
        for index, data in enumerate(ganache_data):
            tmp_account = Account.from_key(ganache_data[data]['private_key'])
            self.account_data['gAccount' + str(index)] = {'address': tmp_account.address, 'private_key': tmp_account.privateKey}

    def _evaluate_account_data(self, stream):
        for item in self.account_data:
            if stream.startswith(item):
                key = stream.split('.')[1]
                print(stream, item, self.account_data[item][key])
                return self.account_data[item][key]


def main():
    # Todo newContract BUILD_PATH or address, ABI
    aux = ConsoleSessionAccounts()
    stream = 'gAccount0.address'
    aux._evaluate_account_data(stream)




if __name__ == '__main__':
    main()


# INPUT TESTS
query_is_owner = 'isOwner --address=0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 --query'
execute_swap_owner = 'swapOwner --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002 --from=0x00000000000000000000000000000003 --execute'
query_get_owners = 'getOwners --query'
query_execTransaction_not_enough_args = 'execTransaction --queue --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002'