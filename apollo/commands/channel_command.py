from discord.ext import commands

from apollo.can import Can
from apollo.models import EventChannel
from apollo.queries import find_or_create_guild
from apollo.translate import t


class ChannelCommand(commands.Cog):

    def __init__(self, bot, list_events):
        self.bot = bot
        self.list_events = list_events


    @commands.command()
    @commands.guild_only()
    async def channel(self, ctx):
        """Create a new event channel"""
        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)

            if not Can(ctx.author, guild).channel():
                return await ctx.send(t("error.missing_permissions"))

            if guild.has_max_event_channels():
                return await ctx.send(t("channel.channel_limit"))

            channel = await self.bot.create_discord_event_channel(ctx.guild)
            event_channel = EventChannel(id=channel.id, guild_id=ctx.guild.id)
            session.add(event_channel)

            self.bot.cache.create_event_channel(event_channel.id)
            await self.list_events.call(event_channel)

            await ctx.send(
                t("channel.channel_created").format(channel.mention)
            )

