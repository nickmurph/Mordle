import json
import nltk

#nltk.download()
#nltk.download('averaged_perceptron_tagger')


fiveLetterWords = []

with open('wordListFiveLetter.json', 'r') as fiveJSON:
    fiveLetterWords = json.load(fiveJSON)


fiveLetterWordsFiltered = []

for x in fiveLetterWords:
    #all caps confuses NLTK classification
    x = x.lower()
    # capitalizing the first letter seems to give the least false results re: proper nouns
    x = x.capitalize()
    wordClassification = nltk.tag.pos_tag(x.split())
    #print(wordClassification[0][1])
    if wordClassification[0][1] not in ["NNP", "NNPS", "NNS"]:
        fiveLetterWordsFiltered.append(x)

print(len(fiveLetterWords))
print(len(fiveLetterWordsFiltered))

# The five letter word list is reduced from 5787 to 3953
# unfortunately, it still contains multiple instances of obscure place names or non-words
with open('wordListFiveLetterFilteredNLTK.json', 'w') as fiveJSON:
    json.dump(fiveLetterWordsFiltered, fiveJSON, indent=2)




# Used these lines to play around with NLTK's classification and probe the limits of what it considers a proper noun (NNP),
# in a non-exhaustive but sufficient manner
#
# testVar = nltk.tag.pos_tag("Testing this phrase for Nick".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Testing this phrase for Aaron".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Testing this phrase for Agatha".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Testing this phrase for London".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Testing this phrase for Denver".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Aaron".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("aaron".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("AARON".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Arise".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Roast".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Fuzzy".split())
# print(testVar)
# testVar = nltk.tag.pos_tag("Short".split())
# print(testVar)
# print(testVar[0])
# print(testVar[0][1])