from discord.ext import commands
from datetime import datetime, timedelta, timezone

"""
Set TimeZone of UTC and JST.
UTCとJSTのタイムゾーン設定.
"""
UTC = timezone.utc
JST = timezone(timedelta(hours=+9), "JST")

class VoiceState(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        ----- now (var) -----
        Get the current time.
            ----- TIMEZONE -----
            Default TimeZone is Japan Standard Time(JST).
            If you want to use UTC time, you need to change "JST" to "UTC".
            If you want to use current TimeZone, you need to delete "JST".

            You can set other TimeZone.
            If want to set UTC-8, you need to change "JST" to "timezone(timedelta(hours=-8))".

            ----- DATE FORMAT -----
            Default date format is YYYY/MM/DD. (Default time format is hh/mm/ss.)
            If you want to use the format MM/DD/YYYY, you need to change "%Y/%m/%d" to "%m/%d/%Y".
            If you want to use the format DD/MM/YYYY, you need to change "%Y/%m/%d" to "%d/%m/%Y".

            You can set other format.

        ----- now (変数) -----
        現在時刻を取得します.
            ----- タイムゾーン -----
            既定のタイムゾーンは日本標準時(JST)です.
            世界協定時を使用したい場合, "JST"を"UTC"に変更する必要があります.
            現在のタイムゾーンを使用したい場合, "JST"を削除する必要があります.

            その他のタイムゾーンを設定することも可能です.
            UTC-8に設定したい場合, "JST"を"timezone(timedelta(hours=-8))"に変更する必要があります.

            ----- 日付形式 ----
            デフォルトの日付形式は YYYY/MM/DD です. (既定の時間形式は hh/mm/ss です.)
            MM/DD/YYYY 形式を使用したい場合, "%Y/%m/%d"を"%m/%d/%Y"に変更する必要があります.
            DD/MM/YYYY 形式を使用したい場合, "%Y/%m/%d"を"%d/%m/%Y"に変更する必要があります.

            その他の形式に設定することも可能です.

        ----- Default Code, 既定のコード -----
        now = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")
        """
        now = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")

        afk_channel = member.guild.afk_channel

        if afk_channel is None:
            """
            There is no afk channel in the guild.
            サーバーにAFKチャンネルが存在しない.
            """
            afk_channelid = 0
        else:
            afk_channelid = afk_channel.id

        if before.channel is None:
            """
            The user joined.
            参加.
            """
            self.bot.dispatch("create_activity_embed", 1, member, now, after.channel.name)
        elif after.channel is None:
            """
            The user leaved.
            退出.
            """
            self.bot.dispatch("create_activity_embed", 2, member, now, before.channel.name)
        elif after.channel.id == afk_channelid:
            if before.channel.id != after.channel.id:
                """
                The user joined the afk channel.
                AFKチャンネルへの参加.
                """
                self.bot.dispatch("create_activity_embed", 5, member, now, after.channel.name)
        elif not after.channel is None:
            if before.channel.id == after.channel.id:
                if before.self_stream != after.self_stream:
                    if after.self_stream:
                        """
                        The user started streaming.
                        配信開始.
                        """
                        self.bot.dispatch("create_activity_embed", 3, member, now, after.channel.name)
                    elif not after.self_stream:
                        """
                        The user ended streaming.
                        配信終了.
                        """
                        self.bot.dispatch("create_activity_embed", 4, member, now, before.channel.name)
            else:
                """
                The user joined other voice channel.
                別チャンネルへの参加.
                """
                self.bot.dispatch("create_activity_embed", 1, member, now, after.channel.name)

def setup(bot):
    bot.add_cog(VoiceState(bot))