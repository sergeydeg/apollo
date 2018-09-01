from apollo import emojis as emoji
from apollo.models import Response
from apollo.queries import find_response
from .update_event import UpdateEvent


EMOJI_STATUSES = {
    emoji.CHECK: 'accepted',
    emoji.QUESTION: 'alternate',
    emoji.CROSS: 'declined'
    }


class UpdateResponse:

    def __init__(self, bot, session, event, payload):
        self.bot = bot
        self.session = session
        self.event = event
        self.payload = payload


    async def call(self):
        response = self._find_or_create_response()
        response.status = EMOJI_STATUSES.get(self.payload.emoji.name)
        self.session.add(response)
        await UpdateEvent(self.bot, self.event).call()


    def _find_or_create_response(self):
        response = find_response(
            self.session,
            self.payload.user_id,
            self.event.id)
        if not response:
            response = Response(
                user_id=self.payload.user_id,
                event_id=self.event.id
                )
        return response
