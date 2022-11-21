import configparser

"""A static config parser"""

class StaticConfigParser():
    config_file_path = 'config.ini'
    config = configparser.ConfigParser()

    try:
        with open(config_file_path) as f:
            config.read(config_file_path)
    except (OSError, IOError) as e:
        raise Exception("Couldn't find path to config.ini.") from e
    
    @staticmethod
    def get(parent, child):
        return StaticConfigParser.config.get(parent, child)

