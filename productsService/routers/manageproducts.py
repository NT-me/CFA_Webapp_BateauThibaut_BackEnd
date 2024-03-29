from fastapi import APIRouter, HTTPException, Request, Depends
import requests
import utils as u
from productsService.data.models import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List

ADRESS_CANVA = u.ADRESS_CANVA


class stockClass(BaseModel):
    quantity: int
    price: int
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

stockTypeList = u.LIST_BI_KEYWORDS


@router.patch("/")
async def manage_products(items: List[Item],
request: Request,
Auth: str = Depends(u.testAuth)):
    resDB = session.query(Products).filter(Products.pid.in_([i.id for i in items]))
    HTTPRet = {"status": "success"}

    pr = resDB.all()
    if pr and len(pr) == len(items): # Id existante
        listRet = []
        listJSON = []
        for item in items:
            currentProduct = session.query(Products).filter(Products.pid == item.id)
            itemRet = {"id": item.id}
            r = requests.get(url=ADRESS_CANVA + "tig/product/{}".format(item.id))
            remoteProduct = r.json()

            if item.discPer is not None:
                if item.discPer <= 100 and item.discPer >= 0:
                    newDiscountPrice = round((remoteProduct["price"] * (1-(item.discPer*0.01))), 2)
                    currentProduct.update({Products.discountPercentage: item.discPer, Products.discount: newDiscountPrice})
                    itemRet["discountPercentage"] = item.discPer
                    itemRet["discount"] = newDiscountPrice
                    session.commit()

                else:
                    raise HTTPException(status_code=422, detail="On id {} product percentage is <0 or >100".format(item.id))

            if item.stock is not None:
                currentStock = currentProduct.first().quantityInStock
                if item.stock.type == "A":
                    newStock = currentStock + item.stock.quantity
                else:
                    newStock = currentStock - item.stock.quantity

                if item.stock.type == "RPV" and (not currentProduct.first().avaible or newStock < 0):
                    # raise HTTPException(status_code=403, detail="You cannot sell product you don't have, check id:{}".format(item.id))
                    itemRet["Error"] = "You cannot sell product you don't have, check id:{}".format(item.id)
                else:
                    flagAv = True
                    if newStock < 0:
                        item.stock.quantity = currentStock
                        newStock = 0
                        flagAv = False
                    currentProduct.update({Products.quantityInStock: newStock, Products.avaible: flagAv})
                    itemRet["quantityInStock"] = newStock
                    itemRet["availability"] = flagAv

                    reqJSON = {"pid": currentProduct.first().pid,
                    "price": item.stock.price,
                    "quantity": item.stock.quantity,
                    "type": item.stock.type,
                    "unitprice": remoteProduct["price"],
                    "sale": currentProduct.first().sale,
                    "discount": currentProduct.first().discount}

                    listJSON.append(reqJSON)
                    session.commit()

            listRet.append(itemRet)
            HTTPRet["New state"] = listRet
        if listJSON:
            headers = {'Connection': 'close', 'Auth': Auth}
            ret = requests.put(url=u.localAPIAdress(request)+"/bi/info/history", json=listJSON, headers=headers)
            HTTPRet["BI Return"] = ret.json()
        return HTTPRet

    else:
        raise HTTPException(status_code=404, detail="At least one id doesn't match anything")
