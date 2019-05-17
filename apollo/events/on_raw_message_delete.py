from discord.ext import commands

from apollo.queries import find_event_from_message


class OnRawMessageDelete(commands.Cog):

    def __init__(self, bot, list_events):
        self.bot = bot
        self.list_events = list_events


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if not self.bot.cache.event_exists(payload.message_id): return

        # If the message is marked for deletion, it was deleted by the bot
        # as part of clearing the event channel. Unmark it, and return.
        if self.bot.cache.message_marked_for_deletion(payload.message_id):
            return self.bot.cache.unmark_message_for_deletion(
                payload.message_id
                )

        with self.bot.scoped_session() as session:
            event = find_event_from_message(session, payload.message_id)
            session.delete(event)

        self.bot.cache.delete_event(event.message_id)
        await self.list_events.call(event.event_channel)
