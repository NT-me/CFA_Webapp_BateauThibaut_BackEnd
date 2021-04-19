from fastapi import APIRouter, HTTPException, Request
import requests
import utils as u
from BIService.data.models import Transactions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from pydantic import BaseModel
import time


ADRESS_CANVA = u.ADRESS_CANVA

router = APIRouter(
            prefix="/info",
            tags=["infoproducts", "products"]
            )

db_string = u.DB_BI_PATH
engine = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(engine)
session = Session()


@router.get("/history/all")
def return_informations_about_transactions(request: Request, startInterval: Optional[int] = None,
endInterval: Optional[int] = None,
category: Optional[str] = None,
availability: Optional[bool] = None,
sale: Optional[bool] = None):

    resDB = session.query(Transactions)

    if startInterval is not None:
        resDB.filter(Transactions.time >= startInterval)

    if endInterval is not None:
        resDB.filter(Transactions.time <= endInterval)

    if (category is not None) or (availability is not None) or (sale is not None):
        reqURL_BASE = "http://localhost:{0}/products/info/all?".format(request.url.port)
        flag = False
        if category is not None:
            reqURL_BASE += "category={0}".format(category)
            flag = True
        if availability is not None:
            if flag:
                reqURL_BASE += '&'
            else:
                flag = True
            reqURL_BASE += "availability={0}".format(availability)
        if sale is not None:
            if flag:
                reqURL_BASE += '&'
            else:
                flag = True
            reqURL_BASE += "sale={0}".format(sale)

        r = requests.get(url=reqURL_BASE)

    ret = resDB.all()

    if ret:
        return ret
    else:
        raise HTTPException(status_code=404, detail="No transactions were found in these dates")


class ItemTransact(BaseModel):
    pid: int
    price: int
    quantity: int
    type: str
    unitprice: int
    sale: bool
    discount: float


@router.post("/history")
def add_new_transaction(listTransactions: List[ItemTransact]):
    retList = []
    for item in listTransactions:
        flagOkstl = False
        if item.type == "A":
            flagOkstl = True
            if item.sale:
                rpPrice = item.discount
            else:
                rpPrice = item.price
            rpPrice *= item.quantity
        elif item.type == "RPI":
            flagOkstl = True
            rpPrice = 0
        elif item.type == "RPV":
            flagOkstl = True
            rpPrice = item.price

        if flagOkstl:
            ts = time.time()
            tr = Transactions(pid=item.pid, time=ts, type=item.type, totalPrice=rpPrice, quantity=item.quantity)
            retList.append({"State": "Success", "id": item.pid, "Comment": "Transaction saved"})
        else:
            retList.append({"State": "Error on type", "id": item.pid, "Comment": "Type need to be A, RPI or RPV"})

        session.add(tr)

    session.commit()
    return retList
