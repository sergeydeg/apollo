from datetime import datetime

from apollo.models import Response
from apollo.queries import find_response


class UpdateResponse:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, event_id, user_id, rsvp_status):
        with self.bot.scoped_session() as session:
            response = find_response(session, user_id, event_id)

        if not response:
            response = Response(user_id=user_id, event_id=event_id)

        response.status = rsvp_status
        response.last_updated = datetime.now()

        with self.bot.scoped_session() as session:
            session.add(response)
