from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class EventChannel(Base):
    __tablename__ = 'event_channel'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey('guild.id', ondelete='CASCADE'), nullable=False)

    events = relationship("Event", passive_deletes=True)
