import configparser
config = configparser.ConfigParser()
# config['DEFAULT'] = {'ServerAliveInterval': '45',
#                       'Compression': 'yes',
#                       'CompressionLevel': '9'}
# config['bitbucket.org'] = {}
# config['bitbucket.org']['User'] = 'hg'
# config['topsecret.server.com'] = {}
# topsecret = config['topsecret.server.com']
# topsecret['Port'] = '50022'     # mutates the parser
# topsecret['ForwardX11'] = 'no'  # same here
# config['DEFAULT']['ForwardX11'] = 'yes'
#
# with open('example.ini', 'w') as configfile:
#     config.write(configfile)

config.read('./gnosis_safe_contract_v1_1_0.ini')


for key in config['GnosisSafeSetup']:
    print(config['GnosisSafeSetup'][key])



