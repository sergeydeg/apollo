import discord


class EventListEmbed:
    def call(self, message, title):
        embed = discord.Embed(title=title)
        embed.description = message
        return embed
