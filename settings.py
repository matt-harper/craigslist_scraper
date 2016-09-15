import args

#################################################################################
#	Global variables							#
#################################################################################
ID_STRING = 'Identified:'
MULT_STRING = 'Multiple:'
UNK_STRING = 'Unknown:'

CFG_PATH = './cfg/'		# Path to config data for well known brand/model/series combinations
BRAND_CFG = 'cfg/brands.cfg'	# List of known brands
MODEL_CFG = 'cfg/models.cfg'	# List of known models
SERIES_CFG = 'cfg/series.cfg'	# List of known series

BADWORD_PATH = 'data/badwords.txt'	# Words that indicate a post is completely uninteresting
KEYWORD_PATH = 'data/keywords.txt'	# Words that may represent a brand, model, series, etc
AGENTS_PATH  = 'data/agents.txt'	# User agents for scraping Craigslist pages

CL_BASE_URL = 'https://dallas.craigslist.org'
MUSIC_URL = CL_BASE_URL + '/search/msa'

# Flags to control execution and output
DEBUG = False		# Display debug information
IDENTIFIED = False	# Inverse of whether or not to display identified posts
			# Eg, False means to show identified posts and True is a signal NOT to show
MULTIPLE = False	# Whether or not to display posts detected as having multiple items for sale
UNKNOWN = False		# Whether or not to display posts that are unable to be identified
PAGES = 5		# Number of Craigslist pages to scrape
TEST = False		# Flag to execute identification tests
#################################################################################
#	End global variables							#
#################################################################################

def parseArgs():
	args.parseArgs()
