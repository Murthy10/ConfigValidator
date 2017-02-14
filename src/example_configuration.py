import configparser
import os


class Configuration:
    def __init__(self, config_file_path=''):
        config_parser = self.read_configuration_file(config_file_path)
        sections = [
            {'section': 'IMAGERY', 'options': [{'option': 'url', 'fallback': 'imagery.url.org'}, {'option': 'zoomlevel', 'fallback': '19'}]},
            {'section': 'Server', 'options': [{'option': 'name', 'fallback': 'SuperServer'}, {'option': 'host', 'fallback': '127.0.0.1'}, {'option': 'list', 'fallback': '1,2,3,4'}]},
        ]
        self.check_sections(config_parser, sections)
        self.set_options(config_parser, sections)

    def set_options(self, config_parser, sections):
        for section in sections:
            for option in section['options']:
                if not config_parser.has_option(section['section'], option['option']):
                    raise Exception('Option {0} is not in section {1}!'.format(option['option'], section['section']))
                setattr(self, option['option'], config_parser.get(section['section'], option['option'], fallback=option['fallback']))

    @staticmethod
    def read_configuration_file(config_file_path):
        if not os.path.isfile(config_file_path):
            raise Exception("The config file does not exist!")
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file_path)
        return config_parser

    @staticmethod
    def check_sections(config_parser, sections):
        for section in sections:
            if not config_parser.has_section(section['section']):
                raise Exception('Section {0} is not in config file!'.format(section['section']))

