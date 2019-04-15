from discord.ext import commands

from apollo.models import Guild


class OnGuildRemove(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        session = self.bot.Session()
        self.bot.cache.delete_prefix(guild.id)
        session.query(Guild).filter_by(id=guild.id).delete()
        session.commit()
