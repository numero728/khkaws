
import requests
import html5lib
from bs4 import BeautifulSoup as BS
import pandas as pd

#-----------------------------------------------------------------------------

url='https://dev-kind.krx.co.kr/corpgeneral/corpList.do'
param={
    'method':'download',
    'pageIndex':1,
    'currentPageSize':5000,
    'orderMode':3,
    'orderStat':'D',
    'searchType':13,
    'marketType':'stockMkt',
    'fiscalYearEnd':'all',
    'location':'all'
    }

res=requests.post(url,data=param)

#-----------------------------------------------------------------------------

soup=BS(res.content,'lxml')
tbl=soup.select_one('table')

#-----------------------------------------------------------------------------

rows=tbl.select('tr')
head=rows[0]
body=rows[1:]

#-----------------------------------------------------------------------------

th_columns=head.select('th')
columns=[col_.text for col_ in th_columns]
var_list=[[col_.text for col_ in body_.select('td')] for body_ in body]
table=pd.DataFrame(var_list,columns=columns)
print('요청 정상적으로 수행')

#-----------------------------------------------------------------------------

from sqlalchemy import create_engine
import pymysql
conn=''
try:
    dialect='mysql'
    driver='pymysql'
    database='scrap_data'
    server='khk.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com'
    username='khk'
    password='k2hyokwang2!'
    port='3306'
    db_url=f'{dialect}+{driver}://{username}:{password}@{server}:{port}/{database}'
    engine=create_engine(db_url)
    conn=engine.connect()
    table.to_sql('코스피상장기업',conn,if_exists='replace',index=False)
    print('작업 정상적으로 수행 완료')
except Exception as e:
    print(e)
finally:
    conn.close()
