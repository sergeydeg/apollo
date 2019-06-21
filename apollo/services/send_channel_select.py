from apollo import emojis as emoji
from apollo.embeds import SelectChannelEmbed


class SendChannelSelect:
    def __init__(self, bot, channel, event_channels):
        self.bot = bot
        self.channel = channel
        self.event_channels = event_channels

    async def call(self):
        embed = SelectChannelEmbed(self._discord_channels()).call()
        message = await self.channel.send(embed=embed)
        await self._add_reactions(message)
        return message

    async def _add_reactions(self, message):
        for i, _ in enumerate(self.event_channels):
            await message.add_reaction(emoji.NUMBERS[i])

    def _discord_channels(self):
        return list(
            map(
                lambda event_channel: self.bot.get_channel(event_channel.id),
                self.event_channels,
            )
        )
