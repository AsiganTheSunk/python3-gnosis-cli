#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from core.utils.contract.contract_lexer import ContractLexer
from core.utils.contract.contract_function_completer import ContractFunctionCompleter

# Import PromptToolkit Package
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

# Import Provider Packages

# Import Sys Package
# Importing Custom Logger & Logging Modules
# from core.logger.custom_logger import CustomLogger
# from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
# from logging import INFO, DEBUG, WARNING
# import logging

# Import Console Flags

gnosis_safe_completer = WordCompleter([
    'safe_addr', 'add', 'after', 'all', 'before', 'check', 'current_date',
    'current_time', 'current_timestamp', 'default',
    'delete', 'exit', 'quit', 'without'], ignore_case=True)

cli_sesion_completer = WordCompleter([
    'load', 'about', 'info', 'help', 'newContract', 'loadContract'
], ignore_case=True)


style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})

import os

# todo: move to the proper class all methods
QUOTE = '\''
COMA = ','
PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'

# def to_32byte_hex(val):
#     return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


class ChildGnosisConsole:
    def __init__(self, affix_stream, contract_instance, lexer, completer, previous_session):
        self.affix_stream = affix_stream
        self.contract_instance = contract_instance
        self.lexer = lexer
        self.completer = completer
        self.previous_session = previous_session

    def _get_prompt_text(self, stream=''):
        """ Get Prompt Text

        :param contract_name:
        :return:
        """
        return f'(gnosis-cli)\n\t[ ./{self.affix_stream} ][ {stream} ]>: '

    @staticmethod
    def _close_session(previous_session=None):
        """ Close Session

        :param previous_session:
        :return:
        """
        return previous_session


from core.utils.gnosis_console_session_accounts import ConsoleSessionAccounts

class GnosisConsole:
    def __init__(self, contract_artifacts):
        self.name = self.__class__.__name__
        self.console_session = PromptSession()
        self.contract_console_session = []
        self.console_accounts = ConsoleSessionAccounts()
        self.contract_artifacts = contract_artifacts
        # Get the Contract Info
        # Todo: this should be moved to SubGnosisConsole
        #print('--loading artifacts', self.contract_artifacts['instance'])
        self.contract_methods = self.map_contract_methods(self.contract_artifacts['instance'])
        self.contract_instante = self.contract_artifacts['instance']

    @staticmethod
    def _get_prompt_text(contract_name=''):
        """ Get Prompt Text

        :param contract_name:
        :return:
        """
        return f'(gnosis-safe-cli){contract_name}>: '

    @staticmethod
    def _close_session(previous_session=None):
        """ Close Session

        :param previous_session:
        :return:
        """
        if previous_session is None:
            raise EOFError
        return previous_session

    def _evaluate_gnosis_console_commands(self, stream, session, session_completer=cli_sesion_completer, previous_session=None, lexer=ContractLexer()):
        print('gnosis_console_stream_input:', stream)
        # loadContract --alias=GnosisSafe-v1.1.0 // loadContract 0

        if stream.startswith('loadContract'):
            load_data = stream.slipt(' ')

            self.run_console_session(prompt_text=self._get_prompt_text('\n[ ./ ][ Gnosis-Safe(v1.1.0) ]'), previous_session=session, session_completer=session_completer, lexer=lexer)
        elif stream.startswith('about'):
            print('here_about')
        elif (stream == 'info') or (stream == 'help'):
            print('info/help')
        elif stream == 'loadOwner':
            # Add Ethereum money conversion for all types of coins
            print('loadOwner <Address> or <PK> or <PK + Address>')

    def map_contract_methods(self, contract_instance):
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
            # Retrieve methods presents in the provided abi file
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
                    # <>

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

    def _quote_argument(self, value):
        """ Quote Argument

        :param value:
        :return:
        """
        return QUOTE + value + QUOTE

    def _get_method_argument_value(self, value):
        """ Get Method Argument Value

        :param value:
        :return:
        """
        return self._quote_argument(value.split('=')[1])


    def _get_input_method_arguments(self, argument_list, function_arguments):
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

        for sub_index, argument_item in enumerate(argument_list):
            if '--from=' in argument_item:
                address_from = self._get_method_argument_value(argument_item)
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
                for sub_index, argument_type in enumerate(function_arguments):
                    if argument_type[sub_index] in argument_item \
                            and argument_positions_to_fill != 0 \
                            and argument_positions_to_fill > argument_positions_filled:
                        arguments_to_fill += self._get_method_argument_value(argument_item) + COMA
                        argument_positions_filled += 1

                arguments_to_fill = arguments_to_fill[:-1]

        return argument_list[0], arguments_to_fill, address_from, execute_value, to_queue, to_query

    # todo: move to the proper class all methods
    QUOTE = '\''
    COMA = ','
    PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'

    # todo:
    def operate_with_contract(self, stream, contract_methods, contract_instance):
        """ Operate With Contract
        This function will retrieve the methods present & in the contract_instance
        :param stream:
        :param contract_methods:
        :param contract_instance:
        :return:
        """
        try:
            print('operate_with_contract:', stream)
            for item in contract_methods:
                if contract_methods[item]['name'] in stream:
                    splitted_stream = stream.split(' ')
                    function_name, function_arguments, address_from, execute_flag, queue_flag, query_flag = self._get_input_method_arguments(
                        splitted_stream, contract_methods[item]['arguments'])
                    print(self._get_input_method_arguments(splitted_stream, contract_methods[item]['arguments']))

                    if execute_flag or query_flag or queue_flag:
                        if execute_flag:
                            if contract_methods[item]['name'].startswith('get'):
                                print('WARNING: transact() operation is discourage and might not work if you are calling a get function')
                            print(contract_methods[item]['transact'].format(function_arguments, address_from))
                        elif query_flag:
                            print(contract_methods[item]['call'].format(function_arguments, address_from))
                            print(eval(contract_methods[item]['call'].format(function_arguments, address_from)))
                        elif queue_flag:
                            print(contract_methods[item]['call'].format(function_arguments, address_from))
                            print('INFO: executeBatch when you are ready to launch the transactions that you queued up!')
                    else:
                        print('WARNING: --execute, --query or --queue flag needed!')
        except Exception as err:  # KeyError
            print(err)

    def run_console_session(self, prompt_text='', session_completer=cli_sesion_completer, previous_session=None, lexer=ContractLexer()):
        """ Run Console Session

        :param prompt_text:
        :param session_completer:
        :param previous_session:
        :param lexer:
        :return:
        """
        if previous_session is None:
            session = PromptSession(self._get_prompt_text(), completer=cli_sesion_completer, lexer=ContractLexer(), style=style)
        else:
            session = PromptSession(prompt_text, completer=ContractFunctionCompleter(), style=style, lexer=lexer)
        try:
            while True:
                try:
                    stream = session.prompt()
                    self._evaluate_gnosis_console_commands(stream, session, previous_session=session, session_completer=session_completer, lexer=lexer)
                    self.operate_with_contract(stream, self.contract_methods, self.contract_instante)
                    if (stream == 'close') or (stream == 'quit') or (stream == 'exit'):
                        return self._close_session(previous_session)
                except KeyboardInterrupt:
                    continue  # Control-C pressed. Try again.
                except EOFError:
                    break  # Control-D pressed.
        except Exception as err:
            print('FATAL ERROR: ' + str(err))
