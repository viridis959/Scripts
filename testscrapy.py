import json
from datetime import datetime, timedelta
from time import sleep

import requests, logging, random, urllib, time, datetime as dt
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine


def set_header_user_agent():
    user_agent = UserAgent()
    return user_agent.random


def data_set(st_no,st_na,date,con,con2):
    try:
        sleeptime=random.randint(10,20)
        logging.info(st_na+'->'+urllib.parse.quote(urllib.parse.quote(st_na)))

        url='https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station='+str(st_no)+'&stname='+urllib.parse.quote(urllib.parse.quote(st_na))+'&datepicker='+date
        user_agent = set_header_user_agent()
        headers={
            'User-Agent':user_agent,
            #'keep_alive': 'False',
            'Connection':'close'
        }

        res = requests.get(url,verify=False,headers=headers)
        sleep(sleeptime)
        global count
        count += 1
        logging.info('已請求'+str(count)+'次')
        html=res.text

        soup=bs(html,'html.parser')
        stno=st_no

        if '本段時間區間內無觀測資料！' in soup.text:
            logging.info('本段時間區間內無觀測資料！')
            pass
        else:
            if st_no=='C0V250' or st_no=='C0Z160':

                for tr_index in range(4,27):
                    tr_data=soup.find_all('tr')[tr_index]
                    td_data=tr_data.find_all('td')
                    if tr_data.find('td').text=='24':
                        time=date+"00:00:00"
                        time=datetime.strptime(time,'%Y-%m-%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time=date+tr_data.find('td').text+":00:00"
                        time=datetime.strptime(time,'%Y-%m-%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(st_no+'，'+time+'有資料，開始新增至資料庫')
                    for td_index in range(1,17):
                        td_data[td_index]=td_data[td_index].get_text(strip=True)
                        if(td_data[td_index]== '...' or td_data[td_index]== '/' or td_data[td_index]== 'X'  or  td_data[td_index]== 'T' or td_data[td_index]== 'V'):
                            td_data[td_index]=-9999
                        elif(td_data[td_index]==''):
                            td_data[td_index]='NULL'
                    create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logging.info("==============資料新增時間:"+create_time+"====================")
                    sql = "insert into cwb_data_hr2 (stno,time,PS01,PS02,TX01,TX05,RH01,WD01,WD02,WD05,WD06,PP01,PP02,SS01,SS02,VS01,uvi,CD11,create_time) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s');"%(stno,time,td_data[1],td_data[2],td_data[3],td_data[4],td_data[5],td_data[6],td_data[7],td_data[8],td_data[9],td_data[10],td_data[11],td_data[12],td_data[13],td_data[14],td_data[15],td_data[16],create_time)

                    #logging.info(sql)
                    con2.execute(sql)


            else:

                for tr_index in range(4,28):
                    tr_data=soup.find_all('tr')[tr_index]
                    td_data=tr_data.find_all('td')
                    if tr_data.find('td').text=='24':
                        time=date+"00:00:00"
                        time=datetime.strptime(time,'%Y-%m-%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time=date+tr_data.find('td').text+":00:00"
                        time=datetime.strptime(time,'%Y-%m-%d%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(st_no+'，'+time+'有資料，開始新增至資料庫')
                    for td_index in range(1,17):
                        td_data[td_index]=td_data[td_index].get_text(strip=True)
                        if(td_data[td_index]== '/' or td_data[td_index]== 'X'  or  td_data[td_index]== 'T' or td_data[td_index]== 'V'):
                            td_data[td_index]=-9999
                        elif(td_data[td_index]=='' or td_data[td_index]== '...'):
                            td_data[td_index]='NULL'

                    create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logging.info("==============資料新增時間:"+create_time+"====================")
                    sql2 = "insert into cwb_data_hr2 (stno,time,PS01,PS02,TX01,TX05,RH01,WD01,WD02,WD05,WD06,PP01,PP02,SS01,SS02,VS01,uvi,CD11,create_time) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s');"%(stno,time,td_data[1],td_data[2],td_data[3],td_data[4],td_data[5],td_data[6],td_data[7],td_data[8],td_data[9],td_data[10],td_data[11],td_data[12],td_data[13],td_data[14],td_data[15],td_data[16],create_time)

                    #logging.info(sql2)
                    con2.execute(sql2)
    except:
        logging.exception("=========Exception Logged=============")


def main():
    try:
        global count
        count = 0
        engine = create_engine('mysql+pymysql:' + '//datayoo:*@(!)@&%23@192.168.1.101:3306/' + 'util')
        con = engine.connect()

        engine2 = create_engine('mysql+pymysql:' + '//datayoo:*@(!)@&%23@192.168.1.101:3306/' + 'cwb')
        con2 = engine2.connect()

        FROMAT = '%(asctime)s-%(levelname)s-> %(message)s'
        log_filename = "log/testscrapy/" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.DEBUG, filename=log_filename, format=FROMAT)
        with open('cwb_data_hr.json', 'r') as reader:
            jf = json.loads(reader.read())
        sta_list = []
        for i in jf:
            stno = i['stno']
            if stno != 'CM0180':
                tmp = con2.execute(f"select st_name from cwb_station_status where stno = '{stno}'").fetchone()
                sta_list.append([tmp[0], stno])

        print(sta_list)
        st_na = []
        st_no = []

        for i in range(len(sta_list)):
            st_na.append(sta_list[i][0])
            st_no.append(sta_list[i][1])

        # 將時間及氣象站帶入

        today = datetime.today()
        date = today + timedelta(days=-2)
        date = date.strftime('%Y-%m-%d')
        start = today.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("================開始爬蟲時間:" + start + "==================")

        date_tmp = '2019-08-01'
        endDate = '2020-03-31'
        for k, l in zip(st_no, st_na):
            while date_tmp != endDate:
                logging.info(str(k) + ',' + str(l) + ',' + str(date_tmp))
                data_set(k, l, date_tmp, con, con2)
                date_tmp = str((dt.datetime.strptime(date_tmp, '%Y-%m-%d') + dt.timedelta(days=1)).strftime('%Y-%m-%d'))
            data_set(k, l, endDate, con, con2)

        finish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info("====================爬蟲結束,結束時間:" + finish + "======================")

        con.close()
        con2.close()
    except:
        logging.exception("=========Exception Logged=============")


if __name__ == "__main__":
    main()