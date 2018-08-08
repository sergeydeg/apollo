from .embeds import event_embed

class UpdateEvent:

    def __init__(self, bot, event):
        self.bot = bot
        self.event = event
        self.channel = self._get_channel()


    async def call(self):
        event_message = await self.channel.get_message(self.event.message_id)
        updated_embed = event_embed(self.channel.guild, self.event)
        await event_message.edit(embed=updated_embed)


    def _get_channel(self):
        return self.bot.get_channel(self.event.event_channel.id)
