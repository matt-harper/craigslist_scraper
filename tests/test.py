#!/usr/bin/python

import identify, cl_post, testHelpers, settings

def main():
	testData = testHelpers.getTestData()
	testResults = dict()
	id = identify.Identifier()

	for adText in testData.keys():
		answer = testHelpers.identify(id, adText)
		if answer is None:
			answer = 'More than 1 possible'
		elif answer == '':
			pass
		else:
			(brand, model, series) = answer
			answer = (brand + " " + model + " " + series).rstrip()

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

