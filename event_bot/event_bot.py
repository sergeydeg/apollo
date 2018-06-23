import discord
from discord.ext import commands

from .embeds import event_embed


class EventBot(commands.AutoShardedBot):

    def __init__(self, transaction):
        super().__init__(command_prefix='!')
        self.transaction = transaction


    async def get_next_message(self, user, channel, timeout=120):
        """Get the next message a user sends in the given channel"""
        def is_from_user_in_channel(message):
            return (message.author == user) and (message.channel == channel)
        return await self.wait_for('message', check=is_from_user_in_channel, timeout=timeout)


    async def get_next_pm(self, user, timeout=120):
        """Get the next private message a user sends to the bot"""
        return await self.get_next_message(user, user.dm_channel, timeout=timeout)


    async def create_discord_event_channel(self, guild):
        """Create a text channel with the permissions needed to display events"""
        overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=True),
                guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True)
                }
        return await guild.create_text_channel("events", overwrites=overwrites)


    async def list_events(self, event_channel):
        """Clear the given event channel and then populate it with events"""
        channel = self.get_channel(event_channel.id)
        await channel.purge()
        for event in event_channel.events:
            organizer = self.find_guild_member(event_channel.guild_id, event.organizer_id)
            await channel.send(embed=event_embed(event, organizer.display_name))


    def find_guild_member(self, guild_id, user_id):
        """Retrieve a member with given id that belongs to the given guild"""
        return self.get_guild(guild_id).get_member(user_id)
