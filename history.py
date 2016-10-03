import sqlite3

DB_FILE = 'guitar_history.db'
GUITAR_TABLE = 'guitars'

class Database():
	def __init__(self, filename):
		self.db = self.open(filename)

	def __del__(self):
		self.close()

	def commit(self):
		self.db.commit()

	def open(self, filename):
		return sqlite3.connect(filename)

	def close(self):
		self.db.close()

	def execute(self, statement):
		self.query(statement)

	def query(self, statement):
		try:
			return self.db.execute(statement)
		except sqlite3.OperationalError:
			print "Error using query: " + statement

	def createTable(self, tableName, values):
		stmt = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' ('
		for i, value in enumerate(values):
			if i + 1 != len(values):
				stmt += value + ', '
			else:
				stmt += value + ');'

		self.execute(stmt)

	def dumpTable(self, tableName):
		query = 'select * from ' + tableName
		results = self.query(query)
		for result in results:
			print result

	def addGuitar(self, post):
		stmt = genInsert(GUITAR_TABLE, post.postID, post.title, post.identity, post.price)
		if not self.postExistsInDB(post):
			self.execute(stmt)

	def postExistsInDB(self, post):
		query = 'select * from ' + GUITAR_TABLE + ' where postID = ' + str(post.postID) + ';'
		results = self.query(query)
		if len(results.fetchall()) > 0:
			return True
		else:
			return False

	def createGuitarTable(self):
		self.createTable(GUITAR_TABLE, getGuitarTableValues())


def getGuitarTableValues():
	values = [	'postID INTEGER',
			'postTitle STRING',
			'identity STRING',
			'price INTEGER'
		 ]
	return values

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

def genInsert(tableName, postID, postTitle, identity, price):
	postTitle = postTitle.replace("\"", "")
        return "INSERT INTO " + tableName + " VALUES ( " + str(postID) + ", \"" + postTitle + "\", \"" + identity + "\", " + str(price) + ");"
             

