from sqlalchemy import Column, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event_channel_id = Column(Integer, ForeignKey('event_channel.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    message_id = Column(Integer)
    title = Column(Text)
    description = Column(Text)
    start_time = Column(DateTime)

    event_channel = relationship("EventChannel", back_populates="events")
    organizer = relationship("User", back_populates="events")
    responses = relationship("Response")
