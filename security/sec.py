import utils as u
from fastapi import FastAPI, Depends
from security.routers import passwordmanager
# from productsService.tasks import fetchData as fd
from security.data.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()
BASE_URL = u.ADRESS_CANVA

db_string = u.DB_SEC_PATH
db_sal = create_engine(db_string, connect_args={'check_same_thread': False})
Session = sessionmaker(db_sal)
session = Session()
Base.metadata.create_all(db_sal)

app.include_router(passwordmanager.router)


@app.get("/helloworld")
async def read_root():
    return {"Hello": "World"}
