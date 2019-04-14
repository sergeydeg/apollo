from apollo import emojis as emoji


EMOJI_STATUSES = {
    emoji.CHECK: 'accepted',
    emoji.QUESTION: 'alternate',
    emoji.CROSS: 'declined'
}


class HandleEventReaction:

    def __init__(self, bot, delete_event, update_event, update_response):
        self.bot = bot
        self.delete_event = delete_event
        self.update_event = update_event
        self.update_response = update_response


    async def call(self, session, event, payload):
        if payload.emoji.name == emoji.SKULL:
            member = self.bot.find_guild_member(payload.guild_id, payload.user_id)
            return await self.delete_event.call(session, event, member)

        rsvp_status = EMOJI_STATUSES.get(payload.emoji.name)
        if rsvp_status:
            await self.update_response.call(
                session,
                event.id,
                payload.user_id,
                rsvp_status
            )
            await self.update_event.call(event)
