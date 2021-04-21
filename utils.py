from fastapi import Request

ADRESS_CANVA = "http://51.255.166.155:1352/"
DB_PATH = "sqlite:///productsService/productsServiceDB.db"
DB_BI_PATH = "sqlite:///BIService/BIServiceDB.db"
DB_SEC_PATH = "sqlite:///security/userpswdDB.db"
LIST_BI_KEYWORDS = ["A", "RPV", "RPI"]

f = open("security/key.key", "r")
SECRET_KEY = f.read().split("\n")[0]


def localAPIAdress(request: Request):
    ADRESS = "http://localhost"
    PORT = str(request.url.port)

    if PORT == "None":
        PORT = "80"

    return ADRESS + ':' + PORT
