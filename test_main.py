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

# Todo: This should be moved to the ganache_provider.
# Import default deterministic account information for Ganache Provider
from core.providers.constants.ganache_constants import DETERMINISTIC_ACCOUNT_INFORMATION

from core.providers.utils.build_contract_reader import BuildContractReader
from core.contracts.contract_interface import ContractInterface


# Todo: Map Events Properly, and remove them from the list of functions
def map_contract_methods(contract_instance):
    """ Map Contract functions
    This function will map Events, Functions ( call , transact ), make distintions beetwen them? no input automatic query like function
    input but not output + doble Mayus name Event, otherwise functions with input,output transact it's required
    :param contract_instance:
    :return:
    """
    item_name = ''
    item_input = ''
    contract_methods = {}
    try:

        for index, item in enumerate(contract_instance.functions.__dict__['abi']):
            try:
                item_name = item['name']
            except KeyError:
                continue
            try:
                item_input = item['inputs']
            except KeyError:
                item_input = ''
            try:
                #<>

                metadata_arguments = []
                metadata_information = []
                stream_input = ''
                if len(item_input) >= 1:
                    for data_index, data in enumerate(item_input):
                        metadata_information.append({data_index: str(data['type']) + ' ' + str(data['name'])})
                        metadata_arguments.append({data_index: str(data['type'])})
                        stream_input += '{' + str(data_index) + '},'

                    contract_methods[index] = {
                        'name': item_name,
                        'arguments': metadata_arguments,
                        'argument_block': stream_input[:-1],
                        'metadata': metadata_information,
                        'call': 'contract_instance.functions.{0}('.format(item_name) + '{0}).call({1})',
                        'transact': 'contract_instance.functions.{0}('.format(item_name) + '{0}).transact({1})',
                    }
                else:
                    contract_methods[index] = {
                        'name': item_name,
                        'arguments': metadata_arguments,
                        'argument_block': stream_input,
                        'metadata': metadata_information,
                        'call': 'contract_instance.functions.{0}('.format(item_name) + '{0}).call({1})',
                        'transact': 'contract_instance.functions.{0}('.format(item_name) + '{0}).transact({1})',
                    }
            except Exception as err:
                print(type(err), err)

        # self.logger.info('{0} has successfully retrieved {1} elements from current contract'.format(self.name, len(
        #     contract_methods)))
        return contract_methods
    except Exception as err:
        print(err)


def __quote_argument(value):
    """ Quote Argument

    :param value:
    :return:
    """
    return QUOTE + value + QUOTE


def __get_method_argument_value(value):
    """ Get Method Argument Value

    :param value:
    :return:
    """
    return __quote_argument(value.split('=')[1])


def __get_input_method_arguments(argument_list, function_arguments):
    """ Get Input Method Arguments

    :param argument_list:
    :param function_arguments:
    :return:
    """
    arguments_to_fill = ''
    execute_value = False
    to_queue = False
    to_query = False
    address_from = ''
    aux_address_from = False
    argument_positions_to_fill = len(function_arguments)
    argument_positions_filled = 0

    for index, argument_item in enumerate(argument_list):
        if '--from=' in argument_item:
            address_from = __get_method_argument_value(argument_item)
            aux_address_from = True
        elif '--execute' == argument_item:
            if to_queue or to_query:
                print('--queue|--query value already parsed, this value will be ignored')
            else:
                execute_value = True
        elif '--query' == argument_item:
            if execute_value or to_queue:
                print('--execute|--queue value already parsed, this value will be ignored')
            else:
                to_query = True
        elif '--queue' == argument_item:
            if execute_value or to_query:
                print('--execute|--query value already parsed, this value will be ignored')
            else:
                to_queue = True
        else:
            for index, argument_type in enumerate(function_arguments):
                if argument_type[index] in argument_item and argument_positions_to_fill != 0 and argument_positions_to_fill > argument_positions_filled:
                    arguments_to_fill += __get_method_argument_value(argument_item) + COMA
                    argument_positions_filled += 1

            arguments_to_fill = arguments_to_fill[:-1]

    return argument_list[0], arguments_to_fill, address_from, execute_value, to_queue, to_query

# todo: move to the proper class all methods
QUOTE = '\''
COMA = ','
PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'


# todo:
def operate_with_contract(stream, contract_methods, contract_instance):
    """ Operate With Contract
    This function will retrieve the methods present & in the contract_instance
    :param stream:
    :param contract_methods:
    :param contract_instance:
    :return:
    """
    try:
        print(stream)
        for item in contract_methods:
            if contract_methods[item]['name'] in stream:
                splitted_stream = stream.split(' ')
                function_name, function_arguments, address_from, execute_flag, queue_flag, query_flag = __get_input_method_arguments(splitted_stream, contract_methods[item]['arguments'])
                print(__get_input_method_arguments(splitted_stream, contract_methods[item]['arguments']))

                if execute_flag or query_flag or queue_flag:
                    if execute_flag:
                        if contract_methods[item]['name'].startswith('get'):
                            print('WARNING: transact is usually discourage if you are calling a get function')
                        print(contract_methods[item]['transact'].format(function_arguments, address_from))
                    elif query_flag:
                        print(contract_methods[item]['call'].format(function_arguments, address_from))
                        print(eval(contract_methods[item]['call'].format(function_arguments, address_from)))
                    elif queue_flag:
                        print(contract_methods[item]['call'].format(function_arguments, address_from))
                        print('executeBatch when you are ready to launch the transactions that you queued up!')
                    print()
                else:
                    print('--execute, --query or --queue flag needed!')
    except Exception as err:  # KeyError
        print(err)

def main():


    # remark: Set Ganache Provider
    ganache_provider = GanacheProvider()
    provider = ganache_provider.get_provider()
    # remark: Link to the current contracts via ABI + Bytecode
    contract_interface = ContractInterface(provider, PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    # deploy_contract() will call compile_source_files() if the contract is not yet compiled.
    contract_interface.compile_source_files()
    contract_artifacts = contract_interface.deploy_contract()

    # remark: Get Contract Artifacts for the Proxy & GnosisSafe
    gnosis_instance = contract_interface.get_new_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_new_instance(contract_artifacts['Proxy'])

    # remark: Get Interface to interact with the contract
    gnosis_safe_module = GnosisSafeModule(provider, contract_artifacts)
    contract_instance = gnosis_safe_module.setup(gnosis_instance, proxy_instance)

    # remark: hardcoded private keys for ganache provider
    private_key_account0 = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
    private_key_account1 = '0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1'
    private_key_account2 = '0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c'
    # remark: get Account instances from every private key
    users_to_sign = [Account.from_key(private_key_account0), Account.from_key(private_key_account1), Account.from_key(private_key_account2)]
    orderred_signers = sorted(users_to_sign, key=lambda v: v.address.lower())
    print(Account.from_key(private_key_account0).address)
    function_name = ''
    function_arguments = ''
    address_from = ''
    execute_flag = False
    queue_flag = False
    contract_methods = map_contract_methods(contract_instance)
    # for index in contract_methods:
    #     print(contract_methods[index])

    # Todo: Automatically load Account Assets if you are in a Ganache enviroment
    # Todo loadAccount PK: {ganAccount0, ganAccount1, ganAccount2}, {randAccount0, randAccount1, randAccount2}, {rinkAccount0, rinkAccount1, rinkAccount2}
    # Todo loadContract BUILD_PATH
    # Todo connectContract address, ABI
    #

    query_is_owner = 'isOwner --address=0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 --query'
    execute_swap_owner = 'swapOwner --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002 --from=0x00000000000000000000000000000003 --execute'
    query_get_owners = 'getOwners --query'
    query_execTransaction_not_enough_args = 'execTransaction --queue --address=0x00000000000000000000000000000000 --address=0x00000000000000000000000000000001 --address=0x00000000000000000000000000000002'

    # remark: Operate with the current Contract
    operate_with_contract(query_get_owners, contract_methods, contract_instance)


if __name__ == '__main__':
    main()
