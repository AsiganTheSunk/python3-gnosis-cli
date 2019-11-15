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
    'delete','exit', 'quit', 'without'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


def eval_function_old(param, param_type):
    """ Eval Function (Deprecated)

    isOwner 0xe982E462b094850F12AF94d21D470e21bE9D0E9C
    :param param:
    :param param_type:
    :return:
    """
    try:
        splitted_input = param.split(' ')
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


def validate_byte_byte32_input(param, param_type):
    """"""
    # bytes32
    return


def string_to_byte(data):
    """ String To Byte (Hex)

    :param data:
    :return:
    """
    if len(data) > 8:
        byte8 = data[:8]
    else:
        byte8 = data.ljust(8, '0')
    return bytes(byte8, 'utf-8')


def string_to_bytes32(data):
    """ String To Bytes32 (Hex)

    :param data:
    :return:
    """
    if len(data) > 32:
        bytes32 = data[:32]
    else:
        bytes32 = data.ljust(32, '0')
    return bytes(bytes32, 'utf-8')


def validate_address_input(param):
    """ Validate Address Input

    :param param:
    :return:
    """
    try:
        if '0x' in param:
            if len(param[1][2:]) != 40:
                re.search('0x[0-9,aA-zZ]{40}', param).group(0)
                return True, ''
            return False, 'Not a valid address (Does not have 40 alphanumeric values).'
        return False, 'Not a valid address (Does not start with 0x).'
    except Exception as err:
        print(err)
        return False, 'Not a valid address (Unable to parse param).'


def validate_integer_input(param, param_type):
    """ Validate Integer Input

    :param param:
    :param param_type:
    :return:
    """
    # use hex()
    # address payable 160
    # address 256
    if param_type == 'uint8' and param <= 255:
        return True, ''
    elif param_type == 'uint16' and param <= 65535:
        return True, ''
    elif param_type == 'uint32' and param <= 4294967295:
        return True, ''
    elif param_type == 'uint64'and param <= 18446744073709551615:
        return True, ''
    elif param_type == 'uint128'and param <= 340282366920938463463374607431768211455:
        return True, ''
    elif param_type == 'uint160'and param <= 1461501637330902918203684832716283019655932542975:
        return True, ''
    elif param_type == 'uint256'and param <= 115792089237316195423570985008687907853269984665640564039457584007913129639935:
        return True, ''
    return False, 'Not a valid {0} (Does not fit the current type for the function input)'.format(param_type)


def is_valid_address(text):
    return '0x' in text


validator = Validator.from_callable(
    is_valid_address, error_message='Not a valid address (Does not contain an 0x).', move_cursor_to_end=True
)


# Code Reference: https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/examples/prompts
# todo: Remove crappy code from the current class GnosisConosleInput
class GnosisConsoleInput:
    def run(self, session_completer=gnosis_safe_cli_completer, contract_interface=None, current_contract=None):
        """ Gnosis Console Input

        :param session_completer:
        :param contract_interface:
        :param current_contract:
        :return:
        """
        session = PromptSession(completer=session_completer, style=style)
        while True:
            try:
                # text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=True)
                # text = session.prompt('(gnosis-safe-cli)> ', validator=validator, validate_while_typing=False)

                current_function_call = ''
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
                except Exception as err:  # KeyError
                    print(err)
                    continue

                if text == 'exit':
                    raise EOFError
                elif text == 'quit':
                    raise EOFError
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.
        print('GoodBye!')
