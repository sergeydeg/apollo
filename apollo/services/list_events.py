from apollo.translate import t


class ListEvents:

    def __init__(self, bot, list_event):
        self.bot = bot
        self.list_event = list_event


    async def call(self, event_channel):
        discord_event_channel = self.bot.get_channel(event_channel.id)

        # Mark messages for deletion so that we can ignore them
        # in OnRawMessageDelete
        for event in event_channel.events:
            self.bot.cache.mark_message_for_deletion(event.message_id)

        await discord_event_channel.purge()

        if len(event_channel.events) == 0:
            return await discord_event_channel.send(t("channel.no_events"))

        for event in event_channel.sorted_events():
            await self.list_event.call(event, discord_event_channel)
