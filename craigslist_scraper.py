#!/usr/bin/python

import scraper, adFilter, identify, settings, history
import tests.test, tests.cfgTest

# Download pages from Craigslist and parse pages out into individual ads/posts
def getPosts(pages):
	cl = scraper.Scraper()
	posts = []

	for i in range(pages):
		posts += cl.downloadPage(i).parse()

	return posts

# Attempt to identify interesting posts
def idPosts(posts):
	id = identify.Identifier()
	identified = dict()
	multiple = []
	unknown = []
	for post in posts:
		identity = id.identify(post)

#		if identity == 'Multiple':
#			multiple.append(post)
#		elif identity == '':
#			unknown.append(post)
#		else:
#			identified[post] = identity
#			post.identity = identity

		if identity is None:
			multiple.append(post)
		elif identity == '':
			unknown.append(post)
		else:
			(brand, model, series) = identity
			idString = (brand + " "  + model + " " + series).rstrip()
			identified[post] = idString
			post.identity = identity

	return (identified, multiple, unknown)

def display(idPostGroup):
	(identified, multiple, unknown) = idPostGroup

	# By default, print only identified posts
	if not settings.IDENTIFIED:
		print settings.ID_STRING
		for post in identified.keys():
			print identified[post] + " : " + str(post)
		print "\n"

	if settings.MULTIPLE:
		print settings.MULT_STRING
		for post in multiple:
			print post
		print "\n"

	if settings.UNKNOWN:
		print settings.UNK_STRING
		for post in unknown:
			print post
		print "\n"


def getInterestingPosts():
	posts = getPosts(settings.PAGES)
	interesting = adFilter.filterUninteresting(posts)

	return interesting

if __name__ == "__main__":
	settings.parseArgs()
	historyDB = history.Database(history.DB_FILE)
	historyDB.createTable(history.GUITAR_TABLE, history.getGuitarTableValues())
	historyDB.createTable(history.HISTORY_TABLE, history.getHistoryTableValues())
	historyDB.createTable(history.IDENTITY_TABLE, history.getIdentityTableValues())
	historyDB.createTable(history.URL_TABLE, history.getURLTableValues())
	historyDB.createTable(history.IMAGE_TABLE, history.getImageTableValues())
	historyDB.createTable(history.DELETED_TABLE, history.getDeletedTableValues())

	if settings.TEST:
		print "Testing..."
		tests.test.main()
		exit(0)

	if settings.CFG_TEST:
		print "Testing cfg..."
		tests.cfgTest.main()
		exit(0)

	interesting = getInterestingPosts()
	(identified, multiple, unknown) = idPosts(interesting)

	for post in identified.keys():
		identity = identified[post]
		historyDB.addGuitar(post)
		historyDB.insertPost(post)


	historyDB.commit()

	display((identified, multiple, unknown))

