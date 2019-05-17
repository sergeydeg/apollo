from discord.ext import commands

from apollo.models import Event
from apollo.queries import find_event_from_message, find_or_create_user


class OnRawReactionAdd(commands.Cog):

    def __init__(self, bot, handle_event_reaction):
        self.bot = bot
        self.handle_event_reaction = handle_event_reaction
        self.users_reacting = []


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with self.bot.scoped_session() as session:
            # Ignore reactions added by the bot
            if payload.user_id == self.bot.user.id:
                return

            # Stop if already procesing a reaction for this user
            if payload.user_id in self.users_reacting:
                return await self.remove_reaction(payload)

            event = find_event_from_message(session, payload.message_id)
            if not event:
                return

            try:
                self.users_reacting.append(payload.user_id)
                find_or_create_user(session, payload.user_id)
                await self.handle_event_reaction.call(session, event, payload)
            finally:
                # Clean up to ensure we don't enter an error state
                await self.remove_reaction(payload)
                self.users_reacting.remove(payload.user_id)


    async def remove_reaction(self, payload):
        try:
            await self.bot.remove_reaction(payload)
        except:
            pass
