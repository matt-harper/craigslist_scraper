import argparse, settings

def parseArgs():
	argParse = argparse.ArgumentParser()
	argParse.add_argument('-d', '--debug', dest='DEBUG', action='store_const', const=True, default=False, help='Enable debug output')
	argParse.add_argument('-u', '--unknown', dest='UNKNOWN', action='store_const', const=True, default=False, help='Print unidentified posts')
	argParse.add_argument('-m', '--multiple', dest='MULTIPLE', action='store_const', const=True, default=False, help='Print posts detected as having multiple items for sale')
	argParse.add_argument('-I', dest='IDENTIFIED', action='store_const', const=True, default=False, help='Disable printing of identified posts')
	argParse.add_argument('-n', '--pages', dest='PAGES', default=5, type=int, help='Download specified number of pages of Craigslist posts')
	argParse.add_argument('-w', '--web', dest='WEB', action='store_const', const=True, default=False, help='Print post listing in HTML format')
	argParse.add_argument('-t', '--test', dest='TEST', action='store_const', const=True, default=False, help='Execute script tests')
	argParse.add_argument('-c', '--cfg', dest='CFG_TEST', action='store_const', const=True, default=False, help='Run cfg file loading test')
	argParse.parse_args(namespace=settings)
	
