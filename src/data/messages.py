from typing import Union
import sys

from src.data.json import Json
import commons.errors as errors

json = Json()

class Messages:

    def __init__(self) -> None:
        pass

    """
    Get all guilds data. (bot has joined before)
    すべてのギルドのデータを取得します. (以前参加したことがある)
    """
    def get_guilds_data(self) -> dict:
        return json.get_data(1)

    """
    Get notice messages.
    通知メッセージを取得します.
    """
    def get_notice_messages(self) -> dict:
        return json.get_data(2)

    """
    Get help messages.
    ヘルプメッセージを取得します.
    """
    def get_help_messages(self) -> dict:
        return json.get_data(3)

    """
    Get notice messages in the language of the guild.
    ギルドの言語での通知メッセージを取得します.
    """
    def get_current_language_notice_messages(self, guild_id: str) -> Union[dict, bool]:
        guilds_data = self.get_guilds_data()
        try:
            guild_data = guilds_data[str(guild_id)]
        except KeyError:
            return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

        language = guild_data["language"]
        language = json.language(language)

        notice_data = self.get_notice_messages()
        messages = notice_data[language]
        return messages

    """
    Get notice message in the language of the guild.
    Need a key. (title or description)
    ギルドの言語での通知メッセージを取得します.
    キーが必要です. (title または description)
    """
    def get_current_language_notice_message(self, guild_id: str, key: str) -> Union[dict, bool]:
        messages = self.get_current_language_notice_messages(guild_id)
        if not messages:
            return False

        try:
            return messages[str(key)]
        except KeyError:
            return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

    """
    Get help messages in the language of the guild.
    ギルドの言語でのヘルプメッセージを取得します.
    """
    def get_current_language_help_messages(self, guild_id: str) -> Union[dict, bool]:
        guilds_data = self.get_guilds_data()
        try:
            guild_data = guilds_data[str(guild_id)]
        except KeyError:
            return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

        language = guild_data["language"]
        language = json.language(language)

        help_data = self.get_help_messages()
        keys = ["help", "overview", "settings"]
        messages = {}

        for key in keys:
            messages[key] = help_data[key][language]

        return messages

    """
    Get help message in the language of the guild.
    Need a key. (help or overview or settings)
    ギルドの言語でのヘルプメッセージを取得します.
    キーが必要です. (help または overview または settings)
    """
    def get_current_language_help_message(self, guild_id: str, key: str) -> Union[dict, bool]:
        messages = self.get_current_language_help_messages(guild_id)
        if not messages:
            return False

        try:
            return messages[str(key)]
        except KeyError:
            return False
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)