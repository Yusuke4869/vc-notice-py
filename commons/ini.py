import os
import sys
import configparser

import commons.errors as errors

cwd = os.getcwd()
config_file_path = os.path.expandvars(f"{cwd}/config.ini")

"""
All keys in config.ini file.
config.iniファイルの全てのキー.
"""
default_keys = [
    "env-var",
    "discordbot_token",
    "prefix",
    "language"
]

"""
Default values in config.ini file.
config.iniファイルの既定値.
"""
default_settings = {
    "env-var": True,
    "discordbot_token": "Your TOKEN",
    "prefix": "v!",
    "language": "en"
}

class Config:

    def __init__(self) -> None:
        self.config_ini = configparser.ConfigParser()

    def init(self) -> None:
        self.config_ini = configparser.ConfigParser()

    def set_default_data(self) -> None:
        self.init()
        self.config_ini["Settings"] = default_settings

        try:
            with open(config_file_path, "w") as f:
                self.config_ini.write(f)
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

    def fix(self) -> None:
        self.init()
        settings_data = default_settings
        values = self.read_config()

        for key in default_keys:
            try:
                value = values.get("Settings", key)
            except configparser.NoOptionError as e:
                """
                No key.
                キーが存在しない.
                """
                value = None
            except Exception as e:
                errors.critical_print(e)
                sys.exit(1)

            if value != None:
                settings_data[key] = value

        self.config_ini["Settings"] = settings_data

        try:
            with open(config_file_path, "w") as f:
                self.config_ini.write(f)
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

    def read_config(self):
        self.init()
        if os.path.exists(config_file_path):
            self.config_ini.read(config_file_path)
        else:
            self.set_default_data()
            self.config_ini.read(config_file_path)
        return self.config_ini

    """
    Get value from config.ini file.
    config.iniファイルから値を取得します.
    """
    def get_value(self, key, section="Settings") -> str:
        self.init()
        config = self.read_config()

        try:
            value = config.get(str(section), str(key))
        except configparser.NoOptionError as e:
            """
            No key.
            キーが存在しない.
            """
            errors.error_print(e)
            self.fix()
            return None
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)
        else:
            return value