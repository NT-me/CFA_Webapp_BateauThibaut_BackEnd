from fastapi import Request

ADRESS_CANVA = "http://51.255.166.155:1352/"
DB_PATH = "sqlite:///productsService/productsServiceDB.db"
DB_BI_PATH = "sqlite:///BIService/BIServiceDB.db"


def localAPIAdress(request: Request):
    ADRESS = "http://localhost"
    PORT = str(request.url.port)

    if not PORT:
        PORT = "80"

    return ADRESS + ':' + PORT
