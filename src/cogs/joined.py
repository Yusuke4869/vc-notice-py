import discord
from discord.errors import Forbidden
from discord.ext import commands

from commons.ini import Config
import commons.errors as errors

config = Config()

class Joined(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        default_prefix = config.get_value("prefix")
        embed = discord.Embed(title="Hi, there👋", description="Thanks for inviting this bot", color=0xffa500)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="How to use", value=f"Type {default_prefix}help", inline=False)
        embed.add_field(name="How to see overview of this bot", value=f"Type {default_prefix}overview", inline=False)
        embed.set_footer(text="This is VC Notice Bot")

        for channel in guild.text_channels:
            try:
                await channel.send(embed=embed)
                break
            except Forbidden:
                pass
            except Exception as e:
                errors.error_print(e)

def setup(bot):
    bot.add_cog(Joined(bot))