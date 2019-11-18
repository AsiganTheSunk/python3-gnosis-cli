import os
import pprint
import json

from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
from solcx import compile_source, compile_files, install_solc, get_available_solc_versions

import sys
import time
import pprint
from solc import compile_files as compile_files2
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3

from core.providers.constants.contract_contants import NULL_ADDRESS

from subprocess import Popen, PIPE

from core.contracts.constants.default_truffle_commands import TRUFFLE_COMPILE, TRUFFLE_HARD_MIGRATE, TRUFFLE_SOFT_MIGRATE

from core.providers.utils.build_contract_reader import BuildContractReader

class ContractInterface:
    """A convenience interface for interacting with ethereum smart contracts

    This interface will handle a main contract and it's dependencies. All it
    requires is a path to the directory where your solidity files are stored.
    It will then compile, deploy, fetch a contract instance, and provide
    methods for transacting and calling with gas checks and event output.
    """
    # version = get_available_solc_versions()
    # print(version)
    # install_solc('v0.5.0')
    default_vars_path = os.path.join(os.getcwd(), 'deployment_variables.json')

    def __init__(self, _provider, _contract_directory, _deployment_contract_list, _proxy_contract_list, max_deploy_gas=500000, max_tx_gas=50000):
        """Accepts contract, directory, and an RPC connection and sets defaults

        Parameters:
            _provider (Web3 object): the RPC node you'll make calls to (e.g. geth, ganache-cli)
            _deployment_contract_list (str): name of the contract you want to interface with
            _contract_directory (path): location of Solidity source files
            max_deploy_gas (int): max gas to use on deploy, see 'deploy_contract'
            max_tx_gas (int): max gas to use for transactions, see 'send'
            deployment_vars_path (path): default path for storing deployment variables

        Also sets web3.eth.defaultAccount as the coinbase account (e.g. the
        first key pair/account in ganache) for all send parameters
        """

        self.provider = _provider
        self.contract_directory = _contract_directory + 'contracts/'
        self.contract_build_directory = _contract_directory + 'build/contracts/'
        self.deployment_contract_list = _deployment_contract_list
        self.compiled_contract_list = []
        self.max_deploy_gas = max_deploy_gas
        self.max_tx_gas = max_tx_gas
        self.provider.eth.defaultAccount = _provider.eth.coinbase
        self.build_contract_reader = BuildContractReader()
        self.proxy_contract_list = _proxy_contract_list

    def compile_source_files(self):
        """Compiles 'contract_to_deploy' from specified contract.

        Loops through contracts in 'contract_directory' and creates a list of
        absolute paths to be passed to the py-solc-x's 'compile_files' method.

        Returns:
            self.all_compiled_contracts (dict): all the compiler outputs (abi, bin, ast...)
            for every contract in contract_directory
        """

        try:
            # try-catch for Exceptions on truffle commands while using subprocess
            print('start compile')
            p = Popen('cd {contract_path}; {truffle_command}'.format(
                contract_path=self.contract_directory, truffle_command=TRUFFLE_COMPILE), stdout=PIPE, shell=True)
            p.wait()
            print('finish compile')
            try:
                # If compile process is properly finished, map the build folder to get abi, bytecode and address data
                for root, directories, files in os.walk(self.contract_directory):
                    for file in files:

                        self.compiled_contract_list.append(os.path.abspath(os.path.join(root, file)))
                        print('INFO : ', os.path.abspath(os.path.join(root, file)))

                print('Successfully compiled {number_of_files} contract files'.format(number_of_files=len(self.compiled_contract_list)))
            # Todo: Add Proper Exception Catching so in case of fatal can be raised to the top
            except Exception as err:
                print('inner loop compile sources', err)

            return True
        except Exception as err:
            print(err)
            return False


    def __deploy_contract(self, root, file, address_to_proxy=NULL_ADDRESS):
        print('Deploying Contract', file[:-len('.json')])
        # First we retrieve the current contract_abi & contract_byte code from .json build file
        contract_abi, contract_bytecode = self.build_contract_reader.read_from(os.path.abspath(os.path.join(root, file)))

        # Tmp Contract to make the deployment transaction
        tmp_contract = self.provider.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

        if address_to_proxy != NULL_ADDRESS:
            # Submit the transaction deploying the contract, calling the constructor for the proxy
            tx_hash = tmp_contract.constructor(address_to_proxy).transact()
            # Wait for the transaction to be mined, and get the transaction receipt
            tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
            return {'contract_abi': contract_abi, 'contract_bytecode': contract_bytecode, 'contract_address':  tx_receipt.contractAddress}

        # Submit the transaction that deploys the contract
        tx_hash = tmp_contract.constructor().transact()
        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
        return {'abi': contract_abi, 'bytecode': contract_bytecode, 'address':  tx_receipt.contractAddress}

    def deploy_contract(self):
        """Deploys contract specified by 'contract_to_deploy'

        Estimates deployment gas and compares that to max_deploy_gas before
        deploying. Also writes out variables required to create a contract
        instance to 'deployment_vars' to easily recreate it after exiting
        program.

        Parameters:
            deployment_params (dict): optional dictionary for overloading the
            default deployment transaction parameters. See web3.py's
            eth.sendTransaction for more info.
        """

        contract_data = {}
        print('SELF COMPILED: ', self.compiled_contract_list is [])
        if self.compiled_contract_list is []:
            print('Source files not compiled, compiling now and trying again...')
            try:
                self.compile_source_files()
            # Todo: set a compiling truffle exception, same for deployment + fatal
            except Exception as err:
                print(err)

        try:
            # try-catch for Exceptions on truffle commands while using subprocess
            print('start migration')
            p = Popen('cd {contract_path}; {truffle_command}'.format(
                contract_path=self.contract_directory, truffle_command=TRUFFLE_HARD_MIGRATE), stdout=PIPE, shell=True)
            p.wait()
            print('finished migration')
            try:
                print('Compile Contract List: ', self.compiled_contract_list)
                print('Deployment Contract List: ', self.deployment_contract_list)
                for root, directories, files in os.walk(self.contract_build_directory):
                    for file in files:

                        for to_deploy_contracts in self.deployment_contract_list:
                            if to_deploy_contracts == file[:-len('.json')]:
                                main_contract = file[:-len('.json')]
                                contract_data[main_contract] = self.__deploy_contract(root, file)
                                print(contract_data[main_contract]['address'])
                            # if to_deploy_contracts == file[:-len('.json')]:
                            #     print('Deploying Contract ', file[:-len('.json')])
                            #     contract_abi, contract_bytecode = self.build_contract_reader.read_from(
                            #         os.path.abspath(os.path.join(root, file)))
                            #     tmp_contract = self.provider.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
                            #     # Submit the transaction that deploys the contract
                            #     tx_hash = tmp_contract.constructor().transact()
                            #
                            #     # Wait for the transaction to be mined, and get the transaction receipt
                            #     tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
                            #
                            #     deployed_contract = self.provider.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)
                            #     print('Address:', tx_receipt.contractAddress)
                                if self.proxy_contract_list is not []:
                                    for proxy_item in self.proxy_contract_list:
                                        contract_data[proxy_item] = self.__deploy_contract(root, proxy_item + '.json', contract_data[file[:-len('.json')]]['address'])
                                        print(contract_data)
                                    # contract_abi, contract_bytecode = self.build_contract_reader.read_from(
                                    #     os.path.abspath(os.path.join(root, file)))
                                    # tmp_contract = self.provider.eth.contract(abi=contract_abi,
                                    #                                           bytecode=contract_bytecode)
                                    # # Submit the transaction that deploys the contract
                                    # tx_hash = tmp_contract.constructor(tx_receipt.contractAddress).transact()
                                    #
                                    # # Wait for the transaction to be mined, and get the transaction receipt
                                    # proxy_tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
                                    #
                                    # deployed_contract = self.provider.eth.contract(address=proxy_tx_receipt.contractAddress, abi=contract_abi)
                                    # print('Address:', proxy_tx_receipt.contractAddress)



                    #
                    #



            except Exception as err:
                print(err)
                pass

        except Exception as err:
            print(err)

    def get_instance(self):
        """Returns a contract instance object from variables in 'deployment_vars'

        Checks there is in fact an address saved. Also does a (crude) check
        that the deployment at that address is not empty. Reads variables
        created in 'deploy_contract' and creates a contract instance
        for use with all the 'Contract' methods specified in web3.py

        Returns:
            self.contract_instance(class ContractInterface): see above
        """

        with open (self.deployment_vars_path, 'r') as read_file:
            vars = json.load(read_file)

        try:
            self.contract_address = vars['contract_address']
        except ValueError(
            f"No address found in {self.deployment_vars_path}, please call 'deploy_contract' and try again."):
            raise

        contract_bytecode_length = len(self.provider.eth.getCode(self.contract_address).hex())

        try:
            assert (contract_bytecode_length > 4), f"Contract not deployed at {self.contract_address}."
        except AssertionError as e:
            print(e)
            raise
        else:
            print(f"Contract deployed at {self.contract_address}. This function returns an instance object.")

        self.contract_instance = self.provider.eth.contract(
            abi = vars['contract_abi'],
            address = vars['contract_address']
        )

        return self.contract_instance



    # def retrieve(self, function_, *call_args, tx_params=None):
    #     """Contract.function.call() with cleaning"""
    #
    #     fxn_to_call = getattr(self.contract_instance.functions, function_)
    #     built_fxn = fxn_to_call(*call_args)
    #
    #     return_values = built_fxn.call(transaction=tx_params)
    #
    #     if type(return_values) == bytes:
    #         return_values = return_values.decode('utf-8').rstrip("\x00")
    #
    #     return return_values


