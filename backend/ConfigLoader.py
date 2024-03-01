from configparser import ConfigParser

class ConfigLoader:
    def __init__(self, config_file_path):
        self.config = ConfigParser()
        self.config.read(config_file_path)
        
    def get_host(self):
        return self.config['DATABASE']['host']

    def get_user(self):
        return self.config['DATABASE']['user']

    def get_password(self):
        return self.config['DATABASE']['password']

    def get_database(self):
        return self.config['DATABASE']['database']
    
    def get_port(self):
        return self.config['DATABASE']['port']
