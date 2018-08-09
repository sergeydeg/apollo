from apollo.queries import delete_event_channel


class OnGuildChannelDelete:

    def __init__(self, bot):
        self.bot = bot


    async def on_guild_channel_delete(self, channel):
        session = self.bot.Session()
        delete_event_channel(session, channel.id)
        session.commit()
        session.close()
