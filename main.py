import json
import os
import random



fiveLetterWords = []
perfectLetters = ["_","_","_","_","_"]
validLetters = []
wrongLetters = []


with open('wordListFiveLetter.json', 'r') as fiveJSON:
    fiveLetterWords = json.load(fiveJSON)


# generates a random number, then returns a word from the list at that random index
def getRandomWord(wordList):
    randNum = random.randrange(0,len(wordList)-1)
    return wordList[randNum]


# returns a List of the letters contained within a given word. This is word length agnostic and can be used for both five and six letter word variants
def getLettersFromWord(word):
    letterList = []
    for x in word:
        letterList.append(x)
    return(letterList)
    
    
currentWord = getRandomWord(fiveLetterWords)
currentLetters = getLettersFromWord(currentWord)


def evaluateLetterMatch(guessWord):
    #global perfectLetters
    guessLetters = getLettersFromWord(guessWord)
    wordSize = len(guessLetters)
    # if guessWord == currentWord:
    #     #perfectLetters = guessLetters
    #     # for x in guessLetters:
    #     #     perfectLetters.append(x)
    #     for i in range(wordSize):
    #         perfectLetters[i] = guessLetters[i]
    #     return
    # else:
        # if x is in the word, its valid. if its in the word and in the same spot, its perfect
    for i in range(wordSize):
        if guessLetters[i] == currentWord[i]:
            perfectLetters[i] = guessLetters[i]
            if guessLetters[i] not in validLetters:
                validLetters.append(guessLetters[i])
        elif guessLetters[i] in currentWord and guessLetters[i] not in validLetters:
            validLetters.append(guessLetters[i])
        elif guessLetters[i] not in wrongLetters and guessLetters[i] not in validLetters:
            wrongLetters.append(guessLetters[i])


def resetLetterEvaluations():
    perfectLetters.clear()
    validLetters.clear()
    wrongLetters.clear()


def getUserGuess():
    guess = input("Type your guess: ").upper()
    while len(guess) != len(currentWord): 
        print("You did not enter a word of proper length.")
        guess = input("Please try again: ")
    return guess

def validateUserGuess(guessWord):
    pass


def gameLost():
    print("\n" * 2)
    print(f"Sorry, you didn't guess {currentWord} correctly!")

def gameWon():
    #os.system('cls||clear')
    #print("\n" * 100)
    print("\n" * 2)
    print(f"Congratulations, you guessed {currentWord} correctly!")


# This game loop is terminal based and formed the early basis for the projects skeleton; 
# currently, this file, main.py, serves the GUI game in pyGameGUI
# Will copy and refactor a mainTerminal that reintegrates this loop in the future


#game loop
# currentWord = getRandomWord(fiveLetterWords)
# currentLetters = getLettersFromWord(currentWord)
# guessList = []
# print(f"CURRENT WORD: {currentWord} \n(dev use only comment out)")
# print(f"You're attempting to guess a {len(currentWord)} letter word.")
# userGuess = getUserGuess()
# count = 1
# userWins = True
# while userGuess != currentWord:
#     if count > 6:
#         userWins = False
#         gameLost()
#         break
#     #resetLetterEvaluations()
#     evaluateLetterMatch(userGuess)
#     #currentPerf = "Perfect letters: " + str(perfectLetters)
#     currentPerf = f"Guess Number {count} : " + "   ".join(perfectLetters)
#     #print(currentPerf)
#     guessList.append(currentPerf)
#     #print(guessList)
#     print("\n".join(guessList))
#     print("Valid letters: ", validLetters)
#     print("Wrong letters: ", wrongLetters)
#     #perfectLetters = ["_","_","_","_","_"]
#     if count < 6:
#         userGuess = getUserGuess()
#     count+=1

# if userWins == True:
#     gameWon()
# guessList.clear



