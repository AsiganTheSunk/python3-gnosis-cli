#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.utils.gnosis_console_session_accounts import ConsoleSessionAccounts

def main():
    # remark:
    # todo: newContract BUILD_PATH or address, ABI, Rework of the loadContract to avoid constant migration
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