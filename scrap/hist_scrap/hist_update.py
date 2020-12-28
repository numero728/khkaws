import pymysql
from hist_data_get import *
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as BS
import lxml
import pandas as pd
import re

# 상장기업 리스트 가져오기
def pub_list():
    try:
        conn_=pymysql.connect(
                            host='khk.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com',
                            user='khk',
                            password='k2hyokwang2!',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                            port=3306,
                            db='scrap_data'
        )

        with conn_.cursor() as cursor:
            sql='SELECT 종목코드 FROM pubCorp;'
            cursor.execute(sql)
            rows_=cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        conn_.close()
    corp_list=[code.get('종목코드') for code in rows_]
    return corp_list

# 최근 주가 정보 획득(page=1)
def recent_price(stock_code):
    url_for_first=f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}'
    req=requests.get(url_for_first)
    soup=BS(req.content,'lxml')
    tbl=soup.select_one('table')
    rows=tbl.select('tr')
    head=rows[0].select('th')
    cols=[col.text for col in head]
    body=rows[2:]
    vals=[[td.text for td in tr.select('td')] for tr in body]
    data=pd.DataFrame(vals,columns=cols)
    data=data[data['날짜']!='']
    data=data.sort_values('날짜',ascending=True)
    data['전일비']=data['전일비'].apply(lambda x: type(x)==type('x') and re.sub('\n','',x) or 'None')
    data['전일비']=data['전일비'].apply(lambda x: type(x)==type('x') and re.sub('\t','',x) or 'None')
    try:
        conn_=pymysql.connect(
                            host='khk.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com',
                            user='khk',
                            password='k2hyokwang2!',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,
                            port=3306,
                            db='hist_data'
        )

        with conn_.cursor() as cursor:
            sql=f'SELECT * FROM `{stock_code}`;'
            cursor.execute(sql)
            db_table=cursor.fetchall()
        
    except Exception as e:
        print(e)
    finally:
        conn_.close()

    try:
        db_table=pd.DataFrame(db_table)
        db_table=db_table[db_table['날짜']!='\xa0']
        scrap=db_table['날짜'].tolist()
        data=data[data.apply(lambda x: x['날짜'] not in scrap, axis=1)]
        db_table=pd.concat([db_table,data],axis=0)
        from sqlalchemy import create_engine
        dialect='mysql'
        driver='pymysql'
        database='hist_data'
        server='khk.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com'
        username='khk'
        password='k2hyokwang2!'
        port='3306'
        db_url=f'{dialect}+{driver}://{username}:{password}@{server}:{port}/{database}'
        engine=create_engine(db_url)
        conn=engine.connect()
        db_table.to_sql(stock_code,conn,if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(e)
        

if __name__=='__main__':
    publist=pub_list()
    for code in tqdm(publist):
        recent_price(code)
    