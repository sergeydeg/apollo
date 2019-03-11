import arrow
from sqlalchemy import BigInteger, Column, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_channel_id = Column(BigInteger, ForeignKey('event_channels.id', ondelete='CASCADE'))
    organizer_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
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
        return arrow.get(self.start_time, 'utc')


    @property
    def accepted_user_ids(self):
        user_ids = self._user_ids_by_status("accepted")
        if self.capacity:
            return user_ids[:self.capacity]
        else:
            return user_ids


    @property
    def declined_user_ids(self):
        return self._user_ids_by_status("declined")


    @property
    def alternate_user_ids(self):
        return self._user_ids_by_status("alternate")


    @property
    def _overflow_user_ids(self):
        accepted_user_ids = self._user_ids_by_status("accepted")
        if self.capacity and len(accepted_user_ids) > self.capacity:
            return accepted_user_ids[self.capacity:]
        else:
            return []


    def _user_ids_by_status(self, status):
        responses = list(filter(lambda r: r.status == status, self.responses))
        responses.sort(key=lambda r: r.last_updated)
        return list(map(lambda r: r.user_id, responses))
