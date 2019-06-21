from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Response(Base):
    __tablename__ = "responses"
    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    status = Column(Text)
    last_updated = Column(DateTime)
