from discord.ext import commands

from apollo.permissions import HavePermission
from apollo.services import SendChannelSelect
from apollo.models import Event, EventChannel
from apollo.queries import find_or_create_guild
from apollo.queries import find_or_create_user
from apollo.translate import t


class EventCommand(commands.Cog):
    MAX_CAPACITY = 40
    MAX_DESC_LENGTH = 1000
    MAX_TITLE_LENGTH = 200

    TIME_ZONE_INVITE = "https://discord.gg/PQXA2ys"

    def __init__(
        self,
        bot,
        list_events,
        sync_event_channels,
        capacity_input,
        description_input,
        start_time_input,
        event_time_zone_input,
        title_input,
    ):
        self.bot = bot
        self.list_events = list_events
        self.sync_event_channels = sync_event_channels
        self.capacity_input = capacity_input
        self.description_input = description_input
        self.start_time_input = start_time_input
        self.event_time_zone_input = event_time_zone_input
        self.title_input = title_input

    @commands.command()
    @commands.guild_only()
    async def event(self, ctx):
        """Create a new event"""
        # Clean up event channels that may have been deleted
        # while the bot was offline.
        self.sync_event_channels.call(ctx.guild.id)

        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)

        if not HavePermission(ctx.author, guild).event():
            return await ctx.send(t("error.missing_permissions"))

        with self.bot.scoped_session() as session:
            event_channels = (
                session.query(EventChannel).filter_by(guild_id=ctx.guild.id).all()
            )
            user = find_or_create_user(session, ctx.author.id)

        event = Event()
        event.title = await self.title_input.call(ctx)
        event.description = await self.description_input.call(ctx)
        event.organizer = user
        event.capacity = await self.capacity_input.call(ctx)
        event.event_channel = await self._get_event_channel(ctx, event_channels)

        event.time_zone = await self.event_time_zone_input.call(ctx)
        event.start_time = await self.start_time_input.call(ctx, event.time_zone)

        channel = self.bot.get_channel(event.event_channel.id)
        await ctx.author.send(t("event.created").format(channel.mention))

        with self.bot.scoped_session() as session:
            session.add(event)

        with self.bot.scoped_session() as session:
            events = (
                session.query(Event)
                .filter_by(event_channel_id=event.event_channel_id)
                .all()
            )

        await self.list_events.call(events, channel)

    async def _choose_event_channel(self, ctx, event_channels):
        message = await SendChannelSelect(
            self.bot, ctx.author.dm_channel, event_channels
        ).call()

        def reaction_check(reaction, user):
            return (message.id == reaction.message.id) and (user.id == ctx.author.id)

        reaction, _ = await self.bot.wait_for(
            "reaction_add", check=reaction_check, timeout=90.0
        )

        return event_channels[int(reaction.emoji[0]) - 1]

    async def _get_event_channel(self, ctx, event_channels):
        """Find or create the event channel for the current guild"""
        if len(event_channels) == 1:
            return event_channels[0]
        elif len(event_channels) > 1:
            return await self._choose_event_channel(ctx, event_channels)
        else:
            channel = await self.bot.create_discord_event_channel(
                ctx.guild, ctx.channel.category
            )
            return EventChannel(id=channel.id, guild_id=ctx.guild.id)
