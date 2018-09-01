from apollo.models import Guild


class OnGuildRemove:

    def __init__(self, bot):
        self.bot = bot


    async def on_guild_remove(self, guild):
        session = self.bot.Session()
        self.bot.cache.delete_prefix(guild.id)
        session.query(Guild).filter_by(id=guild.id).delete()
        session.commit()
