import sqlite3

def openDatabase(filename):
        dbHandle = sqlite3.connect(filename)
        return dbHandle

def createGuitarTable(db, tableName):
        stmt = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' (name STRING, price INTEGER);'
        db.execute(stmt)

def insertGibberish(db, tableName, **kwargs):
        numRows = 10
        if 'rows' in kwargs:
                numRows = kwargs['rows']

        for i in range(numRows):
                stmt = 'INSERT INTO ' + tableName + " VALUES ( 'guitar " + str(i) + "', " + str(i) + ");"
                db.execute(stmt)
             
def dumpTable(db, tableName):
        query = 'SELECT * FROM ' + tableName + ';'
        cursor = db.execute(query)

        rows = []
        for row in cursor:
                rows.append(row)

        return rows

DB_FILE = 'guitar_history.db'

connection = openDatabase(DB_FILE)
createGuitarTable(connection, 'test_table')
insertGibberish(connection, 'test_table')
print dumpTable(connection, 'test_table')

connection.commit()
connection.close()
