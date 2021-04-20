from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, UniqueConstraint, ForeignKey
Base = declarative_base()


class Products(Base):
    __tablename__ = "products"
    pk = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    pid = Column(Integer)
    avaible = Column(Integer)
    sale = Column(Integer)
    category = Column(String)
    quantityInStock = Column(Integer)
    discountPercentage = Column(Integer)
    discount = Column(Float)
    __table_args__ = (UniqueConstraint('pk'), UniqueConstraint('pid'))

    def retValue(self, remoteJSON):
        remoteJSON["discountPercentage"] = self.discountPercentage
        remoteJSON["discount"] = self.discount
        remoteJSON["sale"] = bool(self.sale)
        remoteJSON["quantityInStock"] = self.quantityInStock
        return remoteJSON
