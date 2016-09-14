import cl_post

class DealFinder():
	def __init__(self):
		self.badwordsPath = 'data/badwords.txt'
		self.keywordsPath = 'data/keywords.txt'
		self.loadKeywords()
		self.loadBadwords()

	def itemIsInteresting(self, item):
		return not self.itemContainsBadword(item)
		#return self.itemContainsKeyword(item) and not self.itemContainsBadword(item)

	def itemContainsKeyword(self, item):
		item = item.name.lower()
		for word in self.keywords:
			if word in item:
				return True
		return False

	def itemContainsBadword(self, item):
		item.name = item.name.lower()
		for word in self.badwords:
			if word in item.name:
				return True
		return False

	def loadKeywords(self):
		self.keywords = []
		with open(self.keywordsPath) as f:
			for line in f:
				line = line.rstrip()
				if (line == ''):
					continue
				self.keywords.append(line)

	def loadBadwords(self):
		self.badwords = []
		with open(self.badwordsPath) as f:
			for line in f:
				#line = line.rstrip()
				line = line.replace("\n", "")
				if (line == ''):
					continue
				self.badwords.append(line)

	# Filters based on keywords and 'bad' keywords
	def getPotentiallyInteresting(self, posts):
		interesting = []
		for post in posts:
			if self.itemIsInteresting(post):
				interesting.append(post)
		return interesting

	def getNotInteresting(self, posts):
		notInteresting = []
		for post in posts:
			if not self.itemIsInteresting(post):
				notInteresting.append(post)
		return notInteresting

