from apollo.models import EventChannel, Guild, User
from apollo.queries import find_or_create_guild


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
        guild_models = self.session.query(Guild).all()

        # Delete guilds that aren't around anymore
        for guild in guild_models:
            if not self.bot.get_guild(guild.id):
                self.session.delete(guild)

        # Create guilds that were added while offline
        for guild in self.bot.guilds:
            if guild not in (guild_model.id for guild_model in guild_models):
                find_or_create_guild(self.session, guild.id)


    def _sync_users(self):
        for user in self.session.query(User).all():
            if not self.bot.get_user(user.id):
                self.session.delete(user)
