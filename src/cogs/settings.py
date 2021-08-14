import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

from src.data.guilds import GuildData
import commons.errors as errors

guild = GuildData()

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def set(self, ctx):
        self.bot.dispatch("help", "settings", ctx.guild.id, ctx.channel)

    @set.command()
    async def prefix(self, ctx, prefix):
        result = guild.change_prefix(str(ctx.guild.id), prefix)
        if result:
            await ctx.send(f"Prefix changed to {prefix}")
        else:
            await ctx.send("Could not change prefix")

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Need new prefix")
            return

        errors.error_print(error)

    @set.command()
    async def language(self, ctx, language):
        result = guild.change_language(str(ctx.guild.id), language)
        if result:
            await ctx.send(f"Language changed to {language}")
        else:
            await ctx.send("Could not change language")

    @language.error
    async def language_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Need language name")
            return

        errors.error_print(error)

    @set.command()
    async def channel(self, ctx):
        webhook_url = guild.get_webhookurl(str(ctx.guild.id))
        if webhook_url:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
                try:
                    await webhook.delete()
                except discord.NotFound:
                    pass
                except discord.Forbidden:
                    await ctx.send("Could not delete old webhook (Reason: I do not have permissions)")
                except Exception as e:
                    errors.error_print(e)
                    await ctx.send("Could not delete old webhook")

        webhook = await ctx.channel.create_webhook(name="VC Notice")
        result = guild.change_webhookurl(str(ctx.guild.id), webhook.url)
        if result:
            await ctx.send("Notice channel changed to this channel")
        else:
            await ctx.send("Could not change notice channel")

    @channel.error
    async def channel_error(self, ctx, error):
        errors.error_print(error)

def setup(bot):
    bot.add_cog(Settings(bot))