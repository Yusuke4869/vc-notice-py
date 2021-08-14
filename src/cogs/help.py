import discord
from discord.ext import commands

from src.data.messages import Messages
from src.data.guilds import GuildData
import commons.functions as func
import commons.errors as errors

messages = Messages()
guild = GuildData()

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        self.bot.dispatch("help", "help", ctx.guild.id, ctx.channel)

    @commands.Cog.listener()
    async def on_help(self, message_type, guild_id, channel):
        """
        ---about message_type var---
            ・help
            ・overview
            ・settings
        ---message_type変数について---
            ・help
            ・overview
            ・settings
        """
        help_data = messages.get_current_language_help_message(str(guild_id), message_type)
        prefix = guild.get_prefix(str(guild_id))
        if help_data == False or prefix == False:
            try:
                raise errors.BotError("Keyerror of dict")
            except errors.BotError as e:
                errors.error_print(e)
                return

        num = func.str_to_int(help_data["description_num"])
        if not num:
            try:
                raise errors.BotError("Value error")
            except errors.BotError as e:
                errors.error_print(e)
                return

        color = 0x000000

        embed = discord.Embed(title=help_data["title"], description=help_data["description"], color=color)
        embed.set_author(name="VC Notice", icon_url=self.bot.user.avatar_url)

        for i in range(1, num+1):
            data = help_data[str(i)]
            name = data["name"].replace("${PREFIX}", prefix)
            value = data["value"]
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=f"prefix: {prefix}")
        try:
            await channel.send(embed=embed)
        except Exception as e:
            errors.error_print(e)

    @commands.command()
    async def overview(self, ctx):
        self.bot.dispatch("help", "overview", ctx.guild.id, ctx.channel)

def setup(bot):
    bot.add_cog(Help(bot))