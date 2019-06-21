from discord.ext import commands

from apollo.queries import find_or_create_guild
from apollo.translate import t


class PrefixCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix):
        """Update the server's command prefix"""
        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)
            guild.prefix = new_prefix
            session.add(guild)

        self.bot.cache.update_prefix(ctx.guild.id, new_prefix)
        await ctx.send(t("prefix.changed").format(new_prefix))

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(t("prefix.missing"))
