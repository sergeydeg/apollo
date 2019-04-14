from datetime import datetime

from apollo.models import Response
from apollo.queries import find_response


class UpdateResponse:

    def __init__(self):
        pass


    async def call(self, session, event_id, user_id, rsvp_status):
        response = find_response(session, user_id, event_id)

        if not response:
            response = Response(user_id=user_id, event_id=event_id)

        response.status = rsvp_status
        response.last_updated = datetime.now()

        session.add(response)
