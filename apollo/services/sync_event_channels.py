from apollo.models import EventChannel


class SyncEventChannels:
    def __init__(self, bot):
        self.bot = bot

    def call(self, session, discord_guild_id):
        event_channels = session.query(EventChannel).filter_by(
            guild_id=discord_guild_id
        )

        for event_channel in event_channels:
            if not self.bot.get_channel(event_channel.id):
                session.delete(event_channel)
