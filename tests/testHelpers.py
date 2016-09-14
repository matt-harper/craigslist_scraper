import identify, cl_post
TEST_FILE = 'tests/testData.txt'

def loadTestData(filename):
	lines = []
	with open(filename) as f:
		for line in f:
			line = line.rstrip()
			if line != '':
				lines.append(line)
	return lines

def parseTestData(lines):
	QAdict = dict()		# 'Question'/answer dictionary
	for i, line in enumerate(lines):
		try:
			(text, answer) = line.split(':')
			text = text.rstrip()
			answer = answer.lstrip()

			QAdict[text] = answer
		except ValueError:
			print "Error: test data file formatting is incorrect on line", i+1

	return QAdict

def getTestData():
	lines = loadTestData(TEST_FILE)
	return parseTestData(lines)

def identify(id, ad):
	post = cl_post.Post(ad, "", 0)
	return id.identify(post)

def summarizeResults(testResults):
	numTests = len(testResults.keys())
	successfulTests = 0
	failures = dict()
	
	for test in testResults.keys():
		(boolean, answer) = testResults[test]
		if boolean:
			successfulTests += 1
		else:
			failures[test] = answer

	return (str(successfulTests) + "/" + str(numTests) +  " tests completed successfully", failures)
