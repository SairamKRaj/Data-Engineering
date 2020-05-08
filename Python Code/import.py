import pymysql
import csv
import sys
import json
import pandas as pd
import requests


conn = pymysql.connect(user='root', password='root',host='127.0.0.1', database=str(sys.argv[1]))
dbname = str(sys.argv[1])
print(dbname)

cursor = conn.cursor()
query1 = f"SELECT CONCAT(a.table_name) FROM information_schema.tables a WHERE a.table_schema = '{dbname}'"
cursor.execute(query1)
table_list = list(cursor.fetchall())
print(table_list)

for table in table_list:
    cursor.execute("SELECT * FROM %s " % table[0])
    print(table[0])
    requests.delete(f'https://inf551-dcbb6.firebaseio.com/{dbname}/{table[0]}.json')
    rs = cursor.fetchall()
    column_names_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{dbname}' AND TABLE_NAME ='{table[0]}'"
    cursor.execute(column_names_query)
    columns_list = list(cursor.fetchall())
    print(columns_list)
    final_col = []
    for col in columns_list:
        final_col.append(col[0])
    print(final_col)
    df = pd.DataFrame(rs[1:], columns=final_col)
    print(df.head())
    df.to_json("station_data.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
    data1 = json.load(open("station_data.json"))
    response = requests.put(f'https://inf551-dcbb6.firebaseio.com/{dbname}/{table[0]}.json', json=data1)
    print(response)
cursor.close()
conn.close()
