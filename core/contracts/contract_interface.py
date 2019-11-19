#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Os Packages
import os

# Import Subprocess Package
from subprocess import Popen, PIPE

# Import Truffle Command Constant
from core.contracts.constants.default_truffle_commands import TRUFFLE_COMPILE, TRUFFLE_HARD_MIGRATE, TRUFFLE_SOFT_MIGRATE

# Import Json ABIReader Package
from core.providers.utils.build_contract_reader import BuildContractReader

class ContractInterface:
    """A convenience interface for interacting with ethereum smart contracts

    This interface will handle a main contract and it's dependencies. All it
    requires is a path to the directory where your solidity files are stored.
    It will then compile, deploy, fetch a contract instance, and provide
    methods for transacting and calling with gas checks and event output.
    """

    def __init__(self, _provider, _contract_directory, _deployment_contract_list=[], _proxy_contract_list=[]):
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
            print('Start Truffle Compile')
            p = Popen('cd {contract_path}; {truffle_command}'.format(
                contract_path=self.contract_directory, truffle_command=TRUFFLE_COMPILE), stdout=PIPE, shell=True)
            p.wait()
            print('Done.')
            try:
                # If compile process is properly finished, map the build folder to get abi, bytecode and address data
                for root, directories, files in os.walk(self.contract_directory):
                    for file in files:
                        self.compiled_contract_list.append(os.path.abspath(os.path.join(root, file)))
                        # print('DEBUG: ', os.path.abspath(os.path.join(root, file)))

                print('Successfully compiled {number_of_files} contract files'.format(number_of_files=len(self.compiled_contract_list)))
            # Todo: Add Proper Exception Catching so in case of fatal can be raised to the top
            except Exception as err:
                print('inner loop compile sources', err)

            return True
        except Exception as err:
            print(err)
            return False

    def __deploy_contract(self, root, file, contract_to_proxy={}):
        account0 = self.provider.eth.accounts[0]
        print('---------' * 10)
        print('Start Deploying Contract', file[:-len('.json')])
        print('---------' * 10)
        # First we retrieve the current contract_abi & contract_byte code from .json build file
        contract_abi, contract_bytecode = self.build_contract_reader.read_from(os.path.abspath(os.path.join(root, file)))

        # Tmp Contract to make the deployment transaction
        tmp_contract = self.provider.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

        if contract_to_proxy != {}:
            # Submit the transaction deploying the contract, calling the constructor for the proxy
            tx_hash = tmp_contract.constructor(contract_to_proxy['address']).transact({'from': account0})
            # Wait for the transaction to be mined, and get the transaction receipt
            tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
            print('Proxy Contract Address: ', tx_receipt.contractAddress)
            print('Done.', '\n')
            return {'abi': contract_to_proxy['abi'], 'bytecode': contract_bytecode, 'address': tx_receipt.contractAddress}

        # Submit the transaction that deploys the contract
        tx_hash = tmp_contract.constructor().transact({'from': account0})
        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = self.provider.eth.waitForTransactionReceipt(tx_hash)
        print('Main Contract Address: ', tx_receipt.contractAddress)
        print('Done.', '\n')
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
        # Todo: set a compiling truffle exception, same for deployment + fatal
        contract_artifacts = {}
        if self.compiled_contract_list is []:
            print('Source files not compiled, compiling now and trying again...')
            try:
                self.compile_source_files()
                print('Done.')
            except Exception as err:
                print(err)

        try:
            # try-catch for Exceptions on truffle commands while using subprocess
            print('Start Truffle Migration')
            print('---------' * 10)
            p = Popen('cd {contract_path}; {truffle_command}'.format(
                contract_path=self.contract_directory, truffle_command=TRUFFLE_HARD_MIGRATE), stdout=PIPE, shell=True)
            p.wait()
            print('Done.', '\n')
            try:
                print('Deployment Contract List: ', self.deployment_contract_list)
                for root, directories, files in os.walk(self.contract_build_directory):
                    for file in files:
                        for to_deploy_contracts in self.deployment_contract_list:
                            if to_deploy_contracts == file[:-len('.json')]:
                                main_contract = file[:-len('.json')]
                                contract_artifacts[main_contract] = self.__deploy_contract(root, file)

                                # Todo: Make a dict association to bind the proxy to the proper contract and allow
                                #  more dynamic evaluation.
                                if self.proxy_contract_list is not []:
                                    print('Deployment Proxy Contract List: ', self.proxy_contract_list)
                                    for proxy_item in self.proxy_contract_list:
                                        contract_artifacts[proxy_item] = self.__deploy_contract(
                                            root, proxy_item + '.json', contract_artifacts[file[:-len('.json')]]
                                        )
                return contract_artifacts
            except Exception as err:
                print('rrr', err)
                pass

        except Exception as err:
            print(err)
            return {}

    def get_instance(self, _contract_artifacts):
        """Returns a contract instance object from variables in 'deployment_vars'

        Checks there is in fact an address saved. Also does a (crude) check
        that the deployment at that address is not empty. Reads variables
        created in 'deploy_contract' and creates a contract instance
        for use with all the 'Contract' methods specified in web3.py

        Returns:
            self.contract_instance(class ContractInterface): see above
        """

        # review: Web3.toChecksumAddress(contract_address)
        contract_abi = _contract_artifacts['abi']
        contract_address = _contract_artifacts['address']
        try:
            contract_bytecode_length = len(self.provider.eth.getCode(contract_address).hex())
            assert(contract_bytecode_length > 4)
        except AssertionError as err:
            print('Contract not deployed at {contract_address}.'.format(contract_address=contract_address), err)
            raise
        else:
            print(f'Contract deployed at {contract_address}. This function returns an instance object.')
        return self.provider.eth.contract(abi=contract_abi, address=contract_address)

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