class UpdateEvent:
    def __init__(self, bot, event_embed):
        self.bot = bot
        self.event_embed = event_embed

    async def call(self, event, responses, discord_channel):
        event_embed = self.event_embed.call(event, responses, discord_channel.guild)
        event_message = await discord_channel.fetch_message(event.message_id)
        await event_message.edit(embed=event_embed)
