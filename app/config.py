import configparser


class Config:
    def __call__(self, section: str, value: str):
        config_obj = configparser.ConfigParser()
        all_config_files = [
            './config.ini'
        ]
        config_obj.read(all_config_files)
        return config_obj.get(section, value)


config = Config()
