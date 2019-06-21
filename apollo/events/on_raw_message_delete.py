from discord.ext import commands

from apollo.queries import find_event_from_message
from apollo.translate import t


class OnRawMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        # If the message is marked for deletion, it was deleted by the bot
        # as part of clearing the event channel. Unmark it, and return.
        if self.bot.cache.message_marked_for_deletion(payload.message_id):
            return self.bot.cache.unmark_message_for_deletion(payload.message_id)

        with self.bot.scoped_session() as session:
            event = find_event_from_message(session, payload.message_id)

            if not event:
                return

            session.delete(event)

            event_channel = event.event_channel

            if len(event_channel.events) == 0:
                discord_event_channel = self.bot.get_channel(event_channel.id)
                await discord_event_channel.send(t("channel.no_events"))
