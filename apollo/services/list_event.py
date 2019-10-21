from apollo import emojis as emoji
from apollo.entities import EventSummary


class ListEvent:
    def __init__(self, bot, event_embed):
        self.bot = bot
        self.event_embed = event_embed

    async def call(self, event, responses, discord_channel):
        event_summary = EventSummary(discord_channel.guild, event, responses)

        embed = self.event_embed.call(event_summary)
        event_message = await discord_channel.send(embed=embed)

        # Update event message reference
        event.message_id = event_message.id
        with self.bot.scoped_session() as session:
            session.add(event)

        # Add RSVP reactions to event message
        await event_message.add_reaction(emoji.CHECK)
        await event_message.add_reaction(emoji.CROSS)
        await event_message.add_reaction(emoji.QUESTION)
        await event_message.add_reaction(emoji.CLOCK)
