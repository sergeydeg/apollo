from apollo.models import EventChannel, Event
from apollo.permissions import HavePermission
from apollo.translate import t


class EventSelectionInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel, guild):
        """
        Send a list of events to the user and ask them to pick one.
        Note only sends a list, and does not send the prompt before it.
        :param user: Member, e.g. context.author
        :param channel: Messageable
        :param guild: int, guild id
        :return: Event
        """
        # Get all event channels for guild
        with self.bot.scoped_session() as session:
            event_channels = (
                session.query(EventChannel).filter_by(guild_id=guild.id).all()
            )
            events = []

            for event_channel in event_channels:
                if HavePermission(user, guild).manage_guild():
                    # If have guild_permissions.manage_guild, list all events.
                    events += (
                        session.query(Event)
                        .filter_by(event_channel_id=event_channel.id)
                        .all()
                    )
                else:
                    # Otherwise list only the ones the user has access to
                    events += session.query(Event).filter_by(
                        event_channel_id=event_channel.id, organizer=user
                    )

        events_string = ""
        events_dict = {}
        for index, event in enumerate(events, start=1):
            events_string += f"{index}: {event.title}\n"
            events_dict[index] = event

        await channel.send(events_string)

        return await self._get_event_from_user(user, events_dict)

    async def _get_event_from_user(self, user, events_dict):
        while True:
            resp = (await self.bot.get_next_pm(user, timeout=60)).content
            if not resp.isdigit() and int(resp) not in events_dict.keys():
                await user.send(t("event.event_selection_error"))
            else:
                event = events_dict[int(resp)]
                return event
