from apollo import emojis as emoji
from apollo.list_events import update_event_message
from apollo.models import Event, Response
from apollo.queries import find_event_from_message, \
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
        if payload.user_id == self.bot.user.id:
            return
        event = find_event_from_message(
            self.bot.db,
            payload.message_id
        )
        if event:
            await self._handle_event_reaction(event, payload)


    def _save_response(self, event, payload):
        response = find_or_create_response(
            self.bot.db,
            payload.user_id,
            event.id
        )
        response.status = self.emoji_statuses.get(payload.emoji.name)
        self.bot.db.add(response)


    async def _handle_event_reaction(self, event, payload):
        if self.emoji_statuses.get(payload.emoji.name):
            self._save_response(event, payload)
            await update_event_message(self.bot, event.id)
