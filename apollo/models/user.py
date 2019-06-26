from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    time_zone = Column(String)
    events = relationship("Event", back_populates="organizer")
