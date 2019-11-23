from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter
import click
from fuzzyfinder import fuzzyfinder
from prompt_toolkit.validation import Validator, ValidationError

import re
SQLKeywords = ['addEther', 'sendEther']
ARGKeywords = ['--ether', '--miliether', '--microether', '--wei', '--Kwei', '--Mwei', '--Gwei']


def input_address_validation(address):
    """ Input Address Validation
     This function will validate the input address determining if the current value points a directory or if it's a
     address for a blockchain network.
     For References purposes:
        Tx Address: 0x3fbd9cdb8c51278062014032c50ea2ec66cc52f4c8be4136c3d416e2783d3b32
        Contract Address:  0xb23397f97715118532c8c1207F5678Ed4FbaEA6c

        :param address: this could be 0x or path to the contract if it's a local file being tested with ganache
        :return:
    """

    try:
        input_address = re.search('0x[aA-zZ,0-9]{40,64}', address).group(0)
        if len(address) is 42:
            print(len(address), ' ', address)
            return True
        elif len(address) is 66:
            print(len(address), ' ', address)
            return True
    except Exception:
        return False

class ContractFunctionCompleter(WordCompleter):
    def get_completions(self, document, complete_event):

        text = document.text
        if text == 'sendEther':
            word = document.get_word_before_cursor(WORD=True)
            matches = fuzzyfinder(word, ARGKeywords)
            for m in matches:
                yield Completion(m, start_position=-len(word))


class ContractInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if text == '--address=':
            if input_address_validation(text[len('--address='):]):
                print('address_found!!')
        else:
            raise ValidationError(message='This input contains valid address')



while True:
    try:
        user_input = prompt(u'SQL>', completer=ContractFunctionCompleter(), validator=ContractInputValidator(), validate_while_typing=False)
    except KeyboardInterrupt:
        continue  # Control-C pressed. Try again.
    except EOFError:
        break  # Control-D pressed.


regular_expresion_for_send_ether = r'(--wei|--Kwei|--Mwei|--Gwei|--microether|--miliether|--ether)((=[0-9]{0,})?)(\s*?)'