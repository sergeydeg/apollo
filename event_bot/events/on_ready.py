class OnReady:

    def __init__(self, bot, session_scope):
        self.bot = bot
        self.session_scope = session_scope


    async def on_ready(self):
        print(f"{self.bot.user.name} - Ready")
