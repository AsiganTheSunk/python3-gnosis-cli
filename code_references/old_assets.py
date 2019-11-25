
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

def eval_function_old(param, param_type=None):
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

# reference: https://github.com/prompt-toolkit/python-prompt-toolkit/tree/master/examples/prompts
