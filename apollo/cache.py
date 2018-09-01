from apollo.models import Guild


class Cache:

    def __init__(self, Session):
        self.Session = Session
        self.prefixes = {}


    def get_prefix(self, guild_id):
        return self.prefixes[guild_id]


    def load_prefixes(self):
        session = self.Session()
        guilds = session.query(Guild).all()
        for guild in guilds:
            self.prefixes[guild.id] = guild.prefix


    def update_prefix(self, guild_id, prefix):
        self.prefixes[guild_id] = prefix
