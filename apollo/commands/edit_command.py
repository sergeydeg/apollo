from discord.ext import commands

from apollo.permissions import HavePermission
from apollo.models import Event
from apollo.queries import find_or_create_guild
from apollo.translate import t


class EditCommand(commands.Cog):
    def __init__(
        self,
        bot,
        list_events,
        sync_event_channels,
        event_selection_input,
        title_input,
        description_input,
        capacity_input,
        start_time_input,
        event_list_embed,
    ):
        self.bot = bot
        self.list_events = list_events
        self.sync_event_channels = sync_event_channels
        self.event_selection_input = event_selection_input
        self.title_input = title_input
        self.description_input = description_input
        self.capacity_input = capacity_input
        self.start_time_input = start_time_input
        self.event_list_embed = event_list_embed

    @commands.command()
    @commands.guild_only()
    async def edit(self, ctx):
        """Update an already created event"""
        self.sync_event_channels.call(ctx.guild.id)

        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)

        await ctx.author.send(t("event.query_events_list"))
        event = await self.event_selection_input.call(
            ctx.author, ctx.author.dm_channel, guild, 'editable'
        )

        with self.bot.scoped_session() as session:
            channel = self.bot.get_channel(event.event_channel_id)

        await ctx.author.send(t("event.update_title_prompt"))
        title = await self.title_input.call(ctx.author, ctx.author.dm_channel)

        await ctx.author.send(t("event.update_description_prompt"))
        description = await self.description_input.call(
            ctx.author, ctx.author.dm_channel
        )

        await ctx.author.send(t("event.capacity_prompt"))
        capacity = await self.capacity_input.call(ctx.author, ctx.author.dm_channel)

        await ctx.author.send(t("event.update_time_prompt"))
        start_time = await self.start_time_input.call(
            ctx.author, ctx.author.dm_channel, event.time_zone, update=True
        )

        await ctx.author.send(t("event.updated"))

        with self.bot.scoped_session() as session:
            event = session.query(Event).filter_by(id=event.id).first()
            # Edit fields if the user wants them changed
            if title.lower() != "none":
                event.title = title
            if description.lower() != "none":
                event.description = description
            if capacity:
                event.capacity = capacity
            if start_time:
                event.start_time = start_time
            session.commit()

            events = (
                session.query(Event)
                .filter_by(event_channel_id=event.event_channel_id)
                .all()
            )

        await self.list_events.call(events, channel)
