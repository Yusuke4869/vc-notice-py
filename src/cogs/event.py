from discord.ext import commands
import commons.errors as errors

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            self.bot.dispatch("help", "help", message.guild.id, message.channel)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @ping.error
    async def ping_error(self, ctx, error):
        errors.error_print(error)

def setup(bot):
    bot.add_cog(Help(bot))