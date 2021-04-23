from fastapi import APIRouter, HTTPException, Request
import requests
import utils as u
from BIService.data.models import Transactions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from pydantic import BaseModel
import time
from datetime import date, datetime


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
async def return_informations_about_transactions(request: Request, startInterval: Optional[int] = None,
endInterval: Optional[int] = None,
category: Optional[str] = None,
availability: Optional[bool] = None,
sale: Optional[bool] = None,
type: Optional[str] = None,
revenue: Optional[bool] = None
):
    reqURL_BASE = u.localAPIAdress(request)+"/products/info/all"
    resDB = session.query(Transactions)
    headers = {'Connection': 'close'}
    if startInterval is not None:
        resDB = resDB.filter(Transactions.time >= startInterval)

    if endInterval is not None:
        resDB = resDB.filter(Transactions.time <= endInterval)

    if type is not None:
        if type in u.LIST_BI_KEYWORDS:
            resDB = resDB.filter(Transactions.type == type)
        else:
            raise HTTPException(status_code=422, detail="Type not exist")

    if (category is not None) or (availability is not None) or (sale is not None):
        flag = False
        reqURL_BASE += '?'
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

        r = requests.get(url=reqURL_BASE, headers=headers).json()
        resDB = resDB.filter(Transactions.pid.in_([json["id"] for json in r]))
    else:
        r = requests.get(url=reqURL_BASE, headers=headers).json()

    retDB = resDB.all()

    transactList = []
    for tran in retDB:
        name = [pr["name"] for pr in r if pr["id"] == tran.pid][0]
        tran = tran.__dict__
        tran["name"] = name
        transactList.append(tran)
    ret = {"transactions": transactList}

    if revenue is not None:
        rpvList = [x.totalPrice for x in retDB if x.type == "RPV"]
        aList = [x.totalPrice for x in retDB if x.type == "A"]
        ca = sum(rpvList)
        marge = ca - sum(aList)
        ret["relative revenue"] = {}
        ret["relative revenue"]["turnover"] = ca
        ret["relative revenue"]["margin"] = marge

    if retDB:
        return ret
    else:
        raise HTTPException(status_code=404, detail="No transactions were found in these dates with these filters")


class ItemTransact(BaseModel):
    pid: int
    price: int
    quantity: int
    type: str
    unitprice: int
    sale: bool
    discount: float


@router.put("/history")
async def add_new_transaction(listTransactions: List[ItemTransact]):
    retList = []
    for item in listTransactions:
        flagOkstl = False
        if item.type == "A":
            flagOkstl = True
            if item.sale:
                rpPrice = item.discount
            else:
                rpPrice = item.unitprice
            rpPrice *= item.quantity
        elif item.type == "RPI":
            flagOkstl = True
            rpPrice = 0
        elif item.type == "RPV":
            flagOkstl = True
            rpPrice = item.price

        if flagOkstl:
            ts = time.time()
            tr = Transactions(pid=item.pid,
            time=ts,
            type=item.type,
            totalPrice=rpPrice,
            sale=item.sale,
            quantity=item.quantity)

            retList.append({"State": "Success", "id": item.pid, "Comment": "Transaction saved"})
        else:
            retList.append({"State": "Error on type", "id": item.pid, "Comment": "Type need to be A, RPI or RPV"})

        session.add(tr)

    session.commit()
    return retList


@router.get("/accountingresult")
async def show_accounting_result(year: Optional[int] = date.today().year):
    fstDay = datetime(year, 1, 1, 0, 0)
    lstDay = datetime(year, 12, 31, 23, 59)

    tsFstDay = time.mktime(fstDay.timetuple())
    tsLstDay = time.mktime(lstDay.timetuple())

    resDB = session.query(Transactions).filter(Transactions.time >= tsFstDay, Transactions.time <= tsLstDay)
    retDB = resDB.all()
    if len(retDB) > 0:
        rpvList = [x.totalPrice for x in retDB if x.type == "RPV"]
        aList = [x.totalPrice for x in retDB if x.type == "A"]
        ca = sum(rpvList)
        benef = ca - sum(aList)
        if benef > 0:
            mntImpot = benef * 0.3
        else:
            mntImpot = 0
        resulting = benef - mntImpot

        return {"year": year, "turnover": ca, "profit": benef, "taxes": mntImpot, "result": resulting}
    else:
        raise HTTPException(status_code=404, detail="No transactions were found this year")
