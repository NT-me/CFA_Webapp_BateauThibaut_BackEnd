from fastapi import APIRouter, HTTPException
import requests
import utils as u
from productsService.data.models import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List

ADRESS_CANVA = u.ADRESS_CANVA


class Item(BaseModel):
    id: int
    stock: Optional[int]
    discPer: Optional[int]


router = APIRouter(
            tags=["manage", "products"]
            )

db_string = u.DB_PATH
engine = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(engine)
session = Session()


@router.post("/")
def manage_products(items: List[Item]):
    resDB = session.query(Products).filter(Products.pid.in_([i.id for i in items]))
    pr = resDB.all()
    if pr and len(pr) == len(items): # Id existante
        for item in items:
            currentProduct = session.query(Products).filter(Products.pid == item.id)

            if item.discPer is not None:
                if item.discPer <= 100 and item.discPer >= 0:
                    newDiscountPrice = currentProduct.price * (item.discPer*0.01)
                    currentProduct.update({Products.discountPercentage: item.discPer, Products.discount: newDiscountPrice})
                else:
                    raise HTTPException(status_code=422, detail="On id {} product percentage is <0 or >100".format(item.id))

            if item.stock is not None:
                currentStock = currentProduct.first().quantityInStock
                newStock = currentStock + item.stock
                flagAv = True
                if newStock < 0:
                    newStock = 0
                    flagAv = False
                currentProduct.update({Products.quantityInStock: newStock, Products.avaible: flagAv})
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="At least one id doesn't match anything")
