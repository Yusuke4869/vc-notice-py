from typing import Union
import sys

from src.data.json import Json
from commons.ini import Config
import commons.errors as errors

json = Json()
config = Config()

class GuildData:

    def __init__(self):
        pass

    def create_guild_data(self, guild_id: str) -> bool:
        prefix = config.get_value("prefix")
        language = config.get_value("language")
        data = {
            "prefix": prefix,
            "language": language,
            "webhookurl": ""
        }

        result = json.update_guild_data(guild_id, data)
        if result:
            return True
        else:
            return False

    def get_guild_data(self, guild_id: str) -> Union[dict, bool]:
        guilds_data = json.get_data(1)
        try:
            guild_data = guilds_data[str(guild_id)]
            return guild_data
        except KeyError:
            result = self.create_guild_data(guild_id)
            if not result:
                return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

        new_guilds_data = json.get_data(1)
        try:
            guild_data = new_guilds_data[str(guild_id)]
            return guild_data
        except KeyError:
            return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)        

    def get_prefix(self, guild_id: str) -> Union[str, bool]:
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False
        return guild_data["prefix"]

    def get_language(self, guild_id: str) -> Union[str, bool]:
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False
        return guild_data["language"]

    def get_webhookurl(self, guild_id: str) -> Union[str, bool]:
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False
        return guild_data["webhookurl"]

    def change_prefix(self, guild_id: str, prefix: str) -> bool:
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False

        guild_data["prefix"] = prefix
        result = json.update_guild_data(guild_id, guild_data)
        if result:
            return True
        else:
            return False

    def change_language(self, guild_id: str, language: str) -> bool:
        language = json.language(language)
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False

        guild_data["language"] = language
        result = json.update_guild_data(guild_id, guild_data)
        if result:
            return True
        else:
            return False

    def change_webhookurl(self, guild_id: str, webhookurl: str) -> bool:
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            return False

        guild_data["webhookurl"] = webhookurl
        result = json.update_guild_data(guild_id, guild_data)
        if result:
            return True
        else:
            return False