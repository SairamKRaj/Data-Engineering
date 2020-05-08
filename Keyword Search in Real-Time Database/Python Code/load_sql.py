import csv
import mysql.connector
import sys

mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', db='stack_exchange')
cursor = mydb.cursor()

csv_data = csv.reader(open(sys.argv[1]))
for row in csv_data:
    add_data = ("""INSERT INTO tags (id, tag) VALUES (%s, %s)""")
    cursor.execute(add_data, row)
#close the connection to the database.
mydb.commit()
cursor.close()
print("Done")
