from apollo.models import EventChannel, Guild, User


class SyncModels:

    def __init__(self, bot):
        self.bot = bot
        self.session = bot.Session()


    def call(self):
        self._sync_event_channels()
        self._sync_guilds()
        self._sync_users()
        self.session.commit()


    def _sync_event_channels(self):
        for event_channel in self.session.query(EventChannel).all():
            if not self.bot.get_channel(event_channel.id):
                self.session.delete(event_channel)


    def _sync_guilds(self):
        for guild in self.session.query(Guild).all():
            if not self.bot.get_guild(guild.id):
                self.session.delete(guild)


    def _sync_users(self):
        for user in self.session.query(User).all():
            if not self.bot.get_user(user.id):
                self.session.delete(user)
