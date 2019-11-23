#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from pygments.lexers.sql import SqlLexer

from core.console_utils.contract_lexer import ContractLexer
from core.console_utils.contract_function_completer import ContractFunctionCompleter

# Import PromptToolkit Package
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
import re
# Import Provider Packages

# Import Sys Package
import sys
from prompt_toolkit.validation import Validator
# Importing Custom Logger & Logging Modules
# from core.logger.custom_logger import CustomLogger
# from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
# from logging import INFO, DEBUG, WARNING
# import logging

# Import Console Flags
from core.constants.default_values import ConsoleSessionTypeFlag as console_flags

gnosis_safe_completer = WordCompleter([
    'safe_addr', 'add', 'after', 'all', 'before', 'check', 'current_date',
    'current_time', 'current_timestamp', 'default',
    'delete', 'exit', 'quit', 'without'], ignore_case=True)

cli_sesion_completer = WordCompleter([
    'load', 'about', 'info', 'help', 'loadOwner'], ignore_case=True)


style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


class GnosisConsoleInput:
    def __init__(self):
        self.name = self.__class__.__name__
        self.main_console_session = PromptSession()
        self.contract_console_session = None
        self.cli_prompt = self.__get_prompt_text()

    @staticmethod
    def __get_prompt_text(contract_name=''):
        return f'(gnosis-safe-cli){contract_name}>: '

    def __close_session(self, previous_session=None):
        if previous_session is None:
            raise EOFError
        return previous_session

    def run_console_session(self, prompt_text='', session_completer=cli_sesion_completer, previous_session=None, lexer=ContractLexer()):
        if previous_session is None:
            session = PromptSession(self.__get_prompt_text(), completer=cli_sesion_completer, lexer=ContractLexer(), style=style)
        else:
            session = PromptSession(prompt_text, completer=session_completer, style=style, lexer=lexer)
        try:
            while True:
                try:
                    input_value = session.prompt()
                    if input_value == 'load':
                        self.run_console_session(prompt_text=self.__get_prompt_text('[ Gnosis-Safe(v1.1.0) ]'), previous_session=session, session_completer=ContractFunctionCompleter(), lexer=lexer)
                    elif (input_value == 'close') or (input_value == 'quit') or (input_value == 'exit'):
                        return self.__close_session(previous_session)
                    elif input_value == 'about':
                        print('here_about')
                    elif (input_value == 'info') or (input_value == 'help'):
                        print('info/help')
                    elif input_value == 'loadOwner':
                        # Add Ethereum money conversion for all types of coins
                        print('loadOwner <Address> or <PK> or <PK + Address>')
                except KeyboardInterrupt:
                    continue  # Control-C pressed. Try again.
                except EOFError:
                    break  # Control-D pressed.
        except Exception as err:
            print('FATAL ERROR: ' + str(err))


# text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=True)
# text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=False)
# try:
#     for item in contract_methods:
#         if contract_methods[item]['function_name'] in text:
#             current_function_call = contract_methods[item]['function_call']
#             print('Contract Call to: %s' % current_function_call)
#             # remark: ReadFunctionMap
#             # Todo: remove this piece of not so very good just so really bad code, this is only to showcase early functionallity
#             splitted_input = len(text.split(' '))
#             if splitted_input == 1:
#                 print(eval(current_function_call)())
#             else:
#                 for data in contract_methods[item]['function_input']:
#                     try:
#                         function_schema = contract_methods[item]['function_call_clean']
#                         # Todo: base de eval process in a list of input validations, based on the function_input stored in the current_dict for contract interface
#
#                         params = '\'' + eval_function_old(text) + '\''
#                         current_function = function_schema.format(contract_methods[item]['function_name'], params)
#                         print(function_schema.format(contract_methods[item]['function_name'], params))
#                         print(eval(current_function)())
#                     except Exception as err:
#                         print(err)
# except Exception as err:  # KeyError
#     print(err)
#     continue
