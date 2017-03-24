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
 
