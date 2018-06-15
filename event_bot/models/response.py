from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Response(Base):
    __tablename__ = 'response'
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    status = Column(Text)
