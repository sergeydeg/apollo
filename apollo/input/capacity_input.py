from apollo.translate import t
from config import MAX_CAPACITY


class CapacityInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel):
        """
        Retrieve the event capacity from the user
        :param user: Member, e.g. context.author
        :param channel: Messageable, e.g. context.author.dmchannel
        :return: int or None
        """

        while True:
            resp = (await self.bot.get_next_message(user, channel)).content
            if resp.upper() == "NONE":
                return None
            elif resp.isdigit() and int(resp) in range(1, MAX_CAPACITY + 1):
                return int(resp)
            else:
                await channel.send(t("event.invalid_capacity").format(MAX_CAPACITY))
