#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Prompt Toolkit Packages
from core.gnosis_console_engine import GnosisConsoleEngine
from safe_script import init_scenario

# Import GnosisSafe Module
from core.utils.contract.contract_console_data import ContractConsoleArtifacts


# Init Scenario with Random Safe with Setup (Pre-Loaded Contracts)
contract_artifacts_assests = init_scenario()

console_contract_artifacts = ContractConsoleArtifacts()
console_contract_artifacts.add_artifact(contract_artifacts_assests, alias='Gnosis-Safe(v1.1.0)')

gnosis_console_engine = GnosisConsoleEngine(contract_artifacts_assests)
gnosis_console_engine.run_console_session()
