from fastapi import FastAPI
from productsService import pss
# from BIService import bis


app = FastAPI()
app_pss = pss.app
# app_bis = bis.app

app.mount("/products", app_pss)
# app.mount("/bi", app_bis)
