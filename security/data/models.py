from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Boolean, Float, Column, Integer,  UniqueConstraint


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, autoincrement='ignore_fk')
    hashed_password = Column(String)
    email = Column(String)
    full_name = Column(String)
    active = Column(Boolean)
    # __table_args__ = (UniqueConstraint('username'),)
