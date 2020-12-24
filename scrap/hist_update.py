import pymysql
from hist_data_get import *
from tqdm import tqdm

conn_=''
try:
    conn_=pymysql.connect(
                        host='khk.cepsu2i8bkn5.ap-northeast-2.rds.amazonaws.com',
                        user='khk',
                        password='k2hyokwang2!',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        port=3306,
                        db='information_schema'
    )

    with conn_.cursor() as cursor:
        sql='SELECT TABLE_NAME FROM TABLES WHERE TABLES.TABLE_SCHEMA="hist_data";'
        cursor.execute(sql)
        rows=cursor.fetchall()
    
except Exception as e:
    print(e)
finally:
    conn_.close()

corp_code=[x.get('TABLE_NAME') for x in rows]


conn_=''
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

target_list=[x.get('종목코드') for x in rows_]
target_list=list(filter(lambda x:x not in corp_code and True or False,target_list))
print(len(target_list))
for i in tqdm(target_list[0:100]):
    main(i)
    