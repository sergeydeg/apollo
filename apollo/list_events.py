from . import emojis as emoji
from .embeds import event_embed

class ListEvents:

    def __init__(self, bot, event_channel):
        self.bot = bot
        self.event_channel = event_channel
        self.channel = self._get_channel()


    async def call(self):
        await self.channel.purge()     

        if len(self.event_channel.events) == 0:
            return await self.channel.send(
                "There are no upcoming events in this channel.")

        for event in self.event_channel.events:
            event_message = await self._send_event_message(event)
            self.bot.cache.update_event(event.message_id, event_message.id)
            event.message_id = event_message.id
            await self._add_reactions(event_message)


    async def _add_reactions(self, message):
        await message.add_reaction(emoji.CHECK)
        await message.add_reaction(emoji.CROSS)
        await message.add_reaction(emoji.QUESTION)


    def _get_channel(self):
        return self.bot.get_channel(self.event_channel.id)


    async def _send_event_message(self, event):
        embed = event_embed(self.channel.guild, event)
        return await self.channel.send(embed=embed)
