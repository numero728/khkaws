
#-----------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import lxml
import re
from tqdm import tqdm

#-----------------------------------------------------------------------------

def main(stock_code):
    last=get_last(stock_code)
    head=get_head(stock_code)

    list_chain=list()
    page_list=[x for x in range(1,int(last)+1)]
    data_list=list(map(lambda x: list_chain.extend(x),list(map(row_return,[stock_code for i in range(int(last))],[d for d in range(1,int(last)+1)]
    ))))
    data=pd.DataFrame(list_chain, columns=head)

    data=data[data['날짜']!='']
    data=data.sort_values('날짜',ascending=True)
    data['전일비']=data['전일비'].apply(lambda x: type(x)==type('x') and re.sub('\n','',x) or 'None')
    data['전일비']=data['전일비'].apply(lambda x: type(x)==type('x') and re.sub('\t','',x) or 'None')
    conn=''
    try:
        import pymysql
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
        data.to_sql(stock_code,conn,if_exists='replace', index=False)
        print('작업 완료')
    except Exception as e:
        print(e)
    finally:
        conn.close()

#-----------------------------------------------------------------------------

def get_last(stock_code):
    url_for_last=f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}'
    req=requests.get(url_for_last)
    soup=BS(req.content,'lxml')
    nav=soup.select_one('.Nnavi')
    td=nav.select('td')
    last_href=td[-1].select_one('a').attrs['href']
    last_page=re.sub('page=','',re.search('page=\d+',last_href).group())
    return last_page

#-----------------------------------------------------------------------------

def get_head(stock_code):
    url_for_head=f'https://finance.naver.com/item/sise_day.nhn?code=005930&page=1'
    req=requests.get(url_for_head)
    soup=BS(req.content,'lxml')
    tbl=soup.select_one('table')
    rows=tbl.select('tr')
    head=rows[0].select('th')
    cols=[col.text for col in head]
    return cols

#-----------------------------------------------------------------------------

def row_return(stock_code,pageNo):
    page_url=f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page={pageNo}'
    page_row=requests.get(page_url)
    page_soup=BS(page_row.content,'lxml')
    page_tbl=page_soup.select_one('table')
    page_t_rows=page_tbl.select('tr')
    page_body=page_t_rows[1:]
    page_rows=[[td.text for td in row_.select('td')] for row_ in page_body][1:]
    return page_rows

#-----------------------------------------------------------------------------

if __name__ =='__main__':
    main('005930')
    