from apollo.embeds import EventListEmbed
from apollo.models import EventChannel, Event, Guild, User
from apollo.permissions import HavePermission
from apollo.translate import t


class EventSelectionInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel, events, title=None):
        """
        Send a list of events to the user and ask them to pick one.
        Note only sends a list, and does not send the prompt before it.
        :param user: Member, e.g. context.author
        :param channel: Messageable
        :param events: list of events
        :param title: str, if None, will default to generic
        :return: Event or None if no events exist
        """
        if title is None:
            title = t("event.query_events_list")

        if len(events) == 0:
            await channel.send(t("event.empty_selection"))
            return None

        events_dict = {}
        for index, event in enumerate(events, start=1):
            events_dict[index] = event

        await channel.send(embed=EventListEmbed().call(events, title=title))

        return await self._get_event_from_user(user, events_dict)

    async def _get_event_from_user(self, user, events_dict):
        while True:
            resp = (await self.bot.get_next_pm(user, timeout=60)).content
            if not resp.isdigit() or int(resp) not in list(events_dict.keys()):
                await user.send(t("event.event_selection_error"))
            else:
                event = events_dict[int(resp)]
                return event
