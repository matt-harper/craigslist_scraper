
class Post():
	def __init__(self, postID, title, url, price, datetime):
		self.postID = postID
		self.title = title.encode('utf-8')
		self.name = title.lower().encode('utf-8')
		self.url = url
		self.datetime = datetime
		self.setPrice(price)

		self.printHTML = False
		self.images = None
		self.identity = None

	def getRegion(self):
		if (self.url == ''):
			return ''

		return self.url[0:self.url.find(".craigslist")].replace("https://","")

	def setPrice(self, price):
		if price == 'N/A':
			self.price = 0
		else:
			self.price = price

	def __repr__(self):
		if not self.printHTML:
			return self.displayText()
		else:
			return self.htmlPrint()

	def htmlPrint(self):
		return "<a href='" + self.url + "'>" + self.displayText() + "</a>"

	def displayText(self):
		return self.name + " : $" + str(self.price)

