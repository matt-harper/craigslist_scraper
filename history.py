import sqlite3

DB_FILE = '/var/www/guitar_history.db'
GUITAR_TABLE = 'guitars'
HISTORY_TABLE = 'guitars_history'
IDENTITY_TABLE = 'identities'
URL_TABLE = 'urls'
IMAGE_TABLE = 'images'
DELETED_TABLE = 'deleted'

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
		return
		stmt = genInsert(GUITAR_TABLE, post.postID, post.title, post.identity, post.price)
		if not self.postExistsInDB(post):
			self.execute(stmt)

	def insertPost(self, post):
		# Add the post metadata to the history table
		cmd = generateHistoryInsert(post)
		try:
			self.execute(cmd)
		except sqlite3.IntegrityError:
			return	

		cmd = generateURLInsert(post)
		try:
			self.execute(cmd)
		except sqlite3.IntegrityError:
			pass

		for cmd in generateImageInsert(post):
			self.execute(cmd)

		# Add the identity of the post to the indentity table
		if post.identity is None or post.identity == '':
			return
		cmd = generateIdentityInsert(post)
		try:
			self.execute(cmd)
		except sqlite3.IntegrityError:
			pass

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
			'price INTEGER',
		 ]
	return values

def getHistoryTableValues():
	values = [	'region STRING',
			'postID INTEGER UNIQUE',
			'date STRING',
			'postTitle STRING',
			'price INTEGER',
		 ]
	return values

def getIdentityTableValues():
	values = [	'postID INTEGER UNIQUE',
			'brand STRING',
			'model STRING',
			'series STRING',
		 ]
	return values

def getURLTableValues():
	values = [	'postID INTEGER UNIQUE',
			'url STRING',
		 ]
	return values

def getImageTableValues():
	values = [	'postID INTEGER',
			'url STRING',
		 ]
	return values

def getDeletedTableValues():
	values = [	'postID INTEGER UNIQUE',
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
             
def generateHistoryInsert(post):
	region = post.getRegion()
	postID = post.postID
	date   = post.datetime
	title  = post.title.replace("'","").replace("\"","")
	price  = post.price

	return "INSERT INTO " + HISTORY_TABLE + " VALUES ( '" + region + "', " + str(postID) + ", '" + date + "', '" + title + "', " + str(price) + ");"

def generateIdentityInsert(post):
	postID = post.postID
	(brand, model, series) = post.identity

	return "INSERT INTO " + IDENTITY_TABLE + " VALUES ( " + str(postID) + ", '" + brand + "', '" + model + "', '" + series + "');"

def generateURLInsert(post):
	postID = post.postID
	url    = post.url

	return "INSERT INTO " + URL_TABLE + " VALUES ( " + str(postID) + ", '" + url + "');"

def generateImageInsert(post):
	postID = post.postID
	images = post.images

	inserts = []
	for image in images:
		query = "INSERT INTO " + IMAGE_TABLE + " VALUES ( " + str(postID) + ",'" + image + "');"
		inserts.append(query)

	return inserts

