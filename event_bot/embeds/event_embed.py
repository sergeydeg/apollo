import discord


SKULL_EMOJI = '\U0001f480'

def event_embed(event, organizer_name):
    embed = discord.Embed()
    embed.title = event.title
    if event.description : embed.description = event.description
    embed.set_footer(text=f"Created by {organizer_name} | React with {SKULL_EMOJI} to remove this event")
    return embed
