class UpdateEvent:

    def __init__(self, bot, event_embed):
        self.bot = bot
        self.event_embed = event_embed


    async def call(self, event):
        event_channel = self.bot.get_channel(event.event_channel.id)
        updated_embed = self.event_embed.call(event, event_channel.guild)
        event_message = await event_channel.fetch_message(event.message_id)
        await event_message.edit(embed=updated_embed)
