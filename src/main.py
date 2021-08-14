import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

from commons.ini import Config
from commons.log import Log
import commons.errors as errors
import commons.functions as func

from src.data.guilds import GuildData

config = Config()
log = Log()
guild = GuildData()

cogs = [
    "src.cogs.error",
    "src.cogs.embed",
    "src.cogs.event",
    "src.cogs.help",
    "src.cogs.joined",
    "src.cogs.notices",
    "src.cogs.sending",
    "src.cogs.settings",
]

async def prefix(bot, message):
    prefix = guild.get_prefix(str(message.guild.id))
    if not prefix:
        prefix = config.get_value("prefix")
    return prefix

class VCNotice(commands.Bot):

    def __init__(self, prefix):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=prefix, 
            intents=intents,
            help_command=None,
            case_insensitive=True,
            activity=discord.Game(name="Type v!help for help", type=1)
        )

        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                errors.error_print(e)

    async def on_ready(self):
        print("".join(["-" for i in range(50)]))
        print("""\
This is a DiscordBot using discord.py.

When someone joins or leaves a voice channel, the bot notifies a text channel of this activity.
Also, When someone starts or ends \"Screen Share\", the bot does.""")
        print("".join(["-" for i in range(50)]))
        log.print_info_log(f"Logged in as {self.user.name}")
        #await self.change_presence(activity=discord.Game(name="Type v!help for help", type=1))

"""
Run the bot.
Botの起動.
"""
def run():
    bot = VCNotice(prefix=prefix)
    TOKEN = None

    """
    Whether to use env.
    環境変数を使うかどうか.
    """
    env = config.get_value("env-var")
    env = func.str_to_bool(env)

    """
    Get TOKEN from env.
    環境変数からTOKEN取得.
    """
    TOKEN_env = os.environ.get("TOKEN")

    """
    Get TOKEN from .ini file.
    .iniファイルからTOKEN取得.
    """
    TOKEN_ini = config.get_value("discordbot_token")

    if TOKEN_ini != "Your TOKEN":
        TOKEN = TOKEN_ini

    if TOKEN_env != None and env == True:
        TOKEN = TOKEN_env

    error = False

    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        """
        Invalid TOKEN.
        無効なTOKEN.
        """
        error = True
    except Exception as e:
        errors.critical_print(e)
        return

    try:
        if error:
            raise errors.TokenNotFoundError("Token is not Found")
    except errors.TokenNotFoundError as e:
        errors.critical_print(e)
        return