from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class EventChannel(Base):
    __tablename__ = 'event_channels'
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id', ondelete='CASCADE'))
    events = relationship("Event", back_populates="event_channel", passive_deletes=True)
    guild = relationship("Guild", back_populates="event_channels")
