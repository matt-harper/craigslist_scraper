#!/usr/bin/python

import scraper, deal_finder, identify, settings
import tests.test

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

		if identity == 'Multiple':
			multiple.append(post)
		elif identity == '':
			unknown.append(post)
		else:
			identified[post] = identity

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

def filterPosts(posts):
	dealFinder = deal_finder.DealFinder()

	interestingPosts = dealFinder.getPotentiallyInteresting(posts)

	return interestingPosts

def getInterestingPosts():
	posts = getPosts(settings.PAGES)
	interesting = filterPosts(posts)

	return interesting

if __name__ == "__main__":
	settings.parseArgs()

	if settings.TEST:
		print "Testing..."
		tests.test.main()
		exit(0)

	interesting = getInterestingPosts()

	display(idPosts(interesting))

