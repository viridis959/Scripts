import os
import environ
from sqlalchemy import create_engine
from datetime import datetime, timedelta

env = environ.Env()
env.read_env()

engine = create_engine(os.getenv('DB'))
con = engine.connect()

sqlOne = (f"SELECT stno, time \
    FROM cwb_data_hr \
    WHERE SUBSTRING(time, 12, 8) = '00:00:00' \
    GROUP BY stno, time \
    HAVING COUNT(*) = 24")

resultProxy = con.execute(sqlOne)
li = list(resultProxy)

for i in li:
    sqlTwo = (f"SELECT stno, time, create_time \
    FROM cwb_data_hr \
    WHERE stno = '{i[0]}' AND time = '{i[1]}' AND create_time != null \
    ORDER BY create_time ASC")
    li2 = list(con.execute(sqlTwo))
    count = 0
    for j in li2:
        sqlThree = f"UPDATE cwb_data_hr \
        SET time = '{j[1] + timedelta(hours=count)}' \
        WHERE stno = '{j[0]}' AND time = '{j[1]}' AND create_time = '{j[2]}'"
        con.execute(sqlThree)
        count += 1
con.close()
