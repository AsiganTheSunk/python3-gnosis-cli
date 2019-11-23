#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from core.console_utils.contract_console_constants import _exit, simple_function_name, normal_address, uint_data, execute, queue, bytecode_data
import re


def is_valid_argument(regular_expresion, value):
    try:
        re.search(regular_expresion, value).group(0)
        return True
    except AttributeError:
        return False


class ContractLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted(NAMED_COLORS, key=NAMED_COLORS.get))

        def get_line(lineno):
            aux_list = []
            for index, word in enumerate(document.lines[lineno].split(' ')):
                current_color = colors[10 % len(colors)]
                if is_valid_argument(simple_function_name, word):
                    current_color = colors[50 % len(colors)]
                elif is_valid_argument(normal_address, word):
                    current_color = colors[250 % len(colors)]
                elif is_valid_argument(uint_data, word):
                    current_color = colors[110 % len(colors)]
                elif is_valid_argument(bytecode_data, word):
                    current_color = colors[140 % len(colors)]
                elif is_valid_argument(execute, word):
                    current_color = colors[170 % len(colors)]
                elif is_valid_argument(queue, word):
                    current_color = colors[200 % len(colors)]
                elif is_valid_argument(_exit, word):
                    current_color = colors[230 % len(colors)]
                aux_list.append((current_color, word + ' '))
            return aux_list
        return get_line