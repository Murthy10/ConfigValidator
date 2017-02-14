import argparse
import configparser
import os
import sys


class Row:
    def __init__(self, intents=0, code="", line_break=True):
        self.intents = intents
        self.code = code
        self.line_break = line_break


def join_rows(rows):
    text = ""
    for row in rows:
        space = row.intents * "    "
        text += space + row.code
        if row.line_break:
            text += "\n"
    return text


def get_options(config):
    options = []
    for config_section in config.sections():
        for key, value in config.items(config_section):
            parameter = dict(section=config_section, option=key, value=value)
            options.append(parameter)
    return options


def generate_code(sections):
    rows = list()
    rows.append(Row(code="import configparser"))
    rows.append(Row(code="import os"))
    rows.append(Row(code="\n"))

    rows.append(Row(code="class Configuration:"))
    rows.append(Row(intents=1, code="def __init__(self, config_file_path=''):"))
    rows.append(Row(intents=2, code="config_parser = self.read_configuration_file(config_file_path)"))
    rows.append(Row(intents=2, code="sections = ["))
    for section in sections:
        rows.append(Row(intents=3, code="{0},".format(section)))
    rows.append(Row(intents=2, code="]"))
    rows.append(Row(intents=2, code="self.check_sections(config_parser, sections)"))
    rows.append(Row(intents=2, code="self.set_options(config_parser, sections)"))
    rows.append(Row(code="\n", line_break=False))

    rows.append(Row(intents=1, code="def set_options(self, config_parser, sections):"))
    rows.append(Row(intents=2, code="for section in sections:"))
    rows.append(Row(intents=3, code="for option in section['options']:"))
    rows.append(Row(intents=4, code="if not config_parser.has_option(section['section'], option['option']):"))
    rows.append(Row(intents=5,
                    code="raise Exception('Option {0} is not in section {1}!'.format(option['option'], section['section']))"))
    rows.append(Row(intents=4,
                    code="setattr(self, option['option'], config_parser.get(section['section'], option['option'], fallback=option['fallback']))"))
    rows.append(Row(code="\n", line_break=False))

    rows.append(Row(intents=1, code="@staticmethod"))
    rows.append(Row(intents=1, code="def read_configuration_file(config_file_path):"))
    rows.append(Row(intents=2, code="if not os.path.isfile(config_file_path):"))
    rows.append(Row(intents=3, code='raise Exception("The config file does not exist!")'))
    rows.append(Row(intents=2, code="config_parser = configparser.ConfigParser()"))
    rows.append(Row(intents=2, code="config_parser.read(config_file_path)"))
    rows.append(Row(intents=2, code="return config_parser"))

    rows.append(Row(code="\n", line_break=False))

    rows.append(Row(intents=1, code="@staticmethod"))
    rows.append(Row(intents=1, code="def check_sections(config_parser, sections):"))
    rows.append(Row(intents=2, code="for section in sections:"))
    rows.append(Row(intents=3, code="if not config_parser.has_section(section['section']):"))
    rows.append(Row(intents=4, code="raise Exception('Section {0} is not in config file!'.format(section['section']))"))

    return join_rows(rows)


def read_config(args):
    config_file = args.config
    config_parser = configparser.ConfigParser()
    if not os.path.isfile(config_file):
        raise Exception("The config file does not exist! " + config_file)
    config_parser.read(config_file)
    return config_parser


def get_sections(config_parser):
    sections = []
    for section in config_parser.sections():
        options = config_parser.items(section)
        option_dictionaries = []
        for (key, value) in options:
            option_dictionaries.append(dict(option=key, fallback=value))
        sections.append(dict(section=section, options=option_dictionaries))
    return sections


def main_function():
    parser = argparse.ArgumentParser(description='Python configuration class from Config file.', )
    parser.add_argument(
        '-c',
        '--config',
        action='store',
        dest='config',
        required=True,
        help='The path to the configuration file.'
    )
    parser.add_argument(
        '-o',
        '--out',
        action='store',
        dest='out_file',
        required=False,
        help='The output filename, the default is to standard out. (Ex. -o Configuration.py)'
    )

    args = parser.parse_args()
    config_parser = read_config(args)
    sections = get_sections(config_parser)
    code = generate_code(sections)
    if args.out_file is not None:
        sys.stdout = open(args.out_file, 'w')
    print(code)


if __name__ == "__main__":
    main_function()
