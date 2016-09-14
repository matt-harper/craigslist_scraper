from lxml import html, etree
import requests, random, cl_post

base_url = 'https://dallas.craigslist.org'
music_url = base_url + '/search/msa'
agents_path = 'data/agents.txt'

class Scraper():
	def __init__(self):
		self.loadUserAgents()

	def downloadPage(self, pageNumber=0):
		url = music_url
		if pageNumber > 0:
			url += '?s=' + str(int(100 * pageNumber))
		return Page(requests.get(url, headers=self.generateHeaders()))

	def generateHeaders(self):
		return self.generateUserAgentHeader()

	def generateUserAgentHeader(self):
		header = {'User-Agent' : self.getRandomAgent()}
		return header

	def loadUserAgents(self):
		self.agents = []
		with open(agents_path) as f:
			for agent in f:
				agent.rstrip()
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
				title = self.getTitle(row)
				url   = self.getUrl(row)
				price = self.getPrice(row)
				images= self.getImageURLs(row)

				post = cl_post.Post(title, url, price)
				post.images = images

				itemsForSale.append(post)
			except Exception as e:
				print e
				continue
		
		return itemsForSale
			
			
	def getUrl(self, row):
		urlExtension = row.find_class("hdrlnk")[0].get('href')
		return base_url + urlExtension

	def getTitle(self, row):
		return row.find_class("hdrlnk")[0].text
		# return row.get_element_by_id('titletextonly').text	# Old, no longer working

	def getPrice(self, row):
		try:
			price = row.find_class('price')[0].text
			return price.replace('$','')
		except:
			return 'N/A'

	def getImageURLs(self, row):
		imgs = []
		try:
			imgsElement = row.find_class('i gallery')[0]
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
