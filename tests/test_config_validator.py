import pytest
import configparser
from ConfigValidator import config_validator
from ConfigValidator import example_configuration


def test_config_validator(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path + 'config.ini')
    sections = config_validator.get_sections(config_parser)
    code = config_validator.generate_code(sections)

    with open('example_configuration.py', 'a') as file:
        file.write(code)

    configuration = example_configuration.Configuration(path + 'config.ini')

    assert configuration.IMAGERY.url == 'imagery.url.org'
    assert configuration.Server.name == 'SuperServer'


def test_config_validator_bad(path):
    with pytest.raises(Exception) as exception_info:
        example_configuration.Configuration(path + 'bad_config.ini')

    assert 'Option url is not in section IMAGERY!' in str(exception_info.value)
