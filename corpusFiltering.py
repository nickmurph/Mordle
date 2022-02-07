with open('ACL_ARC.csv') as aclCorpus:
    lines = aclCorpus.readlines()



# fiveLetterWords = []
# sixLetterWords = []

for x in lines:
    # #x = x[:len(x)-1]
    # x = x.strip()
    # if len(x) == 5:
    #     fiveLetterWords.append(x.upper())
    print(x)