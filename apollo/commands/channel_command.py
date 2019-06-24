from discord.ext import commands

from apollo.can import Can
from apollo.models import EventChannel
from apollo.queries import find_or_create_guild
from apollo.queries import event_channel_count_for_guild
from apollo.translate import t


class ChannelCommand(commands.Cog):
    MAX_CHANNELS = 10

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

        with self.bot.scoped_session() as session:
            channel_count = event_channel_count_for_guild(session, ctx.guild.id)

        if channel_count >= self.MAX_CHANNELS:
            return await ctx.send(t("channel.channel_limit"))

        channel = await self.bot.create_discord_event_channel(
            ctx.guild, ctx.channel.category
        )
        event_channel = EventChannel(id=channel.id, guild_id=ctx.guild.id)

        with self.bot.scoped_session() as session:
            session.add(event_channel)
            events = event_channel.events

        await self.list_events.call(events, channel)
        await ctx.send(t("channel.channel_created").format(channel.mention))
