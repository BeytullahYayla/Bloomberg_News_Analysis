from sqlalchemy import Boolean, Double, Column, DateTime, ForeignKey, Float, Integer, String, UUID, CHAR, Table, LargeBinary, BLOB
from connect_database import Base
from datetime import datetime
from uuid import uuid4

class New(Base):

    
    __tablename__ = "news"
    
    id = Column(CHAR(36), primary_key=True, index=True, default=uuid4, unique=True, nullable=False)
    title=Column(String(255),nullable=False)
    description=Column(String(255),nullable=False)
    sentiment=Column(String(255),nullable=False)
    publish_date=Column(String(255),nullable=False)
    
    
    
    