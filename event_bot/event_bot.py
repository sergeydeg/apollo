class EventBot:

    def __init__(self, bot, session_scope):
        self.bot = bot
        self.session_scope = session_scope


    def start(self, token):
        self.bot.run(token)
