# ConfigValidator
ConfigValidator should help to reduce the toil of validating the user input of configuration files. 
It automatically generates a Configuration class out of your configuration file (.ini) and checks if a user has set all parameters in his own file.

## Usage
Generate a python Configuration class from the configuration file (.ini) to validate and access the configuration parameters.  

![Alt text](img/ConfigValidator.png)

 1. Create a configuration file (.ini) and add the parameters you need for your application.
    Example config.ini:
    ```bash
    [SERVER]
    Name=SuperServer
    Host=127.0.0.1
    ```
 2. Generate your python Configuration class from your config.ini file.
    ```bash
    python3 config_validator.py -c config.ini -o configuration.py
    ```
    
    The resulting configuration.py will look like the following python script and is ready to use. 
    
    ```python
    import configparser
    import os
    
    
    class Configuration:
        def __init__(self, config_file_path=''):
            config_parser = self.read_configuration_file(config_file_path)
            sections = [
                {'options': [{'fallback': 'SuperServer', 'option': 'name'}, {'fallback': '127.0.0.1', 'option': 'host'}], 'section': 'SERVER'},
            ]
            self.check_sections(config_parser, sections)
            self.set_options(config_parser, sections)
    
        def set_options(self, config_parser, sections):
            for section in sections:
                SectionClass = type(section['section'], (), {})
                section_class = SectionClass()
                for option in section['options']:
                    if not config_parser.has_option(section['section'], option['option']):
                        raise Exception('Option {0} is not in section {1}!'.format(option['option'], section['section']))
                    setattr(section_class, option['option'], config_parser.get(section['section'], option['option'], fallback=option['fallback']))
                setattr(self, section['section'], section_class)
    
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
    ```
    
 3. Well, everything is all ready done for you and the Configuration class is ready to us.
    Now you are able to simply access the configuration parameters in an object oriented way.
    And if the user of your application has missed a parameter in his configuration file he will get an exception. 
    
    Example usage:
    ```python
    import os
    from configuration import Configuration
    
    directory, _ = os.path.split(os.path.abspath(__file__))
    configuration = Configuration(config_file_path=directory + '/config.ini')
    
    print(configuration.SERVER.name, configuration.SERVER.host)
    # output: SuperServer 127.0.0.1
    ```
   

 
### config_validator.py
```
usage: config_validator.py [-h] -c CONFIG [-o OUT_FILE]

Python configuration class from Config file.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The path to the configuration file.
  -o OUT_FILE, --out OUT_FILE
                        The output filename, the default is to standard out.
                        (Ex. -o Configuration.py)
```

## Notes
As you might have seen the access to a option in your config file looks somehow like the following:
```python
configuration.SERVER.name
```
I am aware that this is against the Law of Demeter (LoD) but it should simply represent sections and options in config files (.ini). 
Pseudo notation: ```{object name}.{section}.{option}``` 
 
