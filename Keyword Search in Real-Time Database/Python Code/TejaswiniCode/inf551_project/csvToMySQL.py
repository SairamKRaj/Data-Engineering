import mysql.connector
import pandas as pd
import os

cnx = mysql.connector.connect(user='root', password='tiger', host='127.0.0.1', database='mydb',auth_plugin='mysql_native_password')
cursor = cnx.cursor()
for file in os.listdir("H:\\Fdrive\\INF551\\project\\stack"):
    print(os.path.join("H:\\Fdrive\\INF551\\project\\stack", file))
    fileName=os.path.join("H:\\Fdrive\\INF551\\project\\stack", file)
    csv_data = pd.read_csv(fileName,engine="python")
    tableName=(file.split(".")[0]).lower()
    print(tableName)

    for row in csv_data.iterrows():
        list = row[1].values
        str1=""
        for l in list:
            str1=str1+"'"+str(l)+"',"

        str1=str1[:-1]
        # print(str1)
        cursor.execute("INSERT INTO "+ tableName+" VALUES("+str1+");")

    cnx.commit();


cursor.close()
cnx.close()
