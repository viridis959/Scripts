import os
import environ
from sqlalchemy import create_engine

env = environ.Env()
env.read_env()

engine = create_engine(os.getenv('DB'))
con = engine.connect()

sqlOne = ("SELECT DISTINCT stno \
           FROM cwb_data_hr \
           WHERE SUBSTRING(time, 1, 10) = '2020-03-01'")
resultProxy = con.execute(sqlOne)
li = list(resultProxy)

for i in li:
    checkList = []
    li2 = list(con.execute(f"SELECT * \
           FROM cwb_data_hr \
           WHERE SUBSTRING(time, 1, 10) = '2020-03-01' AND stno = '{i[0]}'"))
    if len(li2) > 24:
        for j in li2:
            changeOrNot = False
            if checkList:
                for k in checkList:
                    if k[1] == j[1]:
                        changeOrNot = True
                        if k == j[:-1]:
                            sqlTwo = f"DELETE \
                       FROM cwb_data_hr \
                       WHERE time = '{j[1]}' AND stno = '{i[0]}' AND create_time = '{j[-1]}'"
                            con.execute(sqlTwo)
                        break
                if not changeOrNot:
                    checkList.append(j[:-1])
            else:
                checkList.append(j[:-1])
con.close()
