from fastapi import APIRouter, HTTPException
import requests
import utils as u
from productsService.data.models import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional


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
def manage_products(item: Item):
    return item
