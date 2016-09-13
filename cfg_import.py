import re

class CFG:
	def __init__(self, fileName):
		self.name = self.stripFilePath(self.stripFileExtension(fileName)).lower()
		self.headers = {}
		self.parse(fileName)

	def parse(self, fileName):
		fileData = ""
		with open(fileName) as f:
			fileData = f.read()

		headerRegex = "a-zA-Z "
		dataPointRegex = "^["

		regex = "\[(?P<header>[" + headerRegex + "]+)\]\n(?P<data>[" + dataPointRegex + "]*)\n"
		#regex = "\[(?P<header>[a-zA-Z ]+)\]\n(?P<data>[a-zA-Z \n]*)\n"
		for section in re.finditer(regex, fileData):
			header = section.groupdict()['header'].lower()
			data   = section.groupdict()['data'].lower()
			self.parseSection(header, data)

	def parseSection(self, header, data):
		if data == '':
			self.headers[header] = []
			return

		for line in data.split("\n"):
			if line == '':
				continue
			if header not in self.headers:
				self.headers[header] = [line,]
			else:
				self.headers[header].append(line)
		 

	def stripFilePath(self, fileName):
		if "/" in fileName:
			return fileName[fileName.rfind("/") + 1:]
		else:
			return fileName

	def stripFileExtension(self, fileName):
		return fileName[:fileName.find(".")]
