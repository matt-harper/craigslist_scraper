from os import listdir
from os.path import isfile, join
import cfg, re, types, settings

class Identifier:
	def __init__(self):
		self.models = cfg.CFG(settings.MODEL_CFG)
		self.brands = cfg.CFG(settings.BRAND_CFG)
		self.series = cfg.CFG(settings.SERIES_CFG)

		self.mc = MasterCFG()

	def identify(self, clItem):
		debug("Identifying ", clItem.name)
		identity = Identity()

		#if self.isMultiple(clItem):
		#	return "Multiple"

		for brand in self.getPotentialBrands(clItem):
			identity.addBrand(brand)

		for model in self.getPotentialModels(clItem):
			identity.addModel(model)

		for series in self.getPotentialSeries(clItem):
			identity.addSeries(series)

		return identity.interpret(self.mc)

	# Get a list of brands that an item could potentially be
	def getPotentialBrands(self, clItem):
		brands = []

		# Loop over each potential brand
		for brand in self.brands.keywords:
			# Ensure all required words are present
			requirementsMet = True
			for requiredWord in self.brands.getRequiredwords(brand):
				if requiredWord not in clItem.name:
					requirementsMet = False
			if not requirementsMet:
				continue

			# Check the item name for keywords
			# If keyword is present, and a badword is not present, add brand as a potential
			for keyword in self.brands.getKeywords(brand):
				if keyword in clItem.name:
					if not hasBadword(self.brands.getBadwords(brand), clItem.name):
						brands.append(brand)
		return brands

	def getPotentialModels(self, clItem):
		models = []

		# Loop over each potential model
		for model in self.models.keywords:
			# Ensure all required words are present
			requirementsMet = True
			for requiredWord in self.models.getRequiredwords(model):
				if requiredWord not in clItem.name:
					requirementsMet = False
			if not requirementsMet:
				continue

			# Check the item name for keywords
			# If keyword is present, and a badword is not present, add model as a potential
			for keyword in self.models.getKeywords(model):
				if keyword in clItem.name:
					if not hasBadword(self.models.getBadwords(model), clItem.name):
						models.append(model)
		return models

	def getPotentialSeries(self, clItem):
		seriesList = []

		# Loop over each potential series 
		for series in self.series.keywords:
			# Ensure all required words are present
			requirementsMet = True
			for requiredWord in self.series.getRequiredwords(series):
				if requiredWord not in clItem.name:
					requirementsMet = False
			if not requirementsMet:
				continue

			# Check the item name for keywords
			# If keyword is present, and a badword is not present, add series as a potential
			for keyword in self.series.getKeywords(series):
				if keyword in clItem.name:
					if not hasBadword(self.series.getBadwords(series), clItem.name):
						seriesList.append(series)
		return seriesList 

	def isAmp(self, clItem):
		ampKeys = ['guitar amp', 'combo amp']
		for key in ampKeys:
			if key in clItem.name:
				return True
		return False

	def isMultiple(self, clItem):
		multipleKeys = [' and ', 'guitars', ',', '+']
		exemptKeys = ['and case',]
		for key in multipleKeys:
			if key in clItem.name and not hasBadword(exemptKeys, clItem.name):
				return True
		return False

	def getBrandList(self):
		brands = []
		for brand in self.brands.keywords:
			brands.append(brand)
		return brands

	def getModelList(self):
		models = []
		for model in self.models.keywords:
			models.append(model)
		return models

	def getSeriesList(self):
		seriesList = []
		for series in self.series.keywords:
			seriesList.append(series)
		return seriesList

class Identity:
	def __init__(self):
		self.brands = {}
		self.models = {}
		self.series = {}

	def addBrand(self, brand):
		if not brand in self.brands:
			self.brands[brand] = 1
		else:
			self.brands[brand] += 1

	def addModel(self, model):
		if not model in self.models:
			self.models[model] = 1
		else:
			self.models[model] += 1

	def addSeries(self, series):
		if not series in self.series:
			self.series[series] = 1
		else:
			self.series[series] += 1

	def interpret(self, masterConfig):
		possibleIDs = []

		debug("Interpretting the following data:\n\t" + str(self.brands.keys()) + "\n\t" + str(self.models.keys()) + "\n\t" + str(self.series.keys()))
		
		for brand in self.brands.keys():
			for model in self.models.keys():
				for series in self.series.keys():
					if masterConfig.exists(brand, model, series):
						debug(brand, model, series, "is a valid combination")
						possibleIDs.append((brand, model, series))
					else:
						debug(brand, model, series, "does not exist")

				# If there is no series data, just check for the brand/model combo
				if len(self.series.keys()) == 0 or not masterConfig.requiresSeries(brand, model):
					if masterConfig.exists_bm(brand, model):
						debug(brand, model, "is a valid combination")
						possibleIDs.append((brand, model, ""))
					else:
						debug(brand, model, "does not exist")
					
		if len(possibleIDs) == 1:
			(brand, model, series) = possibleIDs[0]
			return (brand + " " + model + " " + series).rstrip()
		elif len(possibleIDs) > 1:
			# Throw out any IDs that don't have a full brand/model/series
			completeIDs = []
			for possibleID in possibleIDs:
				(brand, model, series) = possibleID
				if series != '':
					completeIDs.append((brand, model, series))

			if len(completeIDs) == 1:
				(brand, model, series) = completeIDs[0]
				return (brand + " " + model + " " + series).rstrip()
			else:
				return "More than 1 possible"
		else:
			return ""

	def old_interpret(self):
		brand = self.interpretBrand()
		model = self.interpretModel()
		series = self.interpretSeries()

		
		if type(brand) is types.ListType:
			# Choose between brands
			if 'tele' in model.lower() or 'strat' in model.lower():
				if 'squier' in [x.lower() for x in brand]:
					brand = 'Squier'
				if 'fender' in [x.lower() for x in brand]:
					brand = 'Fender'
				#TODO No logic behind choosing [0] here
				brand = brand[0]
			else:
				brand = brand[0]
		elif brand == "":
			# Choose brand based on model/series
			if series.lower() == 'mia' or series.lower() == 'mim':
				if 'tele' in model.lower() or 'strat' in model.lower():
					brand = 'Fender'

		if type(series) is types.ListType:
			# Choose between series
			if 'mia' in [x.lower() for x in series]  and 'deluxe' in [x.lower() for x in series]:
				series = 'Deluxe'
		else:
			pass


		if brand.lower() == 'epiphone' or brand.lower() == 'gibson':
			string = brand + " " + model + " " + series
		else:
			string = brand + " " + series + " " + model

		string = re.sub("\s+", " ", string)
		string = re.sub("^\s|\s$", "", string)

		return string

	def interpretBrand(self):
		maxScore = 0
		maxBrands = []
		for brand in self.brands:
			if self.brands[brand] == 0:
				continue
			if self.brands[brand] > maxScore:
				maxScore = self.brands[brand]
				maxBrands = [brand,]
				continue
			if self.brands[brand] == maxScore:
				maxBrands.append(brand)
		if maxScore == 0:
			return ""
		if len(maxBrands) == 1:
			return maxBrands[0]

		# Choose between multiple detected brands
		return maxBrands

	def interpretModel(self):
		maxScore = 0
		maxModels = []
		for model in self.models:
			if self.models[model] == 0:
				continue
			if self.models[model] > maxScore:
				maxScore = self.models[model]
				maxModels = [model,]
				continue
			if self.models[model] == maxScore:
				maxModels.append(model)
		if maxScore == 0:
			return ""
		if len(maxModels) == 1:
			return maxModels[0]

		# Choose between multiple deteced models
		if 'Acoustic' in maxModels:
			return 'Acoustic'

		return "???"

	def interpretSeries(self):
		maxScore = 0
		maxSeries = []
		for productLine in self.series:
			if self.series[productLine] == 0:
				continue
			if self.series[productLine] > maxScore:
				maxScore = self.series[productLine]
				maxSeries = [productLine,]
				continue
			if self.series[productLine] == maxScore:
				maxSeries.append(productLine)
		if maxScore == 0:
			return ""
		if len(maxSeries) == 1:
			return maxSeries[0]

		# Choose between multiple series
		return "???"

class MasterCFG:
	def __init__(self):
		self.filepath = settings.CFG_PATH
		self.loadedBrands = {}

	def enumerateFiles(self):
		files = [join(self.filepath, f) for f in listdir(self.filepath) if isfile(join(self.filepath, f)) and f[0] != (".")]
		return files

	def exists(self, brand, model, series):
		debug("Checking for", brand, model, series)
		self.loadBrand(brand)

		models = self.loadedBrands[brand].keywords.keys()

		for m in models:
			if m[0] == '!':
				if m[1:] == model and series in self.loadedBrands[brand].keywords[m]:
					return True					
			else:
				if m == model and series in self.loadedBrands[brand].keywords[model]:
					return True

		return False					

	def exists_bm(self, brand, model):
		debug("Checking for", brand, model)
		self.loadBrand(brand)

		models = self.loadedBrands[brand].keywords.keys()

		for m in models:
			if m == model:
				return True
			if m[1:] == model:
				return True

		return False
		
	def requiresSeries(self, brand, model):
		self.loadBrand(brand)

		models = self.loadedBrands[brand].keywords.keys()

		for m in models:
			if m[0] == '!' and m[1:] == model:
				return False

		return True

 	def loadBrand(self, brand):
		# Don't need to do anything if file has already been loaded
		if brand in self.loadedBrands.keys():
			return

		try:
			filename = self.filepath + brand + ".cfg"
			myCFG = cfg.CFG(filename)
			self.loadedBrands[brand] = myCFG
		except:
			raise Exception(brand + " not found")

def hasBadword(wordList, testPhrase):
	for word in wordList:
		if word in testPhrase:
			return True
	return False

def hasWord(wordList, testPhrase):
	for word in wordList:
		if word in testPhrase:
			return True
	return False

def debug(*message):
	if settings.DEBUG:
		string = ''
		for m in message:
			string += str(m) + ' '
		print string.rstrip()


