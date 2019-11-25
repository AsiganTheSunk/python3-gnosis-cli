from core.utils.contract.contract_truffle import TruffleInterface
from core.utils.ganache_provider import GanacheProvider
import os

from core.utils.gnosis_safe_setup import GnosisSafeModule

def init_scenario():
    PROJECT_DIRECTORY = os.getcwd() + '/assets/safe-contracts-1.1.0/'
    ganache_provider = GanacheProvider()
    provider = ganache_provider.get_provider()
    contract_interface = TruffleInterface(provider, PROJECT_DIRECTORY, ['GnosisSafe'], ['Proxy'])
    contract_artifacts = contract_interface.deploy_contract()

    # remark: Get Contract Artifacts for the Proxy & GnosisSafe
    safe_instance = contract_interface.get_new_instance(contract_artifacts['GnosisSafe'])
    proxy_instance = contract_interface.get_new_instance(contract_artifacts['Proxy'])

    # remark: Get Interface to interact with the contract
    gnosis_safe_module = GnosisSafeModule(provider, contract_artifacts)
    functional_safe = gnosis_safe_module.setup(safe_instance, proxy_instance)

    tmp_contract_artifacts = {
        'instance': functional_safe,
        'abi': contract_artifacts['GnosisSafe']['abi'],
        'bytecode': contract_artifacts['GnosisSafe']['bytecode'],
        'address': contract_artifacts['GnosisSafe']['address']
    }

    return tmp_contract_artifacts