from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class EventChannel(Base):
    __tablename__ = 'event_channel'
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey('guild.id', ondelete='CASCADE'))
    events = relationship("Event", passive_deletes=True)
