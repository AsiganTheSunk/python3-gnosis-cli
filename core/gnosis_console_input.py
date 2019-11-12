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
from core.providers.ganache_provider import GanacheProvider
from core.providers.infura_provider import InfuraProvider

# Import Sys Package
import sys


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

def main():
    # connection = sqlite3.connect(database)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=gnosis_safe_cli_completer, style=style)

    while True:
        try:
            text = session.prompt(' (gnosis-safe-manager-cli)> ')
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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        db = ':memory:'
    else:
        db = sys.argv[1]

    main(db)

# #!/usr/bin/env python
# """
# A very simple progress bar where the name of the task scrolls, because it's too long.
# iterator.
# """
# import time
#
# from prompt_toolkit.shortcuts import ProgressBar
#
#
# def main():
#     with ProgressBar(title='Scrolling task name (make sure the window is not too big).') as pb:
#         for i in pb(range(800), label='This is a very very very long task that requires horizontal scrolling ...'):
#             time.sleep(.01)
