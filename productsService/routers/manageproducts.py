from fastapi import APIRouter, HTTPException
import requests
import utils as u
from productsService.data.models import Products, History
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List

ADRESS_CANVA = u.ADRESS_CANVA


class stockClass(BaseModel):
    quantity: int
    type: str


class Item(BaseModel):
    id: int
    stock: Optional[stockClass]
    discPer: Optional[int]


router = APIRouter(
            tags=["manage", "products"]
            )

db_string = u.DB_PATH
engine = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(engine)
session = Session()

stockTypeList = ["A", "RPV", "RPI"]


@router.post("/")
def manage_products(items: List[Item]):
    resDB = session.query(Products).filter(Products.pid.in_([i.id for i in items]))
    pr = resDB.all()
    if pr and len(pr) == len(items): # Id existante
        listRet = []
        for item in items:
            currentProduct = session.query(Products).filter(Products.pid == item.id)
            itemRet = {"id": item.id}
            if item.discPer is not None:
                if item.discPer <= 100 and item.discPer >= 0:
                    r = requests.get(url=ADRESS_CANVA + "tig/product/{}".format(item.id))
                    remoteProduct = r.json()
                    newDiscountPrice = remoteProduct["price"] * (item.discPer*0.01)
                    currentProduct.update({Products.discountPercentage: item.discPer, Products.discount: newDiscountPrice})
                    itemRet["discountPercentage"] = item.discPer
                    itemRet["discount"] = newDiscountPrice
                else:
                    raise HTTPException(status_code=422, detail="On id {} product percentage is <0 or >100".format(item.id))

            if item.stock is not None:
                currentStock = currentProduct.first().quantityInStock
                newStock = currentStock + item.stock.quantity
                flagAv = True
                if newStock < 0:
                    newStock = 0
                    flagAv = False
                currentProduct.update({Products.quantityInStock: newStock, Products.avaible: flagAv})
                itemRet["quantityInStock"] = newStock
                itemRet["availability"] = flagAv
            listRet.append(itemRet)
        session.commit()
        return {"status": "success", "New state": listRet}
    else:
        raise HTTPException(status_code=404, detail="At least one id doesn't match anything")
