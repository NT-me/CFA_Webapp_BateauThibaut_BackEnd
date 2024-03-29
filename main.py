from fastapi import FastAPI
from productsService import pss
from BIService import bis
from security import sec
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)
app_pss = pss.app
app_bis = bis.app
app_sec = sec.app

app.mount("/products", app_pss)
app.mount("/bi", app_bis)
app.mount("/security", app_sec)
