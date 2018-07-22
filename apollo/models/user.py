from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    events = relationship("Event", back_populates="organizer")
