from apollo.models import Event, Guild


class Cache:

    def __init__(self, Session):
        self.Session = Session
        self.event_message_ids = set()
        self.prefixes = {}


    def delete_event(self, message_id):
        self.event_message_ids.remove(message_id)


    def event_exists(self, message_id):
        return message_id in self.event_message_ids


    def get_prefix(self, guild_id):
        return self.prefixes[guild_id]


    def load_event_message_ids(self):
        session = self.Session()
        events = session.query(Event).all()
        for event in events:
            self.event_message_ids.add(event.message_id)


    def load_prefixes(self):
        session = self.Session()
        guilds = session.query(Guild).all()
        for guild in guilds:
            self.prefixes[guild.id] = guild.prefix


    def update_event(self, old_message_id, new_message_id):
        try:
            # If the event is new, it won't be in the cache
            self.event_message_ids.remove(old_message_id)
        except:
            pass
        self.event_message_ids.add(new_message_id)


    def update_prefix(self, guild_id, prefix):
        self.prefixes[guild_id] = prefix
