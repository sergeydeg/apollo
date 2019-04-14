from apollo.can import Can
from .list_events import ListEvents
from apollo.queries import find_or_create_guild


class DeleteEvent:

    def __init__(self, bot):
        self.bot = bot


    async def call(self, session, event, member):
        if self._member_can_delete(session, member):
            session.delete(event)
            self.bot.cache.delete_event(event.message_id)
            await ListEvents(self.bot, event.event_channel).call()
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
