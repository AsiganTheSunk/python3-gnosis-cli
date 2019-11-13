from web3 import Web3
import json

project_api_key = 'https://mainnet.infura.io/v3/b3fa360a82cd459e8f1b459b3cf9127c'
test_safe_addr = '0x522715235d66faeF072509697445A66B442faD88'

web3 = Web3(Web3.HTTPProvider(project_api_key))
# print(web3.isConnected())
# print(web3.eth.blockNumber)
balance = web3.eth.getBalance(test_safe_addr)


address = "0xf79cb3BEA83BD502737586A6E8B133c378FD1fF2"
contract = web3.eth.contract(address=address, abi=abi)

# print(contract.__dict__)
# print(contract.address)
current_abi_function = contract.functions.__dict__
for item in current_abi_function['abi']:
    print(item['name'])
    print(item['inputs'])
    try:
        print(item['outputs'])
    except Exception as err:
        pass

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