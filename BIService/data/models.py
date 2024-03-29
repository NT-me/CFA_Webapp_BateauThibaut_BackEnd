from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Boolean, Float, Column, Integer,  UniqueConstraint
Base = declarative_base()


class Transactions(Base):
    __tablename__ = "transactions"
    pk = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    pid = Column(Integer)
    time = Column(Float)
    type = Column(String)
    totalPrice = Column(Integer)
    quantity = Column(Integer)
    sale = Column(Boolean)
    __table_args__ = ((UniqueConstraint('pid', 'time')), UniqueConstraint('pk'))
