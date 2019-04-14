from apollo.embeds import EventEmbed


class UpdateEvent:

    def __init__(self, bot):
        self.bot = bot


    async def call(self, event):
        event_channel = self.bot.get_channel(event.event_channel.id)
        updated_embed = EventEmbed(event_channel.guild, event).call()
        event_message = await event_channel.fetch_message(event.message_id)
        await event_message.edit(embed=updated_embed)
