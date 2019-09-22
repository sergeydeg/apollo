import discord


class EventListEmbed:
    def call(self, message):
        embed = discord.Embed(title="Events")
        embed.description = message
        return embed
