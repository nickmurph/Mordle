import json

with open('word lists/gwicks justwords/engmix.txt') as engmix:
    lines = engmix.readlines()


#print(lines)
#print(len(lines))

fiveLetterWords = []
sixLetterWords = []

for x in lines:
    #x = x[:len(x)-1]
    x = x.strip()
    if len(x) == 5:
        fiveLetterWords.append(x.upper())
    if len(x) == 6:
        sixLetterWords.append(x.upper())


print(fiveLetterWords[1000])
print(sixLetterWords[1000])
print(len(fiveLetterWords))
print(len(sixLetterWords))
#print(fiveLetterWords[5]+sixLetterWords[5])


json.dumps(fiveLetterWords)

with open('wordListFiveLetter.json', 'w') as fiveJSON:
    json.dump(fiveLetterWords, fiveJSON, indent=2)

with open('wordListSixLetter.json', 'w') as sixJSON:
    json.dump(sixLetterWords, sixJSON, indent=2)





#
#
# TO DO: Add a check for each word off the list to verify it is in the dictionary. This will filter out any given names (eg, Allan or Agatha), place names (eg, Aberdovey, a city in Wales), and 
#        slang to ensure that words being pulled by the game logic fit the expectation for a Wordle-like experience
#        Check should occur as a paired AND condition with the length checks on line 16 and 18
#        Write a small function to call one of the dictionary APIs and check the 'x' word, returning true if a definition exists, call this function in the AND condition
# BONUS: Also consider using a NLP based library (as seen in Comp Linguistics class) to remove variations of word, though this should depend on size of word lists after dictionary
#        filtering; a considerable reduction in the word list may mean having both "abide" in the 5 letter list and "abides" in the 6 letter list is welcome purely for variety/breadth purposes
#
#