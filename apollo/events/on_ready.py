from apollo.services import SyncModels


class OnReady:

    def __init__(self, bot):
        self.bot = bot


    async def on_ready(self):
        print(f"{self.bot.user.name} - Ready")

        # Sync models that may have changed while offline
        SyncModels(self.bot).call()

        # Load items into cache
        self.bot.cache.load_prefixes()
        self.bot.cache.load_event_message_ids()
