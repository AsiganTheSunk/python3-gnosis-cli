#!/usr/bin/env python
"""
Demo of "operate-and-get-next".
(Actually, this creates one prompt application, and keeps running the same app
over and over again. -- For now, this is the only way to get this working.)
"""
from prompt_toolkit.shortcuts import PromptSession


def run_console_session(previous_session=None, prompt_text='new prompt>'):
    if previous_session is not None:
        session = PromptSession(prompt_text)
    else:
        session = PromptSession('prompt> ')
    try:
        while True:
            text = session.prompt()
            if text == 'new':
                run_console_session(previous_session=session, prompt_text='new prompt>')
            if text == 'exit':
                return previous_session
    except EOFError as err:
        return previous_session


run_console_session()

# Todo: Lexer per init of console, type of session, so emun to flag the type focusing on usability in the future
# Todo: Module loader, so it can run the setup for the contract you want to operate with
# Todo: Report the pos of the word to the lexer so it can know if it's dealing with a call to a function or an param
# Todo: Build the suffix + affix list for the management of simple contracts
# Todo: Improve function mapping so it can properly separate Events(Emit's) from the contract methods from the actual functions
# Todo: Maybe Add a listener for the Events done by the contract atleast locally so it can be studied how it behaves
# Todo: Add Interface for the Common Contract Operations Setup(), Transact() etc etc so it can be called from the console
#   If None are provided, the console will assume an standar way of operation for the basic known transaction procedures
# Todo: Move Current "Setup" for the GnosisSafe to it's proper module
# Todo: Move Current "Transact" overrider to the GnosisSafe module
# Todo: Only add to the temporal lexer valid addresses (it has been operated with)
