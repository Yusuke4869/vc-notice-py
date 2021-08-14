import os
import json
import sys

import commons.functions as func
import commons.errors as errors

cwd = os.getcwd()
guildsdata_file_path = os.path.expandvars(f"{cwd}/data/guilds_data.json")
help_file_path = os.path.expandvars(f"{cwd}/data/help_messages.json")
notice_file_path = os.path.expandvars(f"{cwd}/data/notice_messages.json")

class Json:

    def __init__(self) -> None:
        pass

    def language(self, lang: str) -> str:
        lang = str(lang).lower()
        if lang in ["en", "english", "英語"]:
            return "english"
        elif lang in ["ja", "japanese", "日本語"]:
            return "japanese"
        else:
            return "english"

    def check_guildsdata_file(self) -> None:
        if not os.path.exists(guildsdata_file_path):
            with open(guildsdata_file_path, mode="w") as f:
                f.write("{}")

    """
    Get data.
    --- about file var ---
        int type
        1: guilds_data.json
        2: notice_messages.json
        3: help_messages.json
    データを取得します.
    --- file変数について ---
        整数型
        1: guilds_data.json
        2: notice_messages.json
        3: help_messages.json
    """
    def get_data(self, file: int) -> dict:
        file = func.str_to_int(file)
        file_path = None

        if not file:
            return {}

        if file == 1:
            self.check_guildsdata_file()
            file_path = guildsdata_file_path
        elif file == 2:
            file_path = notice_file_path
        elif file == 3:
            file_path = help_file_path
        else:
            return {}

        try:
            with open(file_path, mode="rt", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            errors.critical_print(e)
            sys.exit(1)

    """
    Update data of a guild.
    ギルドデータを更新します.
    """
    def update_guild_data(self, guild_id: str, data: dict) -> bool:
        guilds_data = self.get_data(1)
        guilds_data[str(guild_id)] = data

        try:
            with open(guildsdata_file_path, mode="w", encoding="utf-8") as f:
                json.dump(guilds_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            errors.error_print(e)
            return False