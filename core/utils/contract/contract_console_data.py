class ConsoleContractData:
    def __init__(self):
        self.contract_data = {}

    def add_contract_artifacts(self, contract_artifacts, alias=''):
        if alias != '':
            self.contract_data[alias] = contract_artifacts
            return self.contract_data
        self.contract_data['uContract' + str(len(self.contract_data) -1)] = contract_artifacts
        return self.contract_data

    def get_contract_from_alias(self, stream, key):
        argument = stream.split('=')[1]
        try:
            print(self.contract_data[argument][key])
            print(self.contract_data[argument][key])
        except KeyError as err:
            print(err)
