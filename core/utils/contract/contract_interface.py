#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Os Packages
import os

# Import Subprocess Package
from subprocess import Popen, PIPE

# Import Truffle Command Constant
from core.constants.default_truffle_commands import TRUFFLE_COMPILE, TRUFFLE_HARD_MIGRATE

# Import Json ABIReader Package
from core.utils.build_contract_reader import BuildContractReader

class ContractInterface:
    """A convenience interface for interacting with ethereum smart contracts

    This interface will handle a main contract and it's dependencies. All it
    requires is a path to the directory where your solidity files are stored.
    It will then compile, deploy, fetch a contract instance, and provide
    methods for transacting and calling with gas checks and event output.
    """

    def __init__(self, provider, contract_directory, deployment_contract_list=[], proxy_contract_list=[]):
        """Accepts contract, directory, and an RPC connection and sets defaults
        Parameters:
            provider (Web3 object): the RPC node you'll make calls to (e.g. geth, ganache-cli)
            deployment_contract_list (str): name of the contract you want to interface with
            contract_directory (path): location of Solidity source files
            ¿?# max_deploy_gas (int): max gas to use on deploy, see 'deploy_contract'
            ¿?# max_tx_gas (int): max gas to use for transactions, see 'send'
            deployment_vars_path (path): default path for storing deployment variables

        Also sets web3.eth.defaultAccount as the coinbase account (e.g. the
        first key pair/account in ganache) for all send parameters
        """

        self.provider = provider
        self.contract_directory = contract_directory + 'contracts/'
        self.contract_build_directory = contract_directory + 'build/contracts/'
        self.deployment_contract_list = deployment_contract_list
        self.compiled_contract_list = []
        self.provider.eth.defaultAccount = provider.eth.coinbase
        self.build_contract_reader = BuildContractReader()
        self.proxy_contract_list = proxy_contract_list

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
        ''' Deploy Contract
        This function to setup the proper deploy of the contracts
            :param root: Root Folder
            :param file: Root File
            :param contract_to_proxy: In case the main contract it's deployed with a proxy contract
            :return: contract artifacts (abi/bytecode)
        '''
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

    def deploy_contract(self, migrate=False):
        """Deploys contract specified by 'contract_to_deploy'

        This function will deploy the contract provided in the initialization of the class
        (should estimate deployment gas and compares that to max_deploy_gas before
        deploying.)
        """
        # Todo: set a compiling truffle exception, same for deployment + fatal
        contract_artifacts = {}
        # Map de Assets Directory
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


    def get_instance(self, contract_artifacts, contract_address):
        ''' Connect To Instance
        Fucntion connect to a  smart contract, you only need address?
        :param contract_artifacts:
        :param contract_address:
        :return:
        '''
        return

    def get_new_instance(self, contract_artifacts):
        """Returns a contract instance object from variables in 'deployment_vars'

        Checks there is in fact an address saved. Also does a (crude) check
        that the deployment at that address is not empty. Reads variables
        created in 'deploy_contract' and creates a contract instance
        for use with all the 'Contract' methods specified in web3.py

        Returns:
            self.contract_instance(class ContractInterface): see above
        """

        # review: Web3.toChecksumAddress(contract_address)
        contract_abi = contract_artifacts['abi']
        contract_address = contract_artifacts['address']
        try:
            contract_bytecode_length = len(self.provider.eth.getCode(contract_address).hex())
            assert(contract_bytecode_length > 4)
        except AssertionError as err:
            print('Contract not deployed at {contract_address}.'.format(contract_address=contract_address), err)
            raise
        else:
            print(f'Contract deployed at {contract_address}. This function returns an instance object.')
        return self.provider.eth.contract(abi=contract_abi, address=contract_address)
