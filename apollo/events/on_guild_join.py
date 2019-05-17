from discord.ext import commands

from apollo.queries import find_or_create_guild


class OnGuildJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with self.bot.scoped_session() as session:
            find_or_create_guild(session, guild.id)

        # Add entry for guild prefix in the cache
        self.bot.cache.update_prefix(guild.id, None)
