from discord.ext import commands

from apollo.queries import find_event_channel


class OnGuildChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        with self.bot.scoped_session() as session:
            event_channel = find_event_channel(session, channel.id)

            if event_channel:
                session.delete(event_channel)
