class ContractConsoleArtifacts:
    def __init__(self, contract_artifact_list=None):
        self.contract_artifact_list = contract_artifact_list
        self.contract_data = {}

        # if self.contract_artifact_list is not None:
        #     for contract_artifacts_item in contract_artifact_list:
        #         data = self.add_artifact(contract_artifacts_item)
        #         self.update_data(data)
        #
        # print(self.contract_data['uContract0']['address'])


    def update_data(self, data):
        self.contract_data = data

    def add_artifact(self, contract_artifacts, alias=''):
        if alias != '':
            self.contract_data[alias] = contract_artifacts
            return self.contract_data

        self.contract_data['uContract' + str(len(self.contract_data))] = contract_artifacts

        return self.contract_data

    def get_key_from_alias(self, alias, key=None):
        try:
            if key is None:
                return self.contract_data[alias]
            return self.contract_data[alias][key]
        except KeyError:
            raise KeyError
        except Exception as err:
            print(type(err), err)
