import sys, datetime
import settings, craigslist_scraper


def writeHeader(file):
	pageTitle = 'Craigslist Scraper (%PAGES% Pages)'
	refreshTime = datetime.datetime.now()

	# Add number of pages parsed to title
	pageTitle = pageTitle.replace('%PAGES%', str(settings.PAGES))
	if settings.PAGES < 2:
		pageTitle = pageTitle.replace("Pages", "Page")

	head = "<!DOCTYPE HTML>\n<html>\n\t<head>\n"
	head += "\t\t<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>\n"
	head += "\t\t<script type='text/javascript' src='nhpup_1.1.js'></script>\n"
	head += "\t\t<link rel='stylesheet' href='styles.css'/>\n"
	head += "\t</head>\n\t<body>\n\t\t<h1>" + pageTitle + "</h1>\n"
	head += "\t\t<h3>Last updated " + refreshTime.strftime('%I:%M %m/%d/%y') + "</h3>\n"

	#head = '<!DOCTYPE HTML>\n<html>\n\t<body>\n\t\t	<h1>' + pageTitle + '</h1>\n'
	#head += "\t\t<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>\n"
	#head += "\t\t<script type='text/javascript' src='/nhpup_1.1.js'></script>\n"
	#head += "\t\t<link rel='stylesheet' href='styles.css'>\n"
	file.write(head)

def writeEnd(file):
	end = '\t</body>\n</html>\n'
	file.write(end)

def makePopupLink(post, identity):
	if post.images is not None and len(post.images) > 0:
		imgLink = post.images[0]
		return "<a href='" + post.url + "' onmouseover=\"nhpup.popup('<img src=&quot;" + imgLink + "&quot;/>', {'width':300});\">" + str(post) + "</a>"
	else:
		return makeLink(str(post), post.url)

def makeLink(title, url):
	return "<a href='" + url + "'>" + title + "</a>"

def writeSection(file, title, sectionPosts):
	# Section title/header
	file.write('\t\t<h2>' + title + '</h2>\n')

	file.write('\t\t<ul>\n')

	if type(sectionPosts) is list:
		for post in sectionPosts:
			file.write('\t\t\t\t<li>' + str(post) + '</li>\n')
	elif type(sectionPosts) is dict:
		for post in sectionPosts.keys():
			url = post.url
			identity = sectionPosts[post]
			#file.write('\t\t<li>' + str(identity) + " : " + makeLink(str(post), url)  + "</li>\n")
			file.write('\t\t<li>' + str(identity) + " : " + makePopupLink(post, identity)  + "</li>\n")
	else:
		print "Error: writeSection received unknown data type"
		file.close()
		raise Exception("Error: writeSection received unknown data type")

	file.write('\t</ul><br>\n')

def writeFile(file, data):
	file.truncate()
	(identified, multiple, unknown) = data

	writeHeader(file)

	if not settings.IDENTIFIED:
		writeSection(file, settings.ID_STRING, identified)
	if settings.UNKNOWN:
		writeSection(file, settings.UNK_STRING, unknown)
	if settings.MULTIPLE:
		writeSection(file, settings.MULT_STRING, multiple)

	writeEnd(file)

if __name__ == "__main__":
	htmlFilename = '/var/www/html/clscrape/index.html'

	settings.parseArgs()
	posts = craigslist_scraper.getInterestingPosts()

	# (identified, multiple, unknown)
	identities = craigslist_scraper.idPosts(posts)

	with open(htmlFilename, 'w') as f:
		writeFile(f, identities)


	print 'file://' + htmlFilename
