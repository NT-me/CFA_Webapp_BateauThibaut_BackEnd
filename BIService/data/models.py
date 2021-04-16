from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Float, Column, Integer,  UniqueConstraint
Base = declarative_base()


class Transactions(Base):
    __tablename__ = "transactions"
    pk = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    pid = Column(Integer)
    time = Column(Float)
    type = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    __table_args__ = ((UniqueConstraint('pid', 'time')), UniqueConstraint('pk'))
