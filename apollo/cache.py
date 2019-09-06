from contextlib import contextmanager

from apollo.constants import DEFAULT_PREFIX
from apollo.models import Event, EventChannel, Guild

class Cache:
    def __init__(self, Session):
        self.Session = Session
        self.messages_marked_for_deletion = set()
        self.prefixes = {}

    @contextmanager
    def scoped_session(self):
        """Provide a transactional scope around a series of operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_prefix(self, guild_id):
        self.prefixes.pop(guild_id)

    def get_prefix(self, guild_id):
        return self.prefixes.get(guild_id, DEFAULT_PREFIX)

    def load_prefixes(self):
        with self.scoped_session() as session:
            guilds = session.query(Guild).all()
        for guild in guilds:
            self.prefixes[guild.id] = guild.prefix

    def mark_message_for_deletion(self, message_id):
        self.messages_marked_for_deletion.add(message_id)

    def message_marked_for_deletion(self, message_id):
        return message_id in self.messages_marked_for_deletion

    def unmark_message_for_deletion(self, message_id):
        self.messages_marked_for_deletion.remove(message_id)

    def update_prefix(self, guild_id, prefix):
        self.prefixes[guild_id] = prefix
