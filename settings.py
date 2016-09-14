import args

#################################################################################
#	Global variables							#
#################################################################################
ID_STRING = 'Identified:'
MULT_STRING = 'Multiple:'
UNK_STRING = 'Unknown:'

CFG_PATH = './cfg/'
BRAND_CFG = 'cfg/brands.cfg'
MODEL_CFG = 'cfg/models.cfg'
SERIES_CFG = 'cfg/series.cfg'

BADWORD_PATH = 'data/badwords.txt'
KEYWORD_PATH = 'data/keywords.txt'
AGENTS_PATH  = 'data/agents.txt'

CL_BASE_URL = 'https://dallas.craigslist.org'
MUSIC_URL = CL_BASE_URL + '/search/msa'

#DEBUG = False
#################################################################################
#	End global variables							#
#################################################################################

def parseArgs():
	args.parseArgs()
