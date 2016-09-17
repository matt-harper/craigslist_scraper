import cl_post, settings


BADWORDS = None

def isInteresting(post):
        return not postTitleContainsBadword(post.title)

def postTitleContainsBadword(postTitle):
        # Lazy load badwords file
        global BADWORDS
        if BADWORDS is None:
                BADWORDS = loadBadwords()

        for word in BADWORDS:
                if word in postTitle:
                        return True
        return False

def filterUninteresting(posts):
        return [post for post in posts if isInteresting(post)]

def loadBadwords():
        return loadFile(settings.BADWORD_PATH)

def loadKeywords():
        return loadFile(settings.KEYWORD_PATH)

# Load file by line into array, ignoring blank lines
def loadFile(filename):
        words = []
        with open(filename) as f:
                for line in f:
                        line = line.rstrip()
                        if line == '':
                                continue
                        words.append(line)
        return words
