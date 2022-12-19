import os.path
from configparser import ConfigParser
from typing import Dict


class ConfigConverter:
    """Wrapper around ConfigParser. Used to write and read config files for different users."""

    def __init__(self, username: str) -> None:
        self.username = username
        config_path = "./settings/config_" + username + ".ini"
        default_path = "./settings/config_sample.ini"
        self.config = ConfigParser()
        self.user_exists = False
        if os.path.exists(config_path):
            self.config.read(config_path)
            self.user_exists = True
        else:
            print("Configuration for user not exists, create a new user")
            self.config.read(default_path)

    def generate_conn_settings(self, password: str, dbname: str) -> None:
        self.config.set("database", "user", self.username)
        self.config.set("database", "password", password)
        self.config.set("database", "dbname", dbname)

    def save_conn_settings(self) -> None:
        with open("./settings/config_" + self.username + ".ini", "w") as configfile:
            self.config.write(configfile)

    def generate_conn_settings_sample(
        self, username: str, password: str, dbname: str
    ) -> None:
        self.config.set("database", "user", username)
        self.config.set("database", "password", password)
        self.config.set("database", "dbname", dbname)
        with open("./settings/config_" + self.username + ".ini", "w") as configfile:
            self.config.write(configfile)

    def get_conn_settings(self) -> Dict[str, str]:
        # convert list of tuples to dict
        connection_settings: Dict[str, str] = {}
        if self.config.has_section("database"):
            params = self.config.items("database")
            for key, value in params:
                if key == "schema":
                    connection_settings["options"] = f"-c search_path={value}"
                else:
                    connection_settings[key] = value
        return connection_settings

    def get_jdbc_path(self) -> str:
        if self.config.has_section("jdbc"):
            params = self.config.items("jdbc")
            for key, value in params:
                if key == "driver":
                    return value
        return ""

    def get_data_path(self) -> str:
        if self.config.has_section("data"):
            params = self.config.items("data")
            for key, value in params:
                if key == "path":
                    return value
        return ""

    def set_default_path(self, path: str) -> None:
        self.config.set("database", "default_filepath", path)
        with open("./settings/config_" + self.username + ".ini", "w") as configfile:
            self.config.write(configfile)
