from .embeds import event_embed
from .queries import find_event, find_event_channel
from . import emojis as emoji


async def list_events(bot, session, event_channel):
    """Clear the event channel and populate it with events"""
    channel = bot.get_channel(event_channel.id)
    await channel.purge()

    if len(event_channel.events) == 0:
        await channel.send("There are no upcoming events in this channel.")

    for event in event_channel.events:
        embed = event_embed(channel.guild, event)
        event_msg = await channel.send(embed=embed)
        await _add_rsvp_reactions(event_msg)
        event.message_id = event_msg.id


async def update_event_message(bot, session, event):
    """Update an event message in place"""
    channel = bot.get_channel(event.event_channel.id)
    event_message = await channel.get_message(event.message_id)
    embed = event_embed(channel.guild, event)
    await event_message.edit(embed=embed)


async def _add_rsvp_reactions(msg):
    """Add reaction 'rsvp buttons' to a message"""
    await msg.add_reaction(emoji.CHECK)
    await msg.add_reaction(emoji.CROSS)
    await msg.add_reaction(emoji.QUESTION)
