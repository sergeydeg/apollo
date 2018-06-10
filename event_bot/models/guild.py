from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Guild(Base):
    __tablename__ = 'guild'
    id = Column(Integer, primary_key=True)

    event_channels = relationship("EventChannel", passive_deletes=True)
