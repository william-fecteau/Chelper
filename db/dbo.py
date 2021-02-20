import os
import pyodbc
from dotenv import load_dotenv

class DBO():

    def __init__(self, dbServer : str, dbName : str):
        self.dbServer = dbServer
        self.dbName = dbName
        self.conn = None

        self.connect()

    def connect(self):
        try:
            self.conn = pyodbc.connect(
                'Driver={SQL Server};'
                'Server=' + str(self.dbServer) + ';'
                'Database=' + str(self.dbName) + ';'
                'Trusted_Connection=yes;')
        except pyodbc.Error as err:
            print(err)
            print('Database connection failed!')
            exit()

    def testSelect(self):
        cursor = None

        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM test.dbo.Person')
        except pyodbc.Error as err:
            print(err)

        for row in cursor:
            print(row)