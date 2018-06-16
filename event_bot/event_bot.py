import discord
from discord.ext import commands


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
