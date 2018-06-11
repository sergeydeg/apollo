from discord.ext import commands


class EventBot(commands.AutoShardedBot):

    def __init__(self, token, Session):
        super().__init__(command_prefix='!')
        self.token = token
        self.Session = Session


    def new_session(self):
        return self.Session()


    def run(self):
        super().run(self.token, reconnect=True)
