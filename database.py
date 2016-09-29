import sqlite3

class Database:
	def __init__(self, filename):
		self.filename = filename
		self.connection = None
		self.open()

	def __del__(self):
		self.close()

	def open(self):
		self.connection = sqlite3.connect(self.filename)

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

	def query(self, stmt):
		return self.connection.execute(stmt)

	def execute(self, stmt):
		self.connection.execute(stmt)
