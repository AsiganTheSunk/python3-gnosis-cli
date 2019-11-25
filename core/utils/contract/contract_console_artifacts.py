#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ConsoleContractData:
    def __init__(self):
        self.contract_artifacts = {}

    def add_contract_artifacts(self, contract_artifacts, alias=''):
        if alias != '':
            self.contract_artifacts[alias] = contract_artifacts
            return self.contract_artifacts
        self.contract_artifacts['uContract' + str(len(self.contract_artifacts) - 1)] = contract_artifacts
        return self.contract_artifacts

    def get_contract_from_alias(self, stream, key):
        argument = stream.split('=')[1]
        try:
            print('loading_scontract_by_alias', self.contract_artifacts[argument][key])
            return self.contract_artifacts[argument][key]
        except KeyError as err:
            print(err)
