import sqlite3 as sql
import requests as req
import random
import sys


if __name__ == "__main__":
    if not sys.argv[1]:
        NB_ITER = 1000
    else:
        NB_ITER = int(sys.argv[1])

    conn = sql.connect('BIService/BIServiceDB.db')

    prList = req.get(url="http://loutre-duveteuse.fr.nf/products/info/all")
    typesList = ["RPV", "RPI", "A"]
    prList = prList.json()
    prQt = {}

    for i in range(0, NB_ITER):
        sqlReq = "INSERT INTO \"transactions\"(\"pid\",\"time\",\"type\",\"totalPrice\",\"quantity\",\"sale\")"
        # sqlReq += "VALUES (7,1618935910.67476,"RPI",0,10,1)"
        currentPr = random.choice(prList)
        # print(currentPr)
        id = currentPr["id"]
        sale = 1 if currentPr["sale"] else 0
        unitPrice = currentPr["price"]
        sellPrice = unitPrice + 10
        type = random.choices(typesList, weights=(5, 1, 3))

        quantity = random.randint(1, 100)

        time = random.randint(1514800539, 1609494939)
        quantity_ = -quantity

        try:
            actualQt = prQt[id]
        except :
            actualQt = 0

        if (actualQt - quantity) <= 0:
            type = 'A'
            quantity = abs(actualQt) + 1

        if type == "A":
            totalPrice = quantity * unitPrice
            quantity_ = quantity
        elif type == "RPV":
            totalPrice = quantity * sellPrice
        else:
            totalPrice = 0

        try:
            prQt[id] += quantity_
        except :
            prQt[id] = quantity_

        sqlReq += "VALUES ({0},{1},\"{2}\",{3},{4},{5})".format(id, time, type[0], totalPrice, quantity, sale)
        print(sqlReq)
        conn.execute(sqlReq)
    conn.commit()
    conn.close()

    print(prQt)
    conn2 = sql.connect('productsService/productsServiceDB.db')

    for item in prQt:
        sqlReqUpdate = "UPDATE \"products\" SET \"quantityInStock\"={0} WHERE \"pid\"={1}".format(prQt[item], item)
        print(sqlReqUpdate)
        conn2.execute(sqlReqUpdate)
    conn2.commit()
