import uuid
from datetime import datetime

from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now)

    investments = relationship('Investment', back_populates='user', lazy='selectin')

class Investment(Base):
    __tablename__ = 'investments'

    investment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    scheme_name = Column(String(255), nullable=False)
    scheme_code = Column(Integer, nullable=False)
    units = Column(Float, nullable=False)
    nav = Column(Float, nullable=False)
    date = Column(TIMESTAMP(timezone=True), default=datetime.now)
    current_value = Column(Float, nullable=False)
    fund_family = Column(String(255), nullable=False)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    user = relationship("User", back_populates="investments")
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now, onupdate=datetime.now)
