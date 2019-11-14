#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from pygments.lexers.sql import SqlLexer

# Import PromptToolkit Package
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

# Import Provider Packages

# Import Sys Package
import sys
from prompt_toolkit.validation import Validator
# Importing Custom Logger & Logging Modules
# from core.logger.custom_logger import CustomLogger
# from core.logger.constants.custom_verbose_levels import VERBOSE, FATAL
# from logging import INFO, DEBUG, WARNING
# import logging

gnosis_safe_cli_completer = WordCompleter([
    'safe_addr', 'add', 'after', 'all', 'before', 'check', 'current_date',
    'current_time', 'current_timestamp', 'default',
    'delete', 'without'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


def is_valid_address(text):
    return '0x' in text


validator = Validator.from_callable(
    is_valid_address, error_message='Not a valid address (Does not contain an 0x).', move_cursor_to_end=True
)

class GnosisConsoleInput:
    def run(self, session_completer=gnosis_safe_cli_completer, contract_interface=None, current_contract=None):
        session = PromptSession(completer=session_completer, style=style)
        while True:
            try:
                current_function_call = ''
                #text = session.prompt('(gnosis-safe-cli)> ')
                # Validate when pressing ENTER.
                #text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=False)
                #print('You said: %s' % text)

                # While typing
                #text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=True)
                #text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=False)
                text = session.prompt('(gnosis-safe-cli)> ')
                try:
                    for item in contract_interface:
                        if text == contract_interface[item]['function_name']:
                            current_function_call = contract_interface[item]['function_call']
                            print('Contract Call to: %s' % current_function_call)
                            print(eval(current_function_call)())
                except KeyError:
                    continue

            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

        # with connection:
        #     try:
        #         messages = connection.execute(text)
        #     except Exception as e:
        #         print(repr(e))
        #     else:
        #         for message in messages:
        #             print(message)

        print('GoodBye!')
