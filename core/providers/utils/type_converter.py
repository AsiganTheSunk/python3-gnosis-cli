class ContractTypeConverter:
    def __init__(self):
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

from web3 import Web3

def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))
