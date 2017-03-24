import os
from ConfigValidator.example_configuration import Configuration

directory, _ = os.path.split(os.path.abspath(__file__))
configuration = Configuration(config_file_path=directory + '/config.ini')

print(configuration.SERVER.name, configuration.SERVER.host)
# output: SuperServer 127.0.0.1
