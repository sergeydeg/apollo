from apollo import emojis as emoji
from apollo.services import DeleteEvent
from apollo.services import UpdateResponse


EMOJI_STATUSES = {
    emoji.CHECK: 'accepted',
    emoji.QUESTION: 'alternate',
    emoji.CROSS: 'declined'
    }


class HandleEventReaction:

    def __init__(self, bot, session, event, payload):
        self.bot = bot
        self.session = session
        self.event = event
        self.payload = payload
        self.member = bot.find_guild_member(payload.guild_id, payload.user_id)


    async def call(self):
        if self.payload.emoji.name == emoji.SKULL:
            await DeleteEvent(
                self.bot,
                self.session,
                self.event,
                self.member
                ).call()
        elif EMOJI_STATUSES.get(self.payload.emoji.name):
            await UpdateResponse(
                self.bot,
                self.session,
                self.event,
                self.payload
                ).call()

        try:
            await self.bot.remove_reaction(self.payload)
        except:
            pass
