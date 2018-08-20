import arrow
from discord.ext import commands

from apollo.list_events import ListEvents
from apollo.models import Event, EventChannel, Guild
from apollo.queries import find_or_create_guild, find_or_create_user
from apollo.send_channel_select import SendChannelSelect
from apollo.time_zones import VALID_TIME_ZONES


class EventCommand:
    MAX_CAPACITY = 40
    MAX_DESC_LENGTH = 250
    MAX_TITLE_LENGTH = 100

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    async def event(self, ctx):
        """Create a new event"""
        session = self.bot.Session()

        await ctx.send("Event creation instructions have been messaged to you.")
        event = await self._get_event_from_user(ctx, session)
        channel = self.bot.get_channel(event.event_channel.id)
        await ctx.author.send(f"Your event has been created in the {channel.mention} channel!")
        await ListEvents(self.bot, event.event_channel).call()

        session.add(event)
        session.commit()


    async def _choose_event_channel(self, ctx, event_channels):
        message = await SendChannelSelect(
            self.bot,
            ctx.author.dm_channel,
            event_channels
            ).call()

        def reaction_check(reaction, user):
            return (message.id == reaction.message.id) \
                and (user.id == ctx.author.id)

        reaction, _ = await self.bot.wait_for(
            'reaction_add',
            check=reaction_check,
            timeout=90.0)

        return event_channels[int(reaction.emoji[0]) - 1]


    async def _get_capacity_from_user(self, ctx):
        """Retrieve the event capacity from the user"""
        await ctx.author.send("Enter the maximum number of attendees (type 'None' for no limit):")
        while True:
            resp = (await self.bot.get_next_pm(ctx.author)).content
            if resp.upper() == 'NONE':
                return None
            elif resp.isdigit() and int(resp) in range(1, self.MAX_CAPACITY):
                return int(resp)
            else:
                await ctx.author.send(f"Entry must be between 1 and {self.MAX_CAPACITY} (or 'None' for no limit). Try again:")


    async def _get_desc_from_user(self, ctx):
        """Retrieve the event description from the user"""
        await ctx.author.send("Enter event description (type 'None' for no description):")
        while True:
            resp = (await self.bot.get_next_pm(ctx.author, timeout=240)).content
            if resp.upper() == 'NONE':
                return None
            elif len(resp) <= self.MAX_DESC_LENGTH:
                return resp
            else:
                await ctx.author.send(f"Event description must be less than {self.MAX_DESC_LENGTH} characters. Try again:")


    async def _get_event_channel(self, ctx, session):
        """Find or create the event channel for the current guild"""
        guild = find_or_create_guild(session, ctx.guild.id)

        if guild.has_single_event_channel():
            return guild.event_channels[0]
        elif guild.has_multiple_event_channels():
            return await self._choose_event_channel(ctx, guild.event_channels)
        else:
            channel = await self.bot.create_discord_event_channel(ctx.guild)
            return EventChannel(id=channel.id, guild_id=ctx.guild.id)


    async def _get_start_time(self, ctx, time_zone):
        """Retrieve a datetime UTC object from the user"""
        await ctx.author.send("Enter the event start time (ex. `2018-08-17 7:00 pm` or `2018-08-17 19:00`):")
        while True:
            start_time_str = (await self.bot.get_next_pm(ctx.author)).content
            try:
                start_time = arrow.get(
                    start_time_str,
                    ['YYYY-MM-DD h:mm A', 'YYYY-MM-DD HH:mm'],
                    tzinfo=VALID_TIME_ZONES.get(time_zone)
                )
                return start_time.to('utc').datetime
            except:
                await ctx.author.send("Invalid start time. Try again:")


    async def _get_time_zone(self, ctx):
        """Retrieve a valid time zone string from the user"""
        await ctx.author.send("Enter your time zone:")
        while True:
            time_zone = (await self.bot.get_next_pm(ctx.author)).content.upper()
            if time_zone in VALID_TIME_ZONES.keys():
                return time_zone
            else:
                await ctx.author.send("Invalid time zone. Try again:")


    async def _get_title_from_user(self, ctx):
        """Retrieve the event title from the user"""
        await ctx.author.send("Enter the event title:")
        while True:
            title = (await self.bot.get_next_pm(ctx.author)).content
            if len(title) <= self.MAX_TITLE_LENGTH:
                return title
            else:
                await ctx.author.send(f"Event title must be less than {self.MAX_TITLE_LENGTH} characters. Try again:")


    async def _get_event_from_user(self, ctx, session):
        """Create an event with user input via private messages"""
        event = Event()
        event.organizer = find_or_create_user(session, ctx.author.id)
        event.title = await self._get_title_from_user(ctx)
        event.description = await self._get_desc_from_user(ctx)
        event.capacity = await self._get_capacity_from_user(ctx)
        event.event_channel = await self._get_event_channel(ctx, session)
        event.time_zone = await self._get_time_zone(ctx)
        event.start_time = await self._get_start_time(ctx, event.time_zone)
        return event
