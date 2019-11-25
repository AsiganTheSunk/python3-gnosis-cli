from web3 import Web3
import json

test_abi_contract = [{"name": "TokenPurchase", "inputs": [{"type": "address", "name": "buyer", "indexed": 'true'}, {"type": "uint256", "name": "eth_sold", "indexed": 'true'}, {"type": "uint256", "name": "tokens_bought", "indexed": 'true'}], "anonymous": 'false', "type": "event"}, {"name": "EthPurchase", "inputs": [{"type": "address", "name": "buyer", "indexed": 'true'}, {"type": "uint256", "name": "tokens_sold", "indexed": 'true'}, {"type": "uint256", "name": "eth_bought", "indexed": 'true'}], "anonymous": 'false', "type": "event"}, {"name": "AddLiquidity", "inputs": [{"type": "address", "name": "provider", "indexed": 'true'}, {"type": "uint256", "name": "eth_amount", "indexed": 'true'}, {"type": "uint256", "name": "token_amount", "indexed": 'true'}], "anonymous": 'false', "type": "event"}, {"name": "RemoveLiquidity", "inputs": [{"type": "address", "name": "provider", "indexed": 'true'}, {"type": "uint256", "name": "eth_amount", "indexed": 'true'}, {"type": "uint256", "name": "token_amount", "indexed": 'true'}], "anonymous": 'false', "type": "event"}, {"name": "Transfer", "inputs": [{"type": "address", "name": "_from", "indexed": 'true'}, {"type": "address", "name": "_to", "indexed": 'true'}, {"type": "uint256", "name": "_value", "indexed": 'false'}], "anonymous": 'false', "type": "event"}, {"name": "Approval", "inputs": [{"type": "address", "name": "_owner", "indexed": 'true'}, {"type": "address", "name": "_spender", "indexed": 'true'}, {"type": "uint256", "name": "_value", "indexed": 'false'}], "anonymous": 'false', "type": "event"}, {"name": "setup", "outputs": [], "inputs": [{"type": "address", "name": "token_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 175875}, {"name": "addLiquidity", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "min_liquidity"}, {"type": "uint256", "name": "max_tokens"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'true', "type": "function", "gas": 82616}, {"name": "removeLiquidity", "outputs": [{"type": "uint256", "name": "out"}, {"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "amount"}, {"type": "uint256", "name": "min_eth"}, {"type": "uint256", "name": "min_tokens"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 116814}, {"name": "__default__", "outputs": [], "inputs": [], "constant": 'false', "payable": 'true', "type": "function"}, {"name": "ethToTokenSwapInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "min_tokens"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'true', "type": "function", "gas": 12757}, {"name": "ethToTokenTransferInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "min_tokens"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}], "constant": 'false', "payable": 'true', "type": "function", "gas": 12965}, {"name": "ethToTokenSwapOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'true', "type": "function", "gas": 50463}, {"name": "ethToTokenTransferOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}], "constant": 'false', "payable": 'true', "type": "function", "gas": 50671}, {"name": "tokenToEthSwapInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_eth"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 47503}, {"name": "tokenToEthTransferInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_eth"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 47712}, {"name": "tokenToEthSwapOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "eth_bought"}, {"type": "uint256", "name": "max_tokens"}, {"type": "uint256", "name": "deadline"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 50175}, {"name": "tokenToEthTransferOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "eth_bought"}, {"type": "uint256", "name": "max_tokens"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 50384}, {"name": "tokenToTokenSwapInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_tokens_bought"}, {"type": "uint256", "name": "min_eth_bought"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "token_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 51007}, {"name": "tokenToTokenTransferInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_tokens_bought"}, {"type": "uint256", "name": "min_eth_bought"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}, {"type": "address", "name": "token_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 51098}, {"name": "tokenToTokenSwapOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "max_tokens_sold"}, {"type": "uint256", "name": "max_eth_sold"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "token_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 54928}, {"name": "tokenToTokenTransferOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "max_tokens_sold"}, {"type": "uint256", "name": "max_eth_sold"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}, {"type": "address", "name": "token_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 55019}, {"name": "tokenToExchangeSwapInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_tokens_bought"}, {"type": "uint256", "name": "min_eth_bought"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "exchange_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 49342}, {"name": "tokenToExchangeTransferInput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}, {"type": "uint256", "name": "min_tokens_bought"}, {"type": "uint256", "name": "min_eth_bought"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}, {"type": "address", "name": "exchange_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 49532}, {"name": "tokenToExchangeSwapOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "max_tokens_sold"}, {"type": "uint256", "name": "max_eth_sold"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "exchange_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 53233}, {"name": "tokenToExchangeTransferOutput", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}, {"type": "uint256", "name": "max_tokens_sold"}, {"type": "uint256", "name": "max_eth_sold"}, {"type": "uint256", "name": "deadline"}, {"type": "address", "name": "recipient"}, {"type": "address", "name": "exchange_addr"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 53423}, {"name": "getEthToTokenInputPrice", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "eth_sold"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 5542}, {"name": "getEthToTokenOutputPrice", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_bought"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 6872}, {"name": "getTokenToEthInputPrice", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "tokens_sold"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 5637}, {"name": "getTokenToEthOutputPrice", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "uint256", "name": "eth_bought"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 6897}, {"name": "tokenAddress", "outputs": [{"type": "address", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1413}, {"name": "factoryAddress", "outputs": [{"type": "address", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1443}, {"name": "balanceOf", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "address", "name": "_owner"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 1645}, {"name": "transfer", "outputs": [{"type": "bool", "name": "out"}], "inputs": [{"type": "address", "name": "_to"}, {"type": "uint256", "name": "_value"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 75034}, {"name": "transferFrom", "outputs": [{"type": "bool", "name": "out"}], "inputs": [{"type": "address", "name": "_from"}, {"type": "address", "name": "_to"}, {"type": "uint256", "name": "_value"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 110907}, {"name": "approve", "outputs": [{"type": "bool", "name": "out"}], "inputs": [{"type": "address", "name": "_spender"}, {"type": "uint256", "name": "_value"}], "constant": 'false', "payable": 'false', "type": "function", "gas": 38769}, {"name": "allowance", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [{"type": "address", "name": "_owner"}, {"type": "address", "name": "_spender"}], "constant": 'true', "payable": 'false', "type": "function", "gas": 1925}, {"name": "name", "outputs": [{"type": "bytes32", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1623}, {"name": "symbol", "outputs": [{"type": "bytes32", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1653}, {"name": "decimals", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1683}, {"name": "totalSupply", "outputs": [{"type": "uint256", "name": "out"}], "inputs": [], "constant": 'true', "payable": 'false', "type": "function", "gas": 1713}]

project_api_key = 'https://mainnet.infura.io/v3/b3fa360a82cd459e8f1b459b3cf9127c'
test_safe_addr = '0x522715235d66faeF072509697445A66B442faD88'

web3 = Web3(Web3.HTTPProvider(project_api_key))
print(web3.isConnected())
# print(web3.eth.blockNumber)
balance = web3.eth.getBalance(test_safe_addr)
print(balance)

address = "0xf79cb3BEA83BD502737586A6E8B133c378FD1fF2"
contract = web3.eth.contract(address=address, abi=test_abi_contract)

# print(contract.__dict__)
# print(contract.address)

current_abi_function = contract.functions.__dict__
# for item in current_abi_function['abi']:
#     print(item['name'])
#     print(item['inputs'])
#     try:
#         print(item['outputs'])
#     except Exception as err:
#         pass

# contractAddress = '0x3c7bec02bd4fa73dce24413d2a13c02e1a91e858'
# print(web3.eth.blockNumber)

# print(web3.fromWei(balance, "ether"))
# print(web3.web3.getTransactionCount('0x6fF6b266dA243Cf12337f82B50ecc2eFCbF748b6'))
# print(web3.web3.hashrate)
# print(web3.web3.protocolVersion)
# print(web3.web3.chainId)
# print(web3.web3.syncing)
# print(web3.web3.getBlock('latest'))

# print('Creator',contract)
# print('OracleName',contract.call().oracleName)

# with open('factory.json', 'r') as abi_definition:
#     abi = json.load(abi_definition)

# from web3.contract import ConciseContract
# reader = ConciseContract(fContract)
# print(reader)
# assert reader.creator()      == fContract.functions.creator().call()
# assert reader.newContracts() == fContract.functions.newContracts().call()
# assert reader.oracleName()   == fContract.functions.oracleName().call()

#
# from eth_utils import (
#     keccak,
# )
# import rlp
# from rlp.sedes import (
#     Binary,
#     big_endian_int,
# )
# from trie import (
#     HexaryTrie,
# )
# from web3._utils.encoding import (
#     pad_bytes,
# )
#
# def format_proof_nodes(proof):
#     trie_proof = []
#     for rlp_node in proof:
#         trie_proof.append(rlp.decode(bytes(rlp_node)))
#     return trie_proof
#
# def verify_eth_getProof(proof, root):
#     trie_root = Binary.fixed_length(32, allow_empty=True)
#     hash32 = Binary.fixed_length(32)
#
#     class _Account(rlp.Serializable):
#         fields = [
#                     ('nonce', big_endian_int),
#                     ('balance', big_endian_int),
#                     ('storage', trie_root),
#                     ('code_hash', hash32)
#                 ]
#     acc = _Account(
#         proof.nonce, proof.balance, proof.storageHash, proof.codeHash
#     )
#     rlp_account = rlp.encode(acc)
#     trie_key = keccak(bytes.fromhex(proof.address[2:]))
#
#     assert rlp_account == HexaryTrie.get_from_proof(
#         root, trie_key, format_proof_nodes(proof.accountProof)
#     ), "Failed to verify account proof {}".format(proof.address)
#
#     for storage_proof in proof.storageProof:
#         trie_key = keccak(pad_bytes(b'\x00', 32, storage_proof.key))
#         root = proof.storageHash
#         if storage_proof.value == b'\x00':
#             rlp_value = b''
#         else:
#             rlp_value = rlp.encode(storage_proof.value)
#
#         assert rlp_value == HexaryTrie.get_from_proof(
#             root, trie_key, format_proof_nodes(storage_proof.proof)
#         ), "Failed to verify storage proof {}".format(storage_proof.key)
#
#     return True
#
# block = web3.web3.getBlock(3391)
# proof = web3.web3.getProof('0x6C8f2A135f6ed072DE4503Bd7C4999a1a17F824B', [0, 1], 3391)
# assert verify_eth_getProof(proof, block.stateRoot)