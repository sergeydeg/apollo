import asyncio
import os
from contextlib import contextmanager

import arrow
import discord
from discord.ext import commands
from raven import Client

from apollo.prefix import prefix_callable


class Apollo(commands.AutoShardedBot):
    def __init__(self, Session, cache):
        super().__init__(command_prefix=prefix_callable)
        self.Session = Session
        self.client = Client(os.getenv("SENTRY_URL"))
        self.cache = cache

    @contextmanager
    def scoped_session(self):
        """Provide a transactional scope around a series of operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    async def create_discord_event_channel(self, guild):
        """Create a text channel with permissions needed to display events"""
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                send_messages=False, add_reactions=True
            ),
            guild.me: discord.PermissionOverwrite(
                send_messages=True, add_reactions=True
            ),
        }
        return await guild.create_text_channel("events", overwrites=overwrites)

    def find_guild_member(self, guild_id, user_id):
        """Retrieve a member with given id that belongs to the given guild"""
        return self.get_guild(guild_id).get_member(user_id)

    async def get_next_message(self, user, channel, timeout=120):
        """Get the next message a user sends in the given channel"""

        def is_from_user_in_channel(message):
            return (message.author == user) and (message.channel == channel)

        return await self.wait_for(
            "message", check=is_from_user_in_channel, timeout=timeout
        )

    async def get_next_pm(self, user, timeout=120):
        """Get the next private message a user sends to the bot"""
        return await self.get_next_message(user, user.dm_channel, timeout=timeout)

    async def remove_reaction(self, payload):
        """Remove a reaction given the raw_reaction_add payload"""
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = channel.guild.get_member(payload.user_id)
        await message.remove_reaction(payload.emoji, member)

    async def _run_event(self, coro, event_name, *args, **kwargs):
        """Overridden from discord.py to send exception reports"""
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if os.getenv("ENV") == "production":
                self.client.captureException()
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass
