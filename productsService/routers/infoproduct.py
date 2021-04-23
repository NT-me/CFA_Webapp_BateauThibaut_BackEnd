from fastapi import APIRouter, HTTPException, Header, Depends, Request, status
import requests
import utils as u
from productsService.data.models import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional


ADRESS_CANVA = u.ADRESS_CANVA

router = APIRouter(
            prefix="/info",
            tags=["infoproducts", "products"]
            )

db_string = u.DB_PATH
engine = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(engine)
session = Session()

categorysList = ["POI", "CRU", "COQ"]


def testAuth(request: Request, Auth: str = Header(None)):
    headers = {'Authorization': Auth}
    print(Auth)
    ret = requests.get(url=u.localAPIAdress(request)+"/security/pswd/users/test/", headers=headers)
    ret = ret.json()
    if ret["detail"] is True:
        return True
    else:
        return True
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )


@router.get("/all")
async def show_all_products(request: Request,
category: Optional[str] = None,
availability: Optional[bool] = None,
sale: Optional[bool] = None):
# Auth: str = Depends(testAuth)
    resDB = session.query(Products)
    res = []

    if category is not None:
        if category in categorysList:
            resDB = list(filter(lambda x: x.category == category, resDB))

    if availability is not None:
        resDB = list(filter(lambda x: x.avaible == availability, resDB))

    if sale is not None:
        resDB = list(filter(lambda x: x.sale == sale, resDB))

    for item in resDB:
        r = requests.get(url=ADRESS_CANVA + "tig/product/{}".format(item.pid))
        ret = r.json()

        ret["quantityInStock"] = item.quantityInStock
        res.append(item.retValue(r.json()))
    return res


@router.get("/{id}")
async def show_one_product(id,
Auth: str = Depends(testAuth)
):
    resDB = session.query(Products).filter(Products.pid == id)
    if resDB.all():
        r = requests.get(url=ADRESS_CANVA + "tig/product/{}".format(id))
        try:
            if r.json()["detail"] == "Not found.":
                raise HTTPException(status_code=404, detail="Item not found")
        except KeyError:
            pass
        return resDB.first().retValue(r.json())
    else:
        raise HTTPException(status_code=404, detail="Item not avaible")
