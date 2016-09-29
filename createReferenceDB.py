import sqlite3
import database
from os import listdir
from os.path import isfile, join

DB_FILE = 'cfg/reference.db'

def enumerateFiles(path):
	files = [f for f in listdir(path) if isfile(join(path, f))]
	files = [f.replace(".cfg", "") for f in files if f[0] != '.']

	excludeList = [	'models',
			'brands',
			'series',
			'master.db',
		      ]

	files = [f for f in files if f not in excludeList]
	return files

def loadBrands():
	brandsFilePath = 'cfg/'
	brands = enumerateFiles(brandsFilePath)

	return brands

def generateBrandInsert(brand):
	return 'insert into brands values ( "' + brand + '" );'

def insertBrands():
	db = database.Database(DB_FILE)
	for brand in loadBrands():
		db.execute(generateBrandInsert(brand))
	db.commit()

if __name__ == "__main__":
	insertBrands()
