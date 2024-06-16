from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    source = Column(String, index=True)
    data = Column(JSONB)
    created_at = Column(DateTime)
