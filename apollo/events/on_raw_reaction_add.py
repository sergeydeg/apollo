from apollo import emojis as emoji
from apollo.list_events import ListEvents
from apollo.models import Event, Response
from apollo.update_event import UpdateEvent
from apollo.queries import find_event_from_message, find_response


ACCEPTED  = 'accepted'
ALTERNATE = 'alternate'
DECLINED  = 'declined'

EMOJI_STATUSES = {
    emoji.CHECK: ACCEPTED,
    emoji.QUESTION: ALTERNATE,
    emoji.CROSS: DECLINED
    }


class OnRawReactionAdd:

    def __init__(self, bot):
        self.bot = bot


    async def on_raw_reaction_add(self, payload):
        session = self.bot.Session()

        # Ignore reactions added by the bot
        if payload.user_id == self.bot.user.id:
            return

        event = find_event_from_message(session, payload.message_id)
        if event:
            await self._handle_event_reaction(session, event, payload)

        session.commit()


    def _update_response(self, session, event, payload):
        response = find_response(session, payload.user_id, event.id)
        if not response:
            response = Response(user_id=payload.user_id, event_id=event.id)

        response.status = EMOJI_STATUSES.get(payload.emoji.name)
        session.add(response)


    async def _handle_event_reaction(self, session, event, payload):
        if EMOJI_STATUSES.get(payload.emoji.name):
            self._update_response(session, event, payload)
            await UpdateEvent(self.bot, event).call()
            await self.bot.remove_reaction(payload)
            session.add(event)
        elif payload.emoji.name == emoji.SKULL:
            session.delete(event)
            await ListEvents(self.bot, event.event_channel).call()
        else:
            await self.bot.remove_reaction(payload)
