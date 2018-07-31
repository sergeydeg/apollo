from .embeds import event_embed
from .queries import find_event, find_event_channel
from . import emojis as emoji


async def list_events(bot, event_channel_id):
    """Clear the event channel and populate it with events"""
    session = bot.Session()

    event_channel = find_event_channel(session, event_channel_id)
    channel = bot.get_channel(event_channel.id)
    await channel.purge()

    for event in event_channel.events:
        embed = event_embed(channel.guild, event)
        event_msg = await channel.send(embed=embed)
        await _add_rsvp_reactions(event_msg)
        event.message_id = event_msg.id

    session.add(event_channel)
    session.commit()


async def update_event_message(bot, event_id):
    """Update an event message in place"""
    session = bot.Session()

    event = find_event(session, event_id)
    channel = bot.get_channel(event.event_channel.id)
    event_message = await channel.get_message(event.message_id)
    embed = event_embed(channel.guild, event)
    await event_message.edit(embed=embed)

    session.add(event)
    session.commit()


async def _add_rsvp_reactions(msg):
    """Add reaction 'rsvp buttons' to a message"""
    await msg.add_reaction(emoji.CHECK)
    await msg.add_reaction(emoji.CROSS)
    await msg.add_reaction(emoji.QUESTION)
