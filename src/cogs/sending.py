from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

from src.data.guilds import GuildData
import commons.errors as errors

guild = GuildData()

class Sending(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """
    Send notice using Webhook.
    Webhookを使用して通知を送信.
    """
    @commands.Cog.listener()
    async def on_sending(self, guildid, embed):
        webhook_url = guild.get_webhookurl(str(guildid))
        if not webhook_url:
            try:
                raise errors.BotError("There was not the url of webhook of the guild")
            except errors.BotError as e:
                errors.error_print(e)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
            try:
                await webhook.send(embed=embed, avatar_url=self.bot.user.avatar_url)
            except Exception as e:
                errors.error_print(e)

def setup(bot):
    bot.add_cog(Sending(bot))