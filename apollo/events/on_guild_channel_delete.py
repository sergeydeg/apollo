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
                self._update_cache(event_channel)
                session.delete(event_channel)


    def _update_cache(self, event_channel):
        self.bot.cache.delete_event_channel(event_channel.id)
        for event in event_channel.events:
            self.bot.cache.delete_event(event.message_id)
