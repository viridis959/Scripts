import os
import time
import uuid
from datetime import datetime

import environ

import pandas as pd
from sqlalchemy import create_engine

path = '/users/viridis/downloads/'
path += '2020-02綠冠採收資料彙整 - 2_田間操作紀錄.csv'
df = pd.read_csv(path)
df = df.drop(index=0).reset_index().drop(columns="index")

env = environ.Env()
env.read_env()

engine = create_engine(os.getenv('TEST_DB'))
con = engine.connect()

thisYearOrNot = False
startDateOrNot = False
eightFieldId = {'A': 112, 'B': 110, 'C': 111, 'D': 113, 'E': 125, 'F': 126, 'G': 114}
otherFieldId = {'F5': 143, 'F11': 140}
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
year = 2020
for index, row in df.iterrows():
    if row['日期'] == str(year):
        thisYearOrNot = True
    if row['日期'] == str(year + 1):
        break
    if thisYearOrNot:
        # if row['日期'] == '10/22':
        startDateOrNot = True
    if startDateOrNot and pd.notnull(row['作業種類']):
        workType = int(row['作業種類'][0:2])
        tmp = time.strptime(row['日期'], u"%m/%d")
        monthDate = time.strftime("%m-%d", tmp)
        farmworkDate = f"{str(year)}-{monthDate}"
        if pd.notnull(row['備註']):
            remarks = row['備註']
        else:
            remarks = ''
        if workType < 7:
            workType += 1

        """
        if row['區域'] == 'F8':
            if pd.notnull(row['小區']):
                checkList = []
                for el in list(row['小區']):
                    if el in eightFieldId and el not in checkList:
                        sqlEight = f"INSERT INTO field_farmwork (field_id, farmwork_date, record, remarks, work_type, create_time, update_time, uuid) " \
                                   f"VALUES ('{eightFieldId[el]}', '{farmworkDate}', '{row['工作內容']}', '{remarks}', '{workType}', '{now}', '{now}', '{str(uuid.uuid4()).replace('-', '')}')"
                        con.execute(sqlEight)
                        checkList.append(el)
            else:
                for key in eightFieldId:
                    sqlEight = f"INSERT INTO field_farmwork (field_id, farmwork_date, record, remarks, work_type, create_time, update_time, uuid) " \
                               f"VALUES ('{eightFieldId[key]}', '{farmworkDate}', '{row['工作內容']}', '{remarks}', '{workType}', '{now}', '{now}', '{str(uuid.uuid4()).replace('-', '')}')"
                    con.execute(sqlEight)
        """

        if row['區域'] == 'F5' or row['區域'] == 'F11':
            sqlEight = f"INSERT INTO field_farmwork (field_id, farmwork_date, record, remarks, work_type, create_time, update_time, uuid) " \
                       f"VALUES ('{otherFieldId[row['區域']]}', '{farmworkDate}', '{row['工作內容']}', '{remarks.replace('%', '%%')}', '{workType}', '{now}', '{now}', '{str(uuid.uuid4()).replace('-', '')}')"
            con.execute(sqlEight)
        if pd.notnull(row['區域']) and len(row['區域']) > 3:
            print(row['區域'])
            for i in eightFieldId:
                sqlEight = f"INSERT INTO field_farmwork (field_id, farmwork_date, record, remarks, work_type, create_time, update_time, uuid) " \
                           f"VALUES ('{eightFieldId[i]}', '{farmworkDate}', '{row['工作內容']}', '{remarks.replace('%', '%%')}', '{workType}', '{now}', '{now}', '{str(uuid.uuid4()).replace('-', '')}');"
                print(sqlEight)
            print('-----')
            for j in otherFieldId:
                sqlEight = f"INSERT INTO field_farmwork (field_id, farmwork_date, record, remarks, work_type, create_time, update_time, uuid) " \
                           f"VALUES ('{otherFieldId[j]}', '{farmworkDate}', '{row['工作內容']}', '{remarks.replace('%', '%%')}', '{workType}', '{now}', '{now}', '{str(uuid.uuid4()).replace('-', '')}');"
                print(sqlEight)
            print('----------')

con.close()
