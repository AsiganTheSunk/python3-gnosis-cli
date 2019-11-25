#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from core.utils.contract.contract_contract_lexer import ContractLexer
from core.utils.contract.contract_function_completer import ContractFunctionCompleter
from core.utils.contract.contract_console_data import ContractConsoleArtifacts

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
import os
# Import Console Flags
from core.utils.gnosis_console_session_accounts import ConsoleSessionAccounts

# style = Style.from_dict({
#     'completion-menu.completion': 'bg:#008888 #ffffff',
#     'completion-menu.completion.current': 'bg:#00aaaa #000000',
#     'scrollbar.background': 'bg:#88aaaa',
#     'scrollbar.button': 'bg:#222222',
# })


# todo: move to the proper class all methods
QUOTE = '\''
COMA = ','
PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'


class GnosisConsoleEngine:
    def __init__(self, contract_artifacts):
        self.name = self.__class__.__name__
        self.console_session = PromptSession()
        self.contract_console_session = []
        self.console_accounts = ConsoleSessionAccounts()
        self.previous_session = None
        # Get the Contract Info
        self.prompt_text = 'GNOSIS-CLI v0.0.1'
        self.contract_artifacts = contract_artifacts

        # remark: Pre-Loading of the Contract Assets (Safe v1.1.0, Safe v1.0.0, Safe v-0.0.1)
        print('Pre-Loading of the Contract Assets (Safe v1.1.0, Safe v1.0.0, Safe v-0.0.1)')

        self.contract_console_data = ContractConsoleArtifacts()
        self.contract_console_data.add_artifact(contract_artifacts, alias='Gnosis-Safe-v1.1.0')

        for contract_artifacts_item in [contract_artifacts]:
            self.contract_console_data.add_artifact(contract_artifacts_item)

        # remark: Map the Artifacts of the Assets



        self.session_config = {
            'prompt': self._get_prompt_text(stream=self.prompt_text),
            'contract_lexer': ContractLexer(),
            'contract_completer': ContractFunctionCompleter(),
            'gnosis_lexer': None,
            'style': 'Empty',
            'completer': WordCompleter(
                ['about', 'info', 'help', 'newContract', 'loadContract', 'setNetwork', 'getNetwork', 'close', 'quit', 'viewContracts', 'viewAccounts'],
                ignore_case=True)
        }

    def get_console_session(self, prompt_text='', previous_session=None):
        if previous_session is None:
            return PromptSession(self.session_config['prompt'], completer=self.session_config['completer'], lexer=self.session_config['contract_lexer'])
        else:
            return PromptSession(prompt_text, completer=self.session_config['contract_completer'], lexer=self.session_config['contract_lexer'])

    def run_console_session(self, prompt_text='', previous_session=None, contract_methods=None, contract_instance=None):
        session = self.get_console_session(prompt_text, previous_session)
        try:
            while True:
                try:
                    # remark: Start the prompt
                    stream = session.prompt()
                    if previous_session is None:
                        # remark: eval gnosis-cli arguments
                        # note: this should be ported to argparse library, this is only a prototype
                        self._evaluate_gnosis_console_commands(stream, session)
                    else:
                        # remark: eval contract-cli arguments
                        # note: this should be ported to argparse library, this is only a prototype
                        self.operate_with_contract(stream, contract_methods, contract_instance)

                    # remark: If you are in a sub session of the console return to gnosis-cli session
                    if (stream == 'close') or (stream == 'quit') or (stream == 'exit'):
                        return self._close_console_session(previous_session)
                except KeyboardInterrupt:
                    continue  # Control-C pressed. Try again.
                except EOFError:
                    break  # Control-D pressed.
        except Exception as err:
            print('FATAL ERROR: ' + str(err))

    def _close_console_session(self, previous_session=None):
        """ Close Session
        This function will return the previous session otherwise it will exit the gnosis-cli
        :param previous_session:
        :return:
        """
        if previous_session is None:
            raise EOFError
        return previous_session

    def _get_gnosis_input_command_argument(self, command_argument, argument_list, checklist):
        """ Get Gnosis Input Command Arguments
        This function will get the input arguments provided in the gnosis-cli
        :param command_argument:
        :param argument_list:
        :param checklist:
        :return:
        """
        for sub_index, argument_item in enumerate(argument_list):
            print('item_argument', argument_item)
            if argument_item.startswith('--alias='):
                alias = self._get_method_argument_value(argument_item, quote=False)
                return alias
            elif argument_item.startswith('--name=') and argument_item in checklist:
                print(command_argument, argument_item)
            elif argument_item.startswith('--id=') and argument_item in checklist:
                print(command_argument, argument_item)
            elif argument_item.startswith('--abi=') and argument_item in checklist:
                print(command_argument, argument_item)
            elif argument_item.startswith('--address=') and argument_item in checklist:
                print(command_argument, argument_item)
            elif argument_item.startswith('--bytecode=') and argument_item in checklist:
                print(command_argument, argument_item)
            else:
                print(command_argument, argument_item)

    def _evaluate_gnosis_console_commands(self, stream, previous_session=None):
        print('gnosis_console_stream_input:', stream)
        argument_list = []
        command_argument = ''
        try:
            split_input = stream.split(' ')
            print(split_input)
            command_argument = split_input[0]
            print('command', command_argument)
            argument_list = split_input[1:]
            print('arguments', argument_list)
        except Exception as err:
            print(type(err), err)

        if command_argument.startswith('loadContract'):

                # tmp_alias, tmp_abi, tmp_bytecode, tmp_address =
                tmp_alias = self._get_gnosis_input_command_argument(command_argument, argument_list, ['--alias=', '--abi=', '--bytecode=', '--address='])
                try:
                    contract_instance = self.contract_console_data.get_key_from_alias(tmp_alias, 'instance')
                    contract_methods = self.map_contract_methods(contract_instance)
                    self.run_console_session(prompt_text=self._get_prompt_text(affix_stream='./', stream=tmp_alias),
                                             previous_session=previous_session, contract_methods=contract_methods,
                                             contract_instance=contract_instance)
                except KeyError as err:
                    print(type(err), err)

        elif stream.startswith('viewContracts'):
            print(' alias                        address')
            for item in self.contract_console_data.contract_data:
                print(item, self.contract_console_data.contract_data[item]['address'], self.contract_console_data.contract_data[item]['instance'])
        elif stream.startswith('viewAccounts'):

            for item in self.console_accounts.account_data:
                print(item, self.console_accounts.account_data[item]['address'], self.console_accounts.account_data[item]['private_key'])
        elif stream.startswith('about'):
            print('here_about')
        elif (stream == 'info') or (stream == 'help'):
            print('info/help')
        elif stream == 'loadOwner':
            # Add Ethereum money conversion for all types of coins
            print('newAccount <Address> or <PK> or <PK + Address>')

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
            return contract_methods
        except Exception as err:
            print(err)

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

    def _get_quoted_argument(self, value):
        """ Quote Argument

        :param value:
        :return:
        """
        return QUOTE + value + QUOTE

    def _get_prompt_text(self, affix_stream='', stream=''):
        """ Get Prompt Text

        :param contract_name:
        :return:
        """
        if affix_stream == '':
            return '[ {cli_name} ]>: '.format(cli_name=self.prompt_text)
        return '[ {affix_stream} ][ {stream} ]>: '.format(affix_stream=affix_stream, stream=stream)

    def _get_method_argument_value(self, value, quote=True):
        """ Get Method Argument Value

        :param value:
        :return:
        """
        if quote:
            return self._get_quoted_argument(value.split('=')[1])
        return value.split('=')[1]