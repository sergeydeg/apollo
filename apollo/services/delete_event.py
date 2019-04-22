from apollo.can import Can
from apollo.queries import find_or_create_guild


class DeleteEvent:

    def __init__(self, bot, list_events):
        self.bot = bot
        self.list_events = list_events


    async def call(self, session, event, member):
        if self._member_can_delete(session, member):
            session.delete(event)
            self.bot.cache.delete_event(event.message_id)
            await self.list_events.call(event.event_channel)
        else:
            await member.send("You don't have permission to do that.")


    def _member_can_delete(self, session, member):
        guild = find_or_create_guild(session, member.guild.id)
        return(
            Can(member, guild).delete() or
            self._member_owns_event(event, memver)
            )


    def _member_owns_event(self, event, member):
        return event.organizer.id == member.id
