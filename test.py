#!/usr/bin/python

import argparse
import identify, cl_post, testHelpers, settings

# Parse program arguments
argParse = argparse.ArgumentParser()
argParse.add_argument('--debug', dest='DEBUG', action='store_const', const=True, default=False)
args = argParse.parse_args(namespace=settings)

testData = testHelpers.getTestData()
testResults = dict()
id = identify.Identifier()

for adText in testData.keys():
	answer = testHelpers.identify(id, adText)
	testResult = testData[adText] == answer
	testResults[adText] = (testResult, answer)
	
(summary, failures) = testHelpers.summarizeResults(testResults)
print summary
if len(failures) > 0:
	print "Failures:"
	for fail in failures.keys():
		try:
			answer = failures[fail]
			print fail, ":", answer
		except ValueError as e:
			print e

#post = cl_post.Post(title, '', 0)
#id = identify.Identifier()
#
#print id.identify(post)

