
# Import Module Web3
from web3 import Web3

# validate contract address via regular expresion - use of mayus/lenth

# API_POOL with gnosis_asociated accounts 100 calls per day * 10 atleast
api_key_dict = {
    'API_KEY': {
        'etherscan': {
            '0': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '1': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '2': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '3': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '4': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '5': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
            '6': 'A1T1PKJXZJC1T4RJZK4ZMZH4JEYTUGAA6G',
        },
        'infura': {
            '0': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '1': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '2': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '3': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '4': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '5': 'b3fa360a82cd459e8f1b459b3cf9127c',
            '6': 'b3fa360a82cd459e8f1b459b3cf9127c',
        }
    }
}

class NetworkBlkInstance:
    def __init__(self, address):
        self.name = self.__class__.__name__

        self.address = address  # validate
        self.block_number = ''
        self.nonce = ''
        self.tx = ''
        self.owners = ''
        self.abi = ''  # if on etherscan - return abi of the contract.
        self.functions = ''  # if abi success, map the functions
        self.receipt = ''  # only if you use this instance to make transactions in the blockchain this will be fill
        self._properties = {'name': self.name, 'tx': self.tx, 'address': self.address, 'owners': self.owners,
                            'abi': self.abi, 'functions': self.functions, 'receipt': self.receipt}

    def __getitem__(self, _key):
        if _key == 'properties':
            return self._properties
        return self._properties[_key]

    def set_address(self, _address):
        self.address = _address

    def set_block(self, _block_number):
        self.block_number = _block_number

    def set_nonce(self, _nonce):
        self.nonce = _nonce

    def set_tx(self, _tx):
        self.tx = _tx

    def set_owners(self, _owners):
        self.owners = _owners

    def set_abi(self, _abi):
        self.abi = _abi

    def set_function(self, _function):
        self.functions = _function

    def set_receipt(self, _receipt):
        self.receipt = _receipt

    def map_address(self, address):
        # print(web3.web3.getTransactionCount('0x6fF6b266dA243Cf12337f82B50ecc2eFCbF748b6'))
        # contractAddress = '0x3c7bec02bd4fa73dce24413d2a13c02e1a91e858'
        # 0x4DC3643DbC642b72C158E7F3d2ff232df61cb6CE

        return

    def map_functions(self):
        return

    def map_abi(self):
        return


def main():
    address0 = "0xf79cb3BEA83BD502737586A6E8B133c378FD1fF2"
    network_blk_instance = NetworkBlkInstance(address=address0)

    print(len(address0))

    address1 = '0x3c7bec02bd4fa73dce24413d2a13c02e1a91e858'

    print(len(address1))

    address2_safe = '0x522715235d66faeF072509697445A66B442faD88'

    import re
    # re.search('[aA-zZ,0-9]')
    # re.search('[A-Z,0-9]')

    ETHERSCAN_API_KEY = api_key_dict['API_KEY']['etherscan']['0']
    import etherscan
    es = etherscan.Client(
        api_key=ETHERSCAN_API_KEY,
        cache_expire_after=5,
    )

    # print(es.get_eth_price())
    # print(es.get_gas_price())


if __name__ == '__main__':
    main()

# give contract file, compile it and genertate the code,
# give abi .json build files with the data

# Externally Owned Accounts (EOA) : these accounts are controlled by their private key.
# Contracts Accounts (Smart Contracts) : these accounts are controlled by their code.

# 2a5bc342ed616b5ba5732269001d3f1ef827552ae1114027bd3ecf1f086ba0f9
# Address = 0x001d3f1ef827552ae1114027bd3ecf1f086ba0f9
# 0x001d3f1ef827552ae1114027bd3ecf1f086ba0f9 or
# 0X001D3F1EF827552AE1114027BD3ECF1F086BA0F9

# Address literals
#
# Address literals are the hexadecimal representation of an Ethereum address (prefixed with 0x)
# that pass the checksum test. (Apparently their size range from 39 to 41 digits). You can declare
# address literals in Solidity as follow :
# address owner = 0xc0ffee254729296a45a3885639AC7E10F9d54979


# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md
# from ethereum import utils
#
# def checksum_encode(addr): # Takes a 20-byte binary address as input
#     o = ''
#     v = utils.big_endian_to_int(utils.sha3(addr.hex()))
#     for i, c in enumerate(addr.hex()):
#         if c in '0123456789':
#             o += c
#         else:
#             o += c.upper() if (v & (2**(255 - 4*i))) else c.lower()
#     return '0x'+o
#
# def test(addrstr):
#     assert(addrstr == checksum_encode(bytes.fromhex(addrstr[2:])))
#
# test('0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed')
# test('0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359')
# test('0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB')
# test('0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb')
