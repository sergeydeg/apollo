from apollo.queries import find_event_channel


class OnGuildChannelDelete:

    def __init__(self, bot):
        self.bot = bot


    async def on_guild_channel_delete(self, channel):
        session = self.bot.Session()
        event_channel = find_event_channel(session, channel.id)

        if event_channel:
            self._update_cache(event_channel)
            session.delete(event_channel)

        session.commit()


    def _update_cache(self, event_channel):
        for event in event_channel.events:
            self.bot.cache.delete_event(event.message_id)
