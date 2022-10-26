# Filtering non-words and proper nouns from the word list using the PyDictionary library

import json
from PyDictionary import PyDictionary


pyDict = PyDictionary()

fiveLetterWords = []

with open('wordListFiveLetter.json', 'r') as fiveJSON:
    fiveLetterWords = json.load(fiveJSON)


fiveLetterWordsFiltered = []

count =  0
for x in fiveLetterWords:
    count +=1
    if count % 50 == 0:
        print(count)
    try:
        tempDef = pyDict.meaning(x, disable_errors=True)
    except:
        pass
    #print(type(tempDef))
    #print(type(fiveLetterWords[0]))
    validType = type(fiveLetterWords[0])
    #if type(tempDef) == validType:
    if tempDef is not None:
        #print(x)
        fiveLetterWordsFiltered.append(x)


# print()
# print(len(fiveLetterWords))
# print(len(fiveLetterWordsFiltered))


with open('wordListFiveLetterPYDICT.json', 'w') as fiveJSON:
    json.dump(fiveLetterWordsFiltered, fiveJSON, indent=2)