import sqlite3
import database, cfg
from os import listdir
from os.path import isfile, join

DB_FILE = 'cfg/reference.db'

def enumerateCfgFiles(path, **kwargs):	
	excludeList = [	'models.cfg',
			'brands.cfg',
			'series.cfg',
		      ]

	files = [f for f in listdir(path) if '.cfg' in f and f[0] != '.' and f not in excludeList]

	if 'stripCFG' in kwargs and kwargs['stripCFG']:
		files = [f.replace('.cfg', '') for f in files]
	return files

def enumerateFiles(path):
	files = [f for f in listdir(path) if isfile(join(path, f)) and '.cfg' in f]
	files = [f.replace(".cfg", "") for f in files if f[0] != '.']

	excludeList = [	'models',
			'brands',
			'series',
			'reference.db',
		      ]

	files = [f for f in files if f not in excludeList]
	return files

def loadBrandsFromCfgPath():
	brandsFilePath = 'cfg/'
	brands = enumerateCfgFiles(brandsFilePath, stripCFG=True)

	return brands

def loadBrandsFromCFG():
	brandCFG = cfg.CFG('cfg/brands.cfg')
	return brandCFG.keywords.keys()

def loadModelsFromCfgPath():
	cfgFiles = ['cfg/' + f for f in enumerateCfgFiles('cfg/')]
	models = []

	for fileName in cfgFiles:
		brandCFG = cfg.CFG(fileName)
		for model in brandCFG.keywords.keys():
			model = model.replace("!", "").replace("*", "")
			if model not in models:
				models.append(model)
		
	return models

def loadModelsFromCFG():
	modelCFG = cfg.CFG('cfg/models.cfg')
	return modelCFG.keywords.keys()

def generateInsert(table, values):
	stmt = 'insert into ' + table + ' values ( '
	for value in values:
		stmt += "'" + value + "',"
	stmt = stmt[:len(stmt)-1]
	stmt += ");"
	return stmt

def generateBrandInsert(brand):
	return generateInsert('brands', [brand,])

def generateModelInsert(model):
	return generateInsert('models', [model.replace("'",""),])

def insertBrands():
	db = database.Database(DB_FILE)
	for brand in loadBrandsFromCfgPath():
		try:
			db.execute(generateBrandInsert(brand))
		except sqlite3.IntegrityError:
			continue
	for brand in loadBrandsFromCFG():
		try:
			db.execute(generateBrandInsert(brand))
		except sqlite3.IntegrityError:
			continue
	db.commit()

def insertModels():
	db = database.Database(DB_FILE)
	# Load from each <BRAND>.cfg  in cfg/
	for model in loadModelsFromCfgPath():
		# Try/catch to avoid inserting duplicate models
		try:
			db.execute(generateModelInsert(model))
		except sqlite3.IntegrityError:
			continue
	# Load from cfg/models.cfg
	for model in loadModelsFromCFG():
		try:
			db.execute(generateModelInsert(model))
		except sqlite3.IntegrityError:
			continue
	db.commit()


if __name__ == "__main__":
	print loadBrandsFromCfgPath()
	print loadBrandsFromCFG()
	#insertBrands()
	#insertModels()
