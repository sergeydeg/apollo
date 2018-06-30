from event_bot import emojis as emoji
from event_bot.models import Event, Response
from event_bot.queries import find_event_from_message, \
    find_or_create_response


class OnRawReactionAdd:
    ACCEPTED  = 'accepted'
    ALTERNATE = 'alternate'
    DECLINED  = 'declined'

    emoji_statuses = {
        emoji.CHECK: ACCEPTED,
        emoji.QUESTION: ALTERNATE,
        emoji.CROSS: DECLINED
    }

    def __init__(self, bot):
        self.bot = bot


    async def on_raw_reaction_add(self, payload):
        """Discord event handler"""
        if payload.user_id == self.bot.user_id:
            return

        event = find_event_from_message(
            self.bot.transaction,
            payload.message_id
        )
        if event: await self._handle_event_reaction(event, payload)


    def _handle_event_response(self, event, payload):
        response = find_or_create_response(
            self.bot.transaction,
            payload.user_id,
            event.id
        )
        response.status = self.emoji_statuses.get(payload.emoji.name)
        with self.bot.transaction.new() as session:
            session.add(response)


    async def _handle_event_reaction(self, event, payload):
        if self.emoji_statuses.get(payload.emoji.name):
            self._handle_event_response(event, payload)
