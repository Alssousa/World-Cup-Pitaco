from sqlalchemy import  create_engine
import mysql.connector
'''
SERVER = 'worldcuppitaco-db.mysql.database.azure.com'
DATABASE = 'worldcuppitaco'
DRIVER = 'SQL Server'
USERNAME = 'worldcuppitaco'
PASSWORD = 'Copadomundo2022'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = create_engine(DATABASE_CONNECTION)
cnx = engine.connect()'''

cnx = mysql.connector.connect(user="worldcuppitaco", password="Copadomundo2022",
                              host="worldcuppitaco-db.mysql.database.azure.com", port=3306, database="worldcuppitaco", ssl_ca="DigiCertGlobalRootCA.crt.pem")

my_cursor = cnx.cursor()

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)