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
        self.member = self._get_member()


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


    def _get_member(self):
        guild = self.bot.get_guild(self.payload.guild_id)
        return guild.get_member(self.payload.user_id)
