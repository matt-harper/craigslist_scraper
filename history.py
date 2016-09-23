import sqlite3

def openDatabase(filename):
        dbHandle = sqlite3.connect(filename)
        return dbHandle

def createGuitarTable(db, tableName):
        stmt = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' (postID INTERGER, postTitle STRING, identity STRING, price INTEGER);'
        db.execute(stmt)

def insertGibberish(db, tableName, **kwargs):
        numRows = 10
        if 'rows' in kwargs:
                numRows = kwargs['rows']

        for i in range(numRows):
                stmt = genInsert(tableName, str(i), "Example title " + str(i), "Guitar " +  str(i), 0)
                db.execute(stmt)

def loadTestData(filename):
        fileData = ''
        with open(filename) as testFile:
                fileData = testFile.read()

        lines = fileData.split('\n')
        for line in lines:
                if line.rstrip() == '':
                        continue
                try:
                        (title, identity) = line.split(' : ')
                except ValueError:
                        print "Test data file error line: " + line
                print title + 'XXX\t' + identity + 'XXX'

def genInsert(tableName, postID, postTitle, identity, price):
        return "INSERT INTO " + tableName + " VALUES ( " + str(postID) + ", '" + postTitle + "', '" + identity + "', " + str(price) + ");"
             
def dumpTable(db, tableName):
        query = 'SELECT * FROM ' + tableName + ';'
        cursor = db.execute(query)

        rows = []
        for row in cursor:
                rows.append(row)

        return rows

DB_FILE = 'guitar_history.db'

loadTestData('tests/testData.txt')

#connection = openDatabase(DB_FILE)
#createGuitarTable(connection, 'test_table')
#insertGibberish(connection, 'test_table')
#print dumpTable(connection, 'test_table')

#connection.commit()
#connection.close()
