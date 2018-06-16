from sqlalchemy import Column, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Guild(Base):
    __tablename__ = 'guild'
    id = Column(BigInteger, primary_key=True)
    prefix = Column(Text)
    event_channels = relationship("EventChannel", back_populates="guild", passive_deletes=True)


    def has_multiple_event_channels(self):
        if len(self.event_channels) > 1:
            return True


    def has_single_event_channel(self):
        if len(self.event_channels) == 1:
            return True
