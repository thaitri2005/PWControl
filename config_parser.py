from configparser import ConfigParser
def GetConfigPaster(section, key):
    '''
    Get a config parser value in the config.ini file.
    Raise Excepton if can't find path to the file
    
    section(string): the section of the needed config paster
    key(string): the individual key of the config paster value
    
    Returns: string
    '''
    config_file_path = 'config.ini'
    config = ConfigParser()
    try:
        with open(config_file_path) as conf:
            config.read(config_file_path)
            return config.get(section, key)
    except (OSError, IOError) as e:
        raise Exception("Couldn't find path to config.ini.") from e
    
def ChangeConfigPasterValue(section, key, value):
    '''
    Change a config parser value in the config.ini file.
    Raise Excepton if can't find path to the file
    
    section(string): the section of the needed config paster
    key(string): the individual key of the config paster value
    value(string): the value need to be changed
    
    Returns: None
    '''
    config_file_path = 'config.ini'
    config = ConfigParser()
    try:
        with open(config_file_path) as conf:
            config.read(config_file_path)
            config[section][key] = value
            with open(config_file_path, 'w') as conf:
                config.write(conf)
    except (OSError, IOError) as e:
        raise Exception("Couldn't find path to config.ini.") from e