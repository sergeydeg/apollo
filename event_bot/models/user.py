from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    events = relationship("Event", back_populates="organizer")
