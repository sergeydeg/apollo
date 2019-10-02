from discord.ext import commands

from apollo.models import Event
from apollo.queries import find_or_create_guild, responses_for_event
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
        selection_input,
        start_time_input,
        event_list_embed,
        update_event,
    ):
        self.bot = bot
        self.list_events = list_events
        self.sync_event_channels = sync_event_channels
        self.event_selection_input = event_selection_input
        self.title_input = title_input
        self.description_input = description_input
        self.capacity_input = capacity_input
        self.selection_input = selection_input
        self.start_time_input = start_time_input
        self.event_list_embed = event_list_embed
        self.update_event = update_event

    @commands.command()
    @commands.guild_only()
    async def edit(self, ctx):
        """Edit an existing command"""
        self.sync_event_channels.call(ctx.guild.id)

        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)

        # Needed to create event dm channel
        await ctx.author.create_dm()
        event = await self.event_selection_input.call(
            ctx.author, ctx.author.dm_channel, guild, "editable"
        )

        # Get Event Information
        description = event.description if event.description else "-"
        capacity = event.capacity if event.capacity else "-"
        selections = {
            t("event.properties.title"): event.title,
            t("event.properties.description"): description,
            t("event.properties.capacity"): capacity,
            t("event.properties.start_time"): event.start_time_string(),
        }

        selection = await self.selection_input.call(
            ctx.author,
            ctx.author.dm_channel,
            selections,
            title=t("event.query_event_fields"),
        )

        with self.bot.scoped_session() as session:
            event = session.query(Event).filter_by(id=event.id).first()

            if selection == 1:
                await ctx.author.send(t("event.title_prompt"))
                title = await self.title_input.call(ctx.author, ctx.author.dm_channel)
                event.title = title

            if selection == 2:
                await ctx.author.send(t("event.description_prompt"))
                description = await self.description_input.call(
                    ctx.author, ctx.author.dm_channel
                )
                event.description = description

            if selection == 3:
                await ctx.author.send(t("event.start_time_prompt"))
                capacity = await self.capacity_input.call(
                    ctx.author, ctx.author.dm_channel
                )
                event.capacity = capacity

            if selection == 4:
                await ctx.author.send(t("event.update_time_prompt"))
                start_time = await self.start_time_input.call(
                    ctx.author, ctx.author.dm_channel, event.time_zone
                )
                event.start_time = start_time

            responses = responses_for_event(session, event.id)

        channel = self.bot.get_channel(event.event_channel_id)
        await self.update_event.call(event, responses, channel)

        await ctx.author.send(t("event.updated"))
