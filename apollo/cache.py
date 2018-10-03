from apollo.models import Event, EventChannel, Guild


class Cache:

    def __init__(self, Session):
        self.Session = Session
        self.event_message_ids = set()
        self.event_channel_ids = set()
        self.prefixes = {}


    def create_event_channel(self, event_channel_id):
        self.event_message_ids.add(event_channel_id)


    def delete_event_channel(self, event_channel_id):
        self.event_channel_ids.remove(event_channel_id)


    def delete_event(self, message_id):
        self.event_message_ids.remove(message_id)


    def delete_prefix(self, guild_id):
        self.prefixes.pop(guild_id)


    def event_channel_exists(self, event_channel_id):
        return event_channel_id in self.event_channel_ids


    def event_exists(self, message_id):
        return message_id in self.event_message_ids


    def get_prefix(self, guild_id):
        return self.prefixes[guild_id]


    def load_event_channel_ids(self):
        session = self.Session()
        event_channels = session.query(EventChannel).all()
        for event_channel in event_channels:
            self.event_channel_ids.add(event_channel.id)
        session.commit()


    def load_event_message_ids(self):
        session = self.Session()
        events = session.query(Event).all()
        for event in events:
            self.event_message_ids.add(event.message_id)
        session.commit()


    def load_prefixes(self):
        session = self.Session()
        guilds = session.query(Guild).all()
        for guild in guilds:
            self.prefixes[guild.id] = guild.prefix
        session.commit()


    def update_event(self, old_message_id, new_message_id):
        try:
            # If the event is new, it won't be in the cache
            self.event_message_ids.remove(old_message_id)
        except:
            pass
        self.event_message_ids.add(new_message_id)


    def update_prefix(self, guild_id, prefix):
        self.prefixes[guild_id] = prefix
