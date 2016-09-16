import re

class CFG:
	def __init__(self, filename, **kwargs):
		self.name = stripFileExtension(filename)
		self.keywords = {}
		self.badwords = {}
		self.requiredwords = {}

		if 'regex' in kwargs and kwargs['regex']:
			self.parseRegex(filename)
		else:
			self.parse(filename)

	def __repr__(self):
		string = self.name + "\n"
		for key in self.keywords.keys():
			string += "Keyword: " + key + "\n"
			for keyword in self.keywords[key]:
				string += "\t" + keyword + "\n"
		return string

	def parse(self, filename):
		fileData = ""
		with open(filename) as f:
			fileData = f.read()

		sections = fileData.split('[')

		for section in sections[1:]:	# First split is empty
			name = section[:section.find(']')].rstrip()	# Grab everything until the close bracket
			section = section.replace(name + "]", "", 1)	# Remove the section name and bracket
			words = section.split("\n")[1:]			# Split on newlines, first is empty
			words = [word for word in words if word != ""]	# Remove blank entries

			if len(words) == 0:
				self.badwords[name] = []
				self.requiredwords[name] = []
				self.keywords[name] = []
			else:
				for word in words:
					self.addGroupKeyword(name, word)


	def parseRegex(self, filename):
		fileData = ''
		with open(filename) as openFile:
			fileData = openFile.read()

		regex = "\[(?P<group>[\w\&\!\'\- ]+)+]\n(?P<keywords>[\w\n\s.!()&\-\*\']+)"
		for section in re.finditer(regex, fileData, flags=re.M):
			groupName = section.groupdict()['group']
			keywords = section.groupdict()['keywords']
			self.addGroupKeywords(groupName, keywords)
			if keywords.replace('\n', '') == '':
				self.badwords[groupName] = []
				self.requiredwords[groupName] = []
				self.keywords[groupName] = []
		
	def addGroupKeywords(self, groupName, keywords):
		for keyword in keywords.split("\n"):
			if keyword == '':
				continue
			self.addGroupKeyword(groupName, keyword)

	def addGroupKeyword(self, groupName, keyword):
		if keyword[0] == '!':
			self.parseBadword(groupName, keyword[1:])
		elif keyword[0] == '*':
			self.parseRequiredword(groupName, keyword[1:])
		else:
			self.parseKeyword(groupName, keyword)

	def parseRequiredword(self, groupName, requiredword):
		if groupName not in self.requiredwords:
			self.requiredwords[groupName] = [requiredword,]
		else:
			self.requiredwords[groupName].append(requiredword)

	def parseBadword(self, groupName, badword):
		if groupName not in self.badwords:
			self.badwords[groupName] = [badword,]
		else:
			self.badwords[groupName].append(badword)

	def parseKeyword(self, groupName, keyword):
		if groupName not in self.keywords:
			self.keywords[groupName] = [keyword,]
		else:
			self.keywords[groupName].append(keyword)

	def getKeywords(self, groupName):
		if groupName in self.keywords:
			return self.keywords[groupName]
		else:
			return []

	def getBadwords(self, groupName):
		if groupName in self.badwords:
			return self.badwords[groupName]
		else:
			return []

	def getRequiredwords(self, groupName):
		if groupName in self.requiredwords:
			return self.requiredwords[groupName]
		else:
			return []
		
def stripFileExtension(filename):
	return filename[:filename.find(".")]
