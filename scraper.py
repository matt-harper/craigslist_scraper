from lxml import html
import requests, random, cl_post, settings

class Scraper():
	def __init__(self):
		self.agents = []
		self.loadUserAgents()

	def downloadPage(self, pageNumber=0):
		url = settings.MUSIC_URL
		if pageNumber > 0:
			url += '?s=' + str(int(100 * pageNumber))

                try:
        		return Page(requests.get(url, headers=self.generateHeaders()))
                except ValueError as e:
                        print "Error downloading page:" + str(e)
                        exit(-1)

	def generateHeaders(self):
		return self.generateUserAgentHeader()

	def generateUserAgentHeader(self):
		header = {'User-Agent' : self.getRandomAgent()}
		return header

	def loadUserAgents(self):
		with open(settings.AGENTS_PATH) as f:
			for agent in f:
				agent = agent.rstrip()
				self.agents.append(agent)

	def getRandomAgent(self):
		numAgents = len(self.agents)
		return self.agents[random.randint(0, numAgents - 1)]

	def getItemDescription(self, item):
		itemPage = Page(self.downloadItemPage(item))
		return itemPage.getDescription()

	def downloadItemPage(self, item):
		url = item.url
		page = requests.get(url, headers=self.generateHeaders())
		return page

class Page():
	def __init__(self, rawPage):
		self.page = rawPage
		self.tree = html.fromstring(rawPage.content)

	def parse(self):
		itemsForSale = []

		for row in self.getRowsClass():
			try:
				postID= self.getPostID(row)
				title = self.getTitle(row)
				url   = self.getUrl(row)
				price = self.getPrice(row)
				images= self.getImageURLs(row)
				date  = self.getDate(row)

				post = cl_post.Post(postID, title, url, price, date)
				post.images = images

				itemsForSale.append(post)
			except Exception as e:
				print e
				continue

		return itemsForSale

	def getPostID(self, row):
		return row.get('data-pid')

	def getUrl(self, row):
		urlExtension = row.find_class("hdrlnk")[0].get('href')
		return settings.CL_BASE_URL + urlExtension

	def getTitle(self, row):
		return row.find_class("hdrlnk")[0].text
		# return row.get_element_by_id('titletextonly').text	# Old, no longer working

	def getPrice(self, row):
		try:
			#price = row.find_class('price')[0].text
			price = row.find_class('result-price')[0].text
			return price.replace('$', '')
		except:
			return 'N/A'

	def getDate(self, row):
		timeClass = row.find_class("result-date")[0]
		datetime = timeClass.get('datetime')
		return datetime

	def getImageURLs(self, row):
		imgs = []
		try:
			#imgsElement = row.find_class('i gallery')[0]
			imgsElement = row.find_class('result-image gallery')[0]
			imgsAttrib = imgsElement.get('data-ids')
			if imgsAttrib is None:
				return imgs

			for url in imgsAttrib.split(','):
				domain = 'https://images.craigslist.org/'
				url = url[url.find(':') + 1:]
				ext = '_300x300.jpg'
				imgs.append(domain + url + ext)

			return imgs
		except:
			print "Error scraping image URLs"
			exit(0)
			return ''

	def getRowsClass(self):
		return self.tree.find_class('rows')[0]

	def getDescription(self):
		text = ''
		for line in self.tree.get_element_by_id('postingbody').itertext():
			line = line.rstrip().lstrip() + '\n'
			if 'show contact info' not in line and line != '\n':
				text += line

		return text
