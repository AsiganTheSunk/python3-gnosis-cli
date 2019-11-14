#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Pygments Package
from pygments.lexers.sql import SqlLexer

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


def eval_function(value, function_name=''):
    print(function_name)
    print('current_value:', value[len(function_name):])
    try:
        print(value)
        if len(value[1][2:]) != 40:
            print('launch error, address must be 40 alfanumeric hash')
        else:
            print('evaluando re')
            re.search('0x[0-9,aA-zZ]{42}', value).group(0)
    except Exception as err: # IndexError:
        print(err)
        print('there is not enough data to verify current input')
        pass

def eval_function_old(value='isOwner 0xe982E462b094850F12AF94d21D470e21bE9D0E9C'):

    try:
        splitted_input = value.split(' ')
    except TypeError:
        pass
    else:
        try:
            print(splitted_input)
            if len(splitted_input[1][2:]) != 40:
                print('launch error, address must be 40 alfanumeric hash')
            else:
                re.search('0x[0-9,aA-zZ]{40}', splitted_input[1]).group(0)
        except IndexError:
            print('there is not enough data to verify current input')
            pass
        return splitted_input[1]

def is_valid_address(text):
    return '0x' in text


validator = Validator.from_callable(
    is_valid_address, error_message='Not a valid address (Does not contain an 0x).', move_cursor_to_end=True
)

# Code Reference: https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/examples/prompts

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
                        if contract_interface[item]['function_name'] in text:
                            current_function_call = contract_interface[item]['function_call']
                            print('Contract Call to: %s' % current_function_call)

                            # Todo: remove this piece of not so very good just so really bad code, this is only to showcase early functionallity
                            splitted_input = len(text.split(' '))
                            if splitted_input == 1:
                                print(eval(current_function_call)())
                            else:
                                for data in contract_interface[item]['function_input']:
                                    try:
                                        function_schema = contract_interface[item]['function_call_clean']
                                        # Todo: base de eval process in a list of input validations, based on the function_input stored in the current_dict for contract interface

                                        params = '\'' + eval_function_old(text) + '\''
                                        current_function = function_schema.format(contract_interface[item]['function_name'], params)
                                        print(function_schema.format(contract_interface[item]['function_name'], params))
                                        print(eval(current_function)())
                                    except Exception as err:
                                        print(err)

                            #print(eval(current_function_call)())


                except Exception as err: # KeyError
                    print(err)
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
