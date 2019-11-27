#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from core.console_session_accounts import ConsoleSessionAccounts
from core.utils.contract.contract_console_lexer import ContractLexer
from core.utils.contract.contract_console_function_completer import ContractFunctionCompleter
from core.utils.contract.contract_console_artifacts import ContractConsoleArtifacts
from core.utils.contract.contract_console_payloads import ContractConsolePayloads

# Import PromptToolkit Package
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit import HTML, prompt

# Import Os Package
import os

# style = Style.from_dict({
#     'completion-menu.completion': 'bg:#008888 #ffffff',
#     'completion-menu.completion.current': 'bg:#00aaaa #000000',
#     'scrollbar.background': 'bg:#88aaaa',
#     'scrollbar.button': 'bg:#222222',
# })

# todo: move to constants class
QUOTE = '\''
COMA = ','
PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'
payload_options = ['alias', 'from', 'gas', 'gasPrice']
payload_tx_options = ['alias', 'from', 'gas', 'gasPrice', 'value', 'nonce', 'safe_tx_gas']

class GnosisConsoleEngine:
    def __init__(self):
        self.name = self.__class__.__name__
        self.console_session = PromptSession()
        self.contract_console_session = []
        self.console_accounts = ConsoleSessionAccounts()
        self.previous_session = None
        self.prompt_text = 'GNOSIS-CLI v0.0.1a'
        self.contract_artifacts = None
        self.network = 'ganache'
        self.contract_console_data = ContractConsoleArtifacts()
        self.console_payloads = ContractConsolePayloads()
        self.default_auto_fill = False
        self.default_owner = ''
        self.default_owner_list = []

        self.session_config = {
            'prompt': self._get_prompt_text(stream=self.prompt_text),
            'contract_lexer': ContractLexer(),
            'contract_completer': ContractFunctionCompleter(),
            'gnosis_lexer': None,
            'style': 'Empty',
            'completer': WordCompleter(
                [
                    'about', 'info', 'help', 'newContract', 'loadContract', 'setNetwork', 'viewNetwork',
                    'close', 'quit', 'viewContracts', 'viewAccounts', 'newAccount', 'setAutofill',
                    'viewPayloads', 'newPayload', 'newTxPayload', 'setDefaultOwner', 'setDefaultOwnerList',
                    'viewOwner', 'viewOwnerList', 'dummyCommand'
                 ],
                ignore_case=True)
        }

    def run_console_session(self, prompt_text='', previous_session=None, contract_methods=None, contract_instance=None):
        """ Run Console Session

        :param prompt_text:
        :param previous_session:
        :param contract_methods:
        :param contract_instance:
        :return:
        """
        session = self.get_console_session(prompt_text, previous_session)
        try:
            while True:
                try:
                    # remark: Start the prompt
                    stream = session.prompt()
                    if previous_session is None:
                        # remark: eval gnosis-cli arguments
                        self._evaluate_console_command(stream, session)
                    else:
                        # remark: eval contract-cli arguments
                        self.operate_with_contract(stream, contract_methods, contract_instance)
                    # remark: If you are in a sub session of the console return to gnosis-cli session
                    command_argument, argument_list = self._get_input_console_arguments(stream)
                    if (command_argument == 'close') or (command_argument == 'quit') or (command_argument == 'exit'):
                        return self._close_console_session(previous_session)
                except KeyboardInterrupt:
                    continue  # remark: Control-C pressed. Try again.
                except EOFError:
                    break  # remark: Control-D pressed.
        except Exception as err:
            print('FATAL:', type(err), err)

    def get_console_session(self, prompt_text='', previous_session=None):
        """ Get Console Session

        :param prompt_text:
        :param previous_session:
        :return:
        """
        if previous_session is None:
            return PromptSession(self.session_config['prompt'], completer=self.session_config['completer'], lexer=self.session_config['contract_lexer'])
        else:
            return PromptSession(prompt_text, completer=self.session_config['contract_completer'], lexer=self.session_config['contract_lexer'])

    def _close_console_session(self, previous_session=None):
        """ Close Console Session
        This function will return the previous session otherwise it will exit the gnosis-cli
        :param previous_session:
        :return:
        """
        if previous_session is None:
            raise EOFError
        return previous_session

    def load_contract_artifacts(self, contract_artifacts):
        """ Load Contract Artifacts

        :param contract_artifacts:
        :return:
        """
        self.contract_artifacts = contract_artifacts
        # remark: Pre-Loading of the Contract Assets (Safe v1.1.0, Safe v1.0.0, Safe v-0.0.1)
        print('Pre-Loading of the Contract Assets Here')
        # remark: Map the Artifacts of the Assets
        # note: method 1, with alias
        self.contract_console_data.add_artifact(contract_artifacts, alias='Gnosis-Safe-v1.1.0')
        # note: method 2, wihout alias
        for contract_artifacts_item in [contract_artifacts]:
            self.contract_console_data.add_artifact(contract_artifacts_item)

    def command_set_network(self, value):
        """ Command Set Network
        This function will perform the setNetwork functionality in the gnosis-cli
        :param value:
        :return:
        """
        self.network = value

    def command_set_default_owner(self, value):
        self.default_owner = value

    def command_set_default_owner_list(self, value):
        self.default_owner_list = value

    def command_view_default_owner_list(self):
        print('Default Owner List', self.default_owner_list)

    def command_view_default_owner(self):
        print('Default Owner:', self.default_owner)

    def _new_payload_helper(self, payload_options):
        alias = ''
        compose_answer = '{'
        for item in payload_options:
            text = ('\'%s\' : ' % (item)).rjust(20)
            answer = prompt(HTML(' <strong>%s</strong> ') % text)
            if answer == '':
                if (item == 'gas') or (item == 'gasPrice') or (item == 'nonce') or (item == 'safe_tx_gas'):
                    compose_answer += '\'%s\' : %s' % (item, str(0)) + ', '
                elif item == 'alias':
                    continue
                else:
                    # todo: here check if setDefaultOwner is active, if it's empty, fill the current defaultOwner
                    #  same goes if you put defaultOwner this should be transcribed to the proper address
                    compose_answer += '\'%s\' : \'%s\'' % (item, '') + ', '
            else:
                if item == 'alias':
                    alias = answer
                else:
                    compose_answer += '\'%s\' : %s' % (item, answer) + ', '

        return alias, compose_answer[:-2] + '}'

    def command_new_payload(self, command_argument, argument_list):
        """ Command New Payload

        :param command_argument:
        :param argument_list:
        :return:
        """
        if command_argument == 'newPayload' and argument_list == []:
            alias, composed_payload = self._new_payload_helper(payload_options)
            print('newPayload:', alias, composed_payload)
            return self.console_payloads.add_payload(composed_payload, alias)

        elif command_argument == 'newTxPayload' and argument_list == []:
            alias, composed_payload = self._new_payload_helper(payload_tx_options)
            print('newTxPayload:', alias, composed_payload)
            return self.console_payloads.add_payload(composed_payload, alias)
        else:
            print('input for argument --nonce=, --gas=, --gasPrice=, --value=')


    def command_view_network(self):
        print('Current_Network:', self.network)

    def command_view_payloads(self):
        for item in self.console_payloads.payload_data:
            print(item, self.console_payloads.payload_data[item])

    def command_view_accounts(self):
        for item in self.console_accounts.account_data:
            print(item, self.console_accounts.account_data[item]['address'],
                  self.console_accounts.account_data[item]['private_key'])

    def command_view_contracts(self):
        for item in self.contract_console_data.contract_data:
            print(item, self.contract_console_data.contract_data[item]['address'],
                  self.contract_console_data.contract_data[item]['instance'])

    def command_view_about(self):
        print('Prototype for Gnosis Console')
        print('Version: 0.0.1a')

    def command_view_help(self):
        print('---------' * 10)
        print('Console Command List')
        print('---------' * 10)
        print(' (+) loadContract: --alias= ')
        print('---------' * 10)
        print(' (+) setNetwork: command to set current network')
        print(' (+) setAutofill: Command to set auto fill option')
        print(' (+) setDefaultOwner: Command to set default owner')
        print(' (+) setDefaultOwnerList: Command to set default owner list')
        print('---------' * 10)
        print(' (+) viewNetwork: Command to get current and available network')
        print(' (+) viewAccounts: Command to get available Accounts')
        print(' (+) viewContracts: Command to get available Contracts')
        print(' (+) viewOwnerList: Command to get default owner list')
        print(' (+) viewOwner: Command to get default owner')
        print(' (+) viewPayloads: Command to get available Payloads')
        print('---------' * 10)
        print(' (+) newContract: --address= --abi= | --abi= --bytecode=')
        print(' (+) newAccount: --alias= --address= --private_key=')
        print(' (+) newPayload: Command to create a new payload to be stored, used in call() & transact()')
        print(' (+) newTxPayload: Command to create a new tx payload to be stored')
        print(' (+) quit|close|exit: Command to exit gnosis-cli & contract-cli')

    # note: Future command to it's own funciton
    def command_load_contract(self, command_argument, argument_list, previous_session):
        """ Command Load Contract

        :param command_argument:
        :param argument_list:
        :param previous_session:
        :return:
        """
        tmp_alias = self._get_gnosis_input_command_argument(command_argument, argument_list,
                                                            ['--alias=', '--abi=', '--bytecode=', '--address='])
        try:
            contract_instance = self.contract_console_data.get_value_from_alias(tmp_alias, 'instance')
            contract_methods = self.map_contract_methods(contract_instance)
            self.run_console_session(prompt_text=self._get_prompt_text(affix_stream='./', stream=tmp_alias),
                                     previous_session=previous_session, contract_methods=contract_methods,
                                     contract_instance=contract_instance)
        except KeyError as err:
            print(type(err), err)

    def _eval_stored_arguments(self, argument_item, storage_item):
        try:
            stored_index = argument_item.split('.')
            print('stored_argument', stored_index[0], stored_index[1])
            try:
                tmp_address = storage_item[stored_index[0]][stored_index[1]]
                return tmp_address
            except KeyError as err:
                print('Key Error here', err)
        except Exception:
            return '*'

    def _get_gnosis_input_command_argument(self, command_argument, argument_list, checklist):
        """ Get Gnosis Input Command Arguments
        This function will get the input arguments provided in the gnosis-cli
        :param command_argument:
        :param argument_list:
        :param checklist:
        :return:
        """
        print('Command:', command_argument)
        for sub_index, argument_item in enumerate(argument_list):
            if argument_item.startswith('--alias='):
                alias = self._get_method_argument_value(argument_item, quote=False)
                return alias
            elif argument_item.startswith('--name='):
                name = self._get_method_argument_value(argument_item, quote=False)
                return name
            elif argument_item.startswith('--id='):
                id = self._get_method_argument_value(argument_item, quote=False)
            elif argument_item.startswith('--abi='):
                contract_abi = self._get_method_argument_value(argument_item, quote=False)
            elif argument_item.startswith('--address='):
                tmp_address = self._get_method_argument_value(argument_item, quote=False)
                aux_tmp_address = self._eval_stored_arguments(tmp_address, self.console_accounts.account_data)
                # aux2_tmp_address = self._eval_stored_arguments(tmp_address, self.contract_console_data.contract_data)
                print(aux_tmp_address)
            elif argument_item.startswith('--bytecode='):
                contract_bytecode = self._get_method_argument_value(argument_item, quote=False)
            else:
                continue
            print(' (+) Argument:', argument_item)

    def _get_input_console_arguments(self, stream):
        argument_list = []
        command_argument = ''
        try:
            split_input = stream.split(' ')
            command_argument = split_input[0]
            argument_list = split_input[1:]
            return command_argument, argument_list
        except Exception as err:
            print('get_input_console_arguments', type(err), err)
            return command_argument, argument_list

    def _evaluate_console_command(self, stream, previous_session):
        command_argument, argument_list = self._get_input_console_arguments(stream)
        print('Commnand:', command_argument, 'Arguments:', argument_list)
        if command_argument == 'loadContract':
            self.command_load_contract(command_argument, argument_list, previous_session)
        elif command_argument == 'setNetwork':
            self.command_set_network(self._get_gnosis_input_command_argument(command_argument, argument_list, ['--name=']))
        elif command_argument == 'viewNetwork':
            self.command_view_network()
        elif command_argument == 'viewContracts':
            self.command_view_contracts()
        elif command_argument == 'viewAccounts':
            self.command_view_accounts()
        elif command_argument == 'viewPayloads':
            self.command_view_payloads()
        elif command_argument == 'about':
            self.command_view_about()
        elif (command_argument == 'info') or (command_argument == 'help'):
            self.command_view_help()
        elif command_argument == 'newAccount':
            # Add Ethereum money conversion for all types of coins
            print('newAccount <Address> or <PK> or <PK + Address>')
        elif command_argument == 'newPayload':
            self.command_new_payload(command_argument, argument_list)
        elif command_argument == 'newTxPayload':
            self.command_new_payload(command_argument, argument_list)
        elif command_argument == 'setDefaultOwner':
            self.command_set_default_owner(argument_list)
        elif command_argument == 'setDefaultOwnerList':
            self.command_set_default_owner_list(argument_list)
        elif command_argument == 'setAutofill':
            print('Autofill Function')
        elif command_argument == 'viewOwner':
            self.command_view_default_owner()
        elif command_argument == 'viewOwners':
            self.command_view_default_owner_list()
        elif command_argument == 'dummyCommand':
            self._get_gnosis_input_command_argument(command_argument, argument_list, [])

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

        # Control for number of input arguments
        argument_positions_to_fill = len(function_arguments)
        argument_positions_filled = 0

        for sub_index, argument_item in enumerate(argument_list):
            if '--from=' in argument_item:
                address_from = self._get_method_argument_value(argument_item)
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
        This function will retrieve the methods present in the contract_instance
        :param stream: command_argument (method to call) that will trigger the operation
        :param contract_methods: dict with all the avaliable methods retrieved from the abi file
        :param contract_instance: only for eval() so it can be triggered
        :return: if method found, a method from the current contract will be triggered, success or not depends on the establishing of the proper values.
        """
        try:
            print('Call operate_with_contract:', stream)
            for item in contract_methods:
                if contract_methods[item]['name'] in stream:
                    splitted_stream = stream.split(' ')
                    function_name, function_arguments, address_from, execute_flag, queue_flag, query_flag = self._get_input_method_arguments(
                        splitted_stream, contract_methods[item]['arguments'])
                    print('command:', function_name, 'arguments', function_arguments, 'tx:', execute_flag, 'call:', query_flag)
                    # print(self._get_input_method_arguments(splitted_stream, contract_methods[item]['arguments']))

                    if execute_flag or query_flag or queue_flag:

                        # remark: Transaction Solver
                        if execute_flag:
                            if contract_methods[item]['name'].startswith('get'):
                                print('WARNING: transact() operation is discourage and might not work if you are calling a get function')
                            # if address_from != '':
                                # address_from = '\{\'from\':{0}\}'.format(address_from)

                            print(contract_methods[item]['transact'].format(function_arguments, address_from))
                            print(eval(contract_methods[item]['transact'].format(function_arguments, address_from)))

                        # remark: Call Solver
                        elif query_flag:
                            print(contract_methods[item]['call'].format(function_arguments, address_from))
                            print(eval(contract_methods[item]['call'].format(function_arguments, address_from)))

                        # remark: Add to the Batch Solver
                        elif queue_flag:
                            print(contract_methods[item]['call'].format(function_arguments, address_from))
                            print('INFO: executeBatch when you are ready to launch the transactions that you queued up!')
                    else:
                        print('WARNING: --execute, --query or --queue flag needed!')
        except Exception as err:
            print(type(err), err)

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