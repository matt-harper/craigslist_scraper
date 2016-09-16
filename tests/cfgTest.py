import settings, cfg, testHelpers

def main():
	brandsRegex = regexLoad('cfg/Gibson.cfg')
	brandsSplit = splitLoad('cfg/Gibson.cfg')

	print "Loaded " + str(len(brandsRegex.keywords.keys())) + " sections with keywords via regex"
	print "Loaded " + str(len(brandsRegex.badwords.keys())) + " sections with badwords via regex"
	print "Loaded " + str(len(brandsRegex.requiredwords.keys())) + " sections with required words via regex"

	#print "\n\n" + str(brandsSplit)
	print "Loaded " + str(len(brandsSplit.keywords.keys())) + " sections with keywords via split"
	print "Loaded " + str(len(brandsSplit.badwords.keys())) + " sections with badwords via split"
	print "Loaded " + str(len(brandsSplit.requiredwords.keys())) + " sections with required words via split"


	

def regexLoad(filename):
	cfgData = cfg.CFG(filename, regex=True)
	return cfgData

def splitLoad(filename):
	cfgData = cfg.CFG(filename)
	return cfgData
	
