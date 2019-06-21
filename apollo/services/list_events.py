from apollo.translate import t
from apollo.queries import responses_for_event


class ListEvents:
    def __init__(self, bot, list_event):
        self.bot = bot
        self.list_event = list_event

    async def call(self, events, discord_channel):
        # Mark messages for deletion so that we can ignore them
        # in OnRawMessageDelete.
        for event in events:
            self.bot.cache.mark_message_for_deletion(event.message_id)

        await discord_channel.purge()

        if len(events) == 0:
            return await discord_channel.send(t("channel.no_events"))

        for event in self.sort_events_by_start_time(events):
            with self.bot.scoped_session() as session:
                responses = responses_for_event(session, event.id)
            await self.list_event.call(event, responses, discord_channel)

    def sort_events_by_start_time(self, events):
        return sorted(events, key=lambda event: event.utc_start_time, reverse=True)
