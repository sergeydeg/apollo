from apollo.models import Event
from apollo.services import HandleEventReaction
from apollo.queries import find_event_from_message, find_or_create_user


class OnRawReactionAdd:

    def __init__(self, bot):
        self.bot = bot
        self.users_reacting = []


    async def on_raw_reaction_add(self, payload):
        with self.bot.scoped_session() as session:
            # Ignore reactions added by the bot
            if payload.user_id == self.bot.user.id:
                return

            # Process event reaction
            if self.bot.cache.event_exists(payload.message_id):

                # Stop if already procesing a reaction for this user
                if payload.user_id in self.users_reacting:
                    await self.remove_reaction(payload)
                    return

                try:
                    self.users_reacting.append(payload.user_id)
                    event = find_event_from_message(session, payload.message_id)
                    find_or_create_user(session, payload.user_id)
                    await HandleEventReaction(
                        self.bot,
                        session,
                        event,
                        payload).call()
                finally:
                    # Clean up to ensure we don't enter an error state
                    await self.remove_reaction(payload)
                    self.users_reacting.remove(payload.user_id)


    async def remove_reaction(self, payload):
        try:
            await self.bot.remove_reaction(payload)
        except:
            pass
