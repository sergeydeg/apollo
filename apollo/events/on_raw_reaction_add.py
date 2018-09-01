from apollo.models import Event
from apollo.services import HandleEventReaction
from apollo.queries import find_event_from_message, find_or_create_user

class OnRawReactionAdd:

    def __init__(self, bot):
        self.bot = bot


    async def on_raw_reaction_add(self, payload):
        session = self.bot.Session()

        # Ignore reactions added by the bot
        if payload.user_id == self.bot.user.id:
            return

        if self.bot.cache.event_exists(payload.message_id):
            event = find_event_from_message(session, payload.message_id)
            find_or_create_user(session, payload.user_id)
            await HandleEventReaction(
                self.bot,
                session,
                event,
                payload).call()

        session.commit()
