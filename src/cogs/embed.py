import discord
from discord.ext import commands

import commons.functions as func
from src.data.messages import Messages
import commons.errors as errors

messages = Messages()

class Embed(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """
    Create Embed Message.
    --- about activity var ---
        int activity
        1: joined
        2: leaved
        3: started_streaming
        4: ended_streaming
        5: joined_afk
    --- activity変数について ---
        整数型
        1: 参加
        2: 退出
        3: 配信開始
        4: 配信終了
        5: AFKに参加
    """
    @commands.Cog.listener()
    async def on_create_activity_embed(self, activity: int, member, time, channelname: str):
        activity = func.str_to_int(activity)
        if not activity:
            try:
                raise errors.BotError("activity var is not int type")
            except errors.BotError as e:
                errors.error_print(e)
                return

        if activity < 1 or activity > 5:
            try:
                raise errors.BotError("activity var is more than 5 or under 1")
            except errors.BotError as e:
                errors.error_print(e)
                return

        guild_id = member.guild.id

        title_data = messages.get_current_language_notice_message(str(guild_id), "title")
        description_data = messages.get_current_language_notice_message(str(guild_id), "description")

        if title_data == False or description_data == False:
            try:
                raise errors.BotError("Keyerror of dict")
            except errors.BotError as e:
                errors.error_print(e)
                return

        activity_title = None
        activity_description = None
        color = None

        if activity == 1:
            activity_title = title_data["joined"]
            activity_description = description_data["joined"].replace("${CHANNELNAME}", str(channelname), 1)
            color = 0x008000
        elif activity == 2:
            activity_title = title_data["leaved"]
            activity_description = description_data["leaved"].replace("${CHANNELNAME}", str(channelname), 1)
            color = 0xff0000
        elif activity == 3:
            activity_title = title_data["started_streaming"]
            activity_description = description_data["started_streaming"]
            color = 0x008000
        elif activity == 4:
            activity_title = title_data["ended_streaming"]
            activity_description = description_data["ended_streaming"]
            color = 0xff0000
        elif activity == 5:
            activity_title = title_data["joined_afk"]
            activity_description = description_data["joined_afk"]
            color = 0x000000
        else:
            return

        embed = discord.Embed(title=activity_title, color=color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=member.display_name, value=activity_description, inline=False)
        embed.set_footer(text=time)
        self.bot.dispatch("sending", guild_id, embed)

def setup(bot):
    bot.add_cog(Embed(bot))