from sqlalchemy import Column, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


MAX_CHANNELS = 9


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(BigInteger, primary_key=True)
    prefix = Column(Text)
    event_role_id = Column(BigInteger)
    channel_role_id = Column(BigInteger)
    delete_role_id = Column(BigInteger)
    event_channels = relationship(
        "EventChannel", back_populates="guild", passive_deletes=True
    )
