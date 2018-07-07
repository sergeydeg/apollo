import discord

from event_bot import emojis as emoji


def event_embed(event, organizer_name):
    embed = discord.Embed()
    embed.title = event.title
    if event.description : embed.description = event.description
    embed.set_footer(text=f"Created by {organizer_name} | React with {emoji.SKULL} to remove this event")
    return embed
