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


    async def get_next_message(self, user, channel, timeout=120):
        """Get the next message a user sends in the given channel"""
        def is_from_user_in_channel(message):
            return (message.author == user) and (message.channel == channel)
        return await self.wait_for('message', check=is_from_user_in_channel, timeout=timeout)


    async def get_next_pm(self, user, timeout=120):
        """Get the next private message a user sends to the bot"""
        return await self.get_next_message(user, user.dm_channel, timeout=timeout)
