from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, CommandNotFound):
            return

        raise error

def setup(bot):
    bot.add_cog(Error(bot))