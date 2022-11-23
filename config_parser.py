from configparser import ConfigParser
'''
Get the config parser from the config.ini file.
Raise Excepton if can't find path to the file
'''
class MainConfigParser():
    config_file_path = 'config.ini'
    config = ConfigParser()
    try:
        with open(config_file_path) as conf:
            config.read(config_file_path)
    except (OSError, IOError) as e:
        raise Exception("Couldn't find path to config.ini.") from e
    
    @staticmethod
    def get(section, key):
        return MainConfigParser.config.get(section, key)