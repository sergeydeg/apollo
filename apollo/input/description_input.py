from apollo.translate import t
from config import MAX_DESC_LENGTH


class DescriptionInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel):
        """
        Get description from user
        :param user: Member, e.g. context.author
        :param channel: Messageable, e.g. context.author.dmchannel
        :return: str
        """

        while True:
            resp = (await self.bot.get_next_message(user, channel, timeout=240)).content
            if resp == "None":
                return None
            elif len(resp) <= MAX_DESC_LENGTH:
                return resp
            else:
                await user.send(t("event.invalid_description").format(MAX_DESC_LENGTH))
