from apollo.models import EventChannel


class SyncEventChannels:

    def __init__(self, bot):
        self.bot = bot
        self.session = bot.Session()


    def call(self):
        for event_channel in self._get_event_channels():
            channel = self.bot.get_channel(event_channel.id)
            if not channel:
                self.session.delete(event_channel)
        self.session.commit()


    def _get_event_channels(self):
        return self.session.query(EventChannel).all()
