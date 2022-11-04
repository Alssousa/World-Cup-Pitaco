import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='alexandre',
    password='Al180202'
)

my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS worldcuppitaco")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)