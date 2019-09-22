from apollo.embeds import EventListEmbed
from apollo.models import EventChannel, Event, Guild, User
from apollo.permissions import HavePermission
from apollo.translate import t


class EventSelectionInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel, guild, events=None):
        """
        Send a list of events to the user and ask them to pick one.
        Note only sends a list, and does not send the prompt before it.
        :param user: Member, e.g. context.author
        :param channel: Messageable
        :param guild: int, guild id
        :param events: str, Choice of editable, channel
        :return: Event
        """
        if events == "editable":
            events = self._editable_events(user, guild)
        elif events == "channel":
            events = self._event_channel(channel)
        else:
            events = self._guild_events(guild)

        events_string = ""
        events_dict = {}
        for index, event in enumerate(events, start=1):
            events_string += f"{index}: {event.title}\n"
            events_dict[index] = event

        await channel.send(embed=EventListEmbed().call(events_string))

        return await self._get_event_from_user(user, events_dict)

    async def _get_event_from_user(self, user, events_dict):
        while True:
            resp = (await self.bot.get_next_pm(user, timeout=60)).content
            if not resp.isdigit() and int(resp) not in events_dict.keys():
                await user.send(t("event.event_selection_error"))
            else:
                event = events_dict[int(resp)]
                return event

    def _editable_events(self, user, guild):
        """Get events that the user can edit"""
        with self.bot.scoped_session() as session:

            if HavePermission(user, guild).manage_guild():
                # If have guild_permissions.manage_guild, list all events.
                events = (
                    session.query(Event)
                    .join(EventChannel)
                    .join(Guild)
                    .filter(Guild.id == guild.id)
                    .all()
                )
            else:
                # Otherwise list only the ones the user has access to
                events = (
                    session.query(Event)
                    .join(EventChannel)
                    .join(Guild)
                    .join(User)
                    .filter(Guild == guild.id)
                    .filter(User.id == Event.organizer_id)
                )

            return events

    def _event_channel(self, channel):
        """Get events for a channel"""
        with self.bot.scoped_session() as session:
            events = (
                session.query(Event).filter(Event.event_channel_id == channel.id).all()
            )

            return events

    def _guild_events(self, guild):
        """Get events for guild"""
        with self.bot.scoped_session() as session:
            events = (
                session.query(Event)
                .join(EventChannel)
                .join(Guild)
                .filter(Guild.id == guild.id)
                .all()
            )

            return events
