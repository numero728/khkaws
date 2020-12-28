import pymysql
import pandas as pd
import numpy as np

#-----------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------

