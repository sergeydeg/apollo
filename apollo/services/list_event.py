from apollo import emojis as emoji
from apollo.embeds import EventEmbed


class ListEvent:

    def __init__(self, bot):
        self.bot = bot


    async def call(self, event, discord_channel):
        embed = EventEmbed(discord_channel.guild, event).call()
        event_message = await discord_channel.send(embed=embed)

        # Update event message reference
        event.message_id = event_message.id
        self.bot.cache.update_event(event.message_id, event_message.id)

        # Add RSVP reactions to event message
        await event_message.add_reaction(emoji.CHECK)
        await event_message.add_reaction(emoji.CROSS)
        await event_message.add_reaction(emoji.QUESTION)
