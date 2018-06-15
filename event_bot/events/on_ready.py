class OnReady:

    def __init__(self, bot, transaction):
        self.bot = bot
        self.transaction = transaction


    async def on_ready(self):
        print(f"{self.bot.user.name} - Ready")
