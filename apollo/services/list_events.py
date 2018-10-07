from apollo import emojis as emoji
from apollo.embeds import EventEmbed
from apollo.translate import t


class ListEvents:

    def __init__(self, bot, event_channel):
        self.bot = bot
        self.event_channel = event_channel
        self.channel = self._get_channel()


    async def call(self):
        await self._clear_channel()

        if len(self.event_channel.events) == 0:
            return await self.channel.send(t("channel.no_events"))

        for event in self.event_channel.events:
            event_message = await self._send_event_message(event)
            self.bot.cache.update_event(event.message_id, event_message.id)
            event.message_id = event_message.id
            await self._add_reactions(event_message)


    async def _add_reactions(self, message):
        await message.add_reaction(emoji.CHECK)
        await message.add_reaction(emoji.CROSS)
        await message.add_reaction(emoji.QUESTION)


    async def _clear_channel(self):
        self._mark_messages_for_deletion()
        await self.channel.purge()


    def _get_channel(self):
        return self.bot.get_channel(self.event_channel.id)


    def _mark_messages_for_deletion(self):
        for event in self.event_channel.events:
            self.bot.cache.mark_message_for_deletion(event.message_id)


    async def _send_event_message(self, event):
        embed = EventEmbed(self.channel.guild, event).call()
        return await self.channel.send(embed=embed)
