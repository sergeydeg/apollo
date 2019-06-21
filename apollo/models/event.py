import arrow
from sqlalchemy import BigInteger, Column, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_channel_id = Column(
        BigInteger, ForeignKey("event_channels.id", ondelete="CASCADE")
    )
    organizer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    message_id = Column(BigInteger)
    title = Column(Text)
    description = Column(Text)
    start_time = Column(DateTime)
    time_zone = Column(Text)
    capacity = Column(Integer)
    organizer = relationship("User", back_populates="events")
    responses = relationship("Response", passive_deletes=True)
    event_channel = relationship("EventChannel", back_populates="events")

    @property
    def local_start_time(self):
        return self.utc_start_time.to(self.time_zone)

    @property
    def utc_start_time(self):
        return arrow.get(self.start_time, "utc")
