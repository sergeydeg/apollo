from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Guild(Base):
    __tablename__ = 'guild'
    id = Column(Integer, primary_key=True)
    prefix = Column(Text)

    event_channels = relationship("EventChannel", passive_deletes=True)
