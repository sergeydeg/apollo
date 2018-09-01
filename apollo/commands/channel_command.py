from discord.ext import commands

from apollo.can import Can
from apollo.services import ListEvents
from apollo.models import EventChannel
from apollo.queries import find_or_create_guild


class ChannelCommand:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    async def channel(self, ctx):
        """Create a new event channel"""
        session = self.bot.Session()

        if not Can(session, ctx.author).channel():
            return await ctx.send("You don't have permission to do that.")

        guild = find_or_create_guild(session, ctx.guild.id)
        if guild.has_max_event_channels():
            return await ctx.send("Event channel limit has been reached.")

        channel = await self.bot.create_discord_event_channel(ctx.guild)
        event_channel = EventChannel(id=channel.id, guild_id=ctx.guild.id)
        await ListEvents(self.bot, event_channel).call()

        await ctx.send(f"A new {channel.mention} channel has been created!")

        session.add(event_channel)
        session.commit()
