from discord.ext import commands
from contextlib import contextmanager


class EventBot(commands.AutoShardedBot):

    def __init__(self, Session):
        super().__init__(command_prefix='!')
        self.Session = Session


    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of DB operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
