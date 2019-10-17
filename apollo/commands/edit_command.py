from discord.ext import commands

from apollo.models import Event
from apollo.queries import find_or_create_guild, responses_for_event
from apollo.translate import t


class EditCommand(commands.Cog):
    def __init__(
        self,
        bot,
        sync_event_channels,
        event_selection_input,
        title_input,
        description_input,
        capacity_input,
        selection_input,
        start_time_input,
        update_event,
        events_for_user,
    ):
        self.bot = bot
        self.sync_event_channels = sync_event_channels
        self.event_selection_input = event_selection_input
        self.title_input = title_input
        self.description_input = description_input
        self.capacity_input = capacity_input
        self.selection_input = selection_input
        self.start_time_input = start_time_input
        self.update_event = update_event
        self.events_for_user = events_for_user

    @commands.command()
    @commands.guild_only()
    async def edit(self, ctx):
        """Edit an existing event"""
        self.sync_event_channels.call(ctx.guild.id)

        editable_events = self.events_for_user.call(ctx.author, ctx.guild)

        # Needed to create event dm channel
        await ctx.author.create_dm()
        event = await self.event_selection_input.call(
            ctx.author, ctx.author.dm_channel, editable_events
        )

        if event is None:
            await ctx.author.dm_channel.send(t("event.empty_selection"))
            return
        elif event is -1:
            return

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

            if selection == 0:
                return
            elif selection == 1:
                await ctx.author.send(t("event.title_prompt"))
                title = await self.title_input.call(ctx.author, ctx.author.dm_channel)
                event.title = title

            elif selection == 2:
                await ctx.author.send(t("event.description_prompt"))
                description = await self.description_input.call(
                    ctx.author, ctx.author.dm_channel
                )
                event.description = description

            elif selection == 3:
                await ctx.author.send(t("event.capacity_prompt"))
                capacity = await self.capacity_input.call(
                    ctx.author, ctx.author.dm_channel
                )
                event.capacity = capacity

            elif selection == 4:
                await ctx.author.send(t("event.start_time_prompt"))
                start_time = await self.start_time_input.call(
                    ctx.author, ctx.author.dm_channel, event.time_zone
                )
                event.start_time = start_time

            responses = responses_for_event(session, event.id)

        channel = self.bot.get_channel(event.event_channel_id)
        await self.update_event.call(event, responses, channel)

        await ctx.author.send(t("event.updated"))
