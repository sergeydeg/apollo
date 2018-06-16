from sqlalchemy import BigInteger, Column, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event_channel_id = Column(BigInteger, ForeignKey('event_channel.id', ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'))
    message_id = Column(BigInteger)
    title = Column(Text)
    description = Column(Text)
    start_time = Column(DateTime)
    capacity = Column(Integer)
    organizer = relationship("User")
    responses = relationship("Response", passive_deletes=True)
