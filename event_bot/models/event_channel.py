from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class EventChannel(Base):
    __tablename__ = 'event_channel'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey('guild.id'))

    events = relationship("Event", back_populates="event_channel")
    guild = relationship("Guild", back_populates="event_channels")
