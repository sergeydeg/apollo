from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Response(Base):
    __tablename__ = 'response'
    event_id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    status = Column(Text)
