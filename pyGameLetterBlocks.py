import pygame
from pygameAlphaKeys import pygame_alpha_keys 
from main import fiveLetterWords
from main import getRandomWord

# PyGame basics to set up the GUI box
pygame.init()
# original screen dimensions 100, 800
screen = pygame.display.set_mode([460,750])
user_font = pygame.font.Font(None, 80)
keyboard_font = pygame.font.Font(None, 40)
user_input = ""
qwertyList = list("QWERTYUIOPASDFGHJKLZXCVBNM")
pygame.display.set_caption('Moredle')
screen.fill((0,0,0))

# targetWord = ['A','R','I','S','E']
targetWord = getRandomWord(fiveLetterWords)
#print(targetWord)


# LetterBox class wraps around a PyGame rectangle object and various helper attributes
# in the GUI, there is a 6x5 grid of LetterBoxes representing the six guesses a player is allowed and the five letters in each guess
class LetterBox:
    def __init__(self, placementTuple, rectObj):
        self.placement = placementTuple
        self.rectObj = rectObj
        self.name = f"LB{placementTuple}"
        self.perfectGuess = False
        self.validGuess = False

    def printRect(self):
        left = self.rectObj.left
        top = self.rectObj.top
        width = self.rectObj.width
        height = self.rectObj.height
        print(left,top,width,height)

    def printPlacement(self):
        print(self.placement)
        
    def printAllInfo(self):
        print(self.name)
        self.printPlacement()
        self.printRect()


class KeyboardLetter():
    def __init__(self, letter, rectObj):
        self.letter = letter
        self.rectObj = rectObj
        self.valid = True
        self.perfect = False

    def setValidity(self, boolArg):
        self.valid = boolArg

    def setPerfection(self, boolArg):
        self.perfect = boolArg

    

#guessZero_letterOne = LetterBox((0,1), pygame.Rect(10, 50, 80, 75))
#guessZero_letterOne.printDump()


letterBox_grid = [[None]*5 for i in range(6)]
guess_storage_grid = [[None]*5 for i in range(6)]
keyboard_grid = [[None]*10, [None]*9, [None]*7]
kb_hash_ref = {}
#print(keyboard_grid)


    

# Creates a LetterBox object and stores it in the 2D grid at the appropriate row,col coordinate
# Each LetterBox is wrapped around a PyGame Rect object, which needs left, top, width, and height coordinates
# The coordinates are adjusted within the loop to provide for proper spacing on the GUI, depending on row and col
def populate_letterbox_grid():
    lb_left = 10
    lb_top = 100
    lb_width = 80
    lb_height = 75
    # i row, j col
    for i in range(6):
        lb_left = 10
        if i > 0:
            lb_top = lb_top + 80
        for j in range(5):
            if j > 0:
                lb_left = lb_left + 90
            letterBox_grid[i][j] = LetterBox((i,j), pygame.Rect(lb_left,lb_top,lb_width,lb_height))



def populate_keyboard():
    kb_left = 7
    kb_top = 610
    kb_width = 37
    kb_height = 37
    counter = 0

    # i row, j col
    for i in range(3):
        if i == 0:
            kb_left = 7
        elif i == 1:
            kb_left = 14
        elif i == 2:
            kb_left = 40
        if i > 0:
            kb_top = kb_top + 50
        
        
        for j in range(10):
            if i == 0:
                tempLetter = qwertyList[counter]
                if j > 0:
                    kb_left = kb_left + 45
                keyboard_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_hash_ref[tempLetter] = (i,j)
                counter += 1
            elif i == 1 and j < 9:
                tempLetter = qwertyList[counter]
                if j > 0:
                    kb_left = kb_left + 49
                keyboard_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_hash_ref[tempLetter] = (i,j)
                counter += 1
            elif i == 2 and j < 7:
                tempLetter = qwertyList[counter]
                if j > 0:
                    kb_left = kb_left + 55
                keyboard_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_hash_ref[tempLetter] = (i,j)
                counter += 1                
# 
#
#
def drawCurrentGuess(rect):
    text_surface = user_font.render(user_input, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))
    pygame.display.flip()

def drawPrevGuess(rect, guessText):
    text_surface = user_font.render(guessText, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))


def drawPerfectGuess(rect, guessLetter):
    text_surface = user_font.render(guessLetter, True, (50,255,168))
    screen.blit(text_surface, (rect.x+30, rect.y+5))


def drawEmptyBox(rect):
    text_surface = user_font.render("", True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))



# populate the LB grid and declare a few global variables to use in the game loop
populate_letterbox_grid()
populate_keyboard()
guess_progressions = [False, False, False, False, False, False]
currentWordLen = 0
curBox = letterBox_grid[0][0]
curRect = curBox.rectObj


# main game loop
gameRunning = True
while gameRunning:    

    # if the user has entered a letter into an empty box, the cursor will progress to the next letter
    if len(user_input) == 1 and currentWordLen < 5:
        row = curBox.placement[0]
        col = curBox.placement[1]

        guess_storage_grid[row][col] = user_input
        user_input = ""
        curBox = letterBox_grid[row][col+1]
        curRect = curBox.rectObj



    # handling user generated events     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

        # if any key has been pressed
        if event.type == pygame.KEYDOWN:    
            # if the user has entered backspace, and there are any entered letters capable of being removed, do so
            if event.key == pygame.K_BACKSPACE:
                row = curBox.placement[0]
                col = curBox.placement[1]

                if currentWordLen == 0:
                    break     
                elif currentWordLen == 1:
                    guess_storage_grid[row][0] = None
                    curBox = letterBox_grid[row][0]
                elif currentWordLen == 5:
                    guess_storage_grid[row][4] = None
                elif guess_storage_grid[row][col] == None:
                    guess_storage_grid[row][col-1] = None
                    curBox = letterBox_grid[row][col-1]
                else:
                    guess_storage_grid[row][col-1] = None

                currentWordLen -= 1
                user_input = user_input[:-1]
                drawEmptyBox(curRect)

            
            # if the cursor is in a empty box and the user enters a letter, it will be recorded
            # though recorded here, the letter entry is technically drawn to the GUI later on at the bottom of the loop
            elif len(user_input) < 1 and currentWordLen < 5 and event.key in pygame_alpha_keys:
                new_input = event.unicode + ""
                new_input = new_input.upper()
                user_input += new_input
                currentWordLen +=1

        
            # if the user has entered five letters and hit enter, the word will be evaluated and the next guess will start
            elif event.key == pygame.K_RETURN and currentWordLen == 5:
                row = curBox.placement[0]
                col = curBox.placement[1]
                guess_storage_grid[row][col] = user_input
                user_input = ""

                # conditional ensures the code does not try to jump to a seventh line and experience an index out of range error
                if row < 5:
                    curBox = letterBox_grid[row+1][0]
                    curRect = curBox.rectObj
                    currentWordLen = 0
                
                currentRowWord = []
    
                # checking if entered letters match, valid or perfect
                # valid: the letter is in the target word, but at a different index
                # perfect: the letter is in the target word at the same index
                for i in range(5):
                    currentRowWord.append(guess_storage_grid[row][i])
                    if currentRowWord[i] in targetWord:
                        letterBox_grid[row][i].validGuess = True
                    if currentRowWord[i] == targetWord[i]:
                        letterBox_grid[row][i].perfectGuess = True
                    if currentRowWord[i] not in targetWord:
                        tempCoords = kb_hash_ref[currentRowWord[i]]
                        tempX = tempCoords[0]
                        tempY = tempCoords[1]
                        tempKBobject = keyboard_grid[tempX][tempY]
                        tempKBobject.valid = False
                        tempKBobject.perfect = False

                # Check if user got the word correct
                if list(targetWord) == currentRowWord:
                    #gameRunning = False
                    print(f"VICTORY, YOU GUESSED {targetWord} IN {row+1} TRIES!")
                elif row == 5:
                    # game lost here unless last guess is correct
                    # simply end the game and close for now
                    gameRunning = False
                    print(f"YOU FAILED TO GUESS {targetWord} IN SIX TRIES")




    screen.fill((0,0,0))

    #set the Window icon
    iconIMG = pygame.image.load('icon2.png')
    pygame.display.set_icon(iconIMG)

    # draw the main Mordle logo onto the GUI
    logoIMG = pygame.image.load('logo.png').convert()
    logoRect = logoIMG.get_rect()
    logoRect.left = 20
    logoRect.top = 20
    screen.blit(logoIMG, logoRect)


    # loop through the 2D grid of letterboxes and draw each one to the GUI
    # O(n^2) time here is of no concern due to the small size (n = 30) of the grid
    for i in range(6):
        for j in range(5):
            tempLB = letterBox_grid[i][j]
            pygame.draw.rect(screen, (70,70,70), tempLB.rectObj)
            #print(tempLB.rectObj)


    # loop through 2D grid of keyboard letters and draw each one to the GUI
    for i in range(3):
        for j in range(10):
            if i == 0 or (i == 1 and j < 9) or (i == 2 and j < 7):
                tempKB = keyboard_grid[i][j]
                pygame.draw.rect(screen, (70,70,70), tempKB.rectObj)
                key_surface = keyboard_font.render(tempKB.letter, True, (255, 255, 255))
                screen.blit(key_surface, (tempKB.rectObj.x+10, tempKB.rectObj.y+5))
    
    
    # draw previous entered letters in their respective boxes

    for i in range(6):
        for j in range(5):
            tempGuess = guess_storage_grid[i][j]
            if tempGuess != None:
                #pygame.draw.rect(screen, (105,105,105), curRect)
                drawPrevGuess(letterBox_grid[i][j].rectObj, tempGuess)
                
                tempTuple = kb_hash_ref[tempGuess]
                tempX = tempTuple[0]
                tempY = tempTuple[1]
                tempLetterKey = keyboard_grid[tempX][tempY]
                if tempLetterKey.valid == False and tempLetterKey.perfect == False:
                    tempRect = tempLetterKey.rectObj
                    pygame.draw.rect(screen, (161, 33, 31), tempRect)
                    text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                    screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))
            
            if tempGuess == None:
                drawEmptyBox(letterBox_grid[i][j].rectObj)
            
            if letterBox_grid[i][j].perfectGuess == True:
                pygame.draw.rect(screen, (53, 133, 71), letterBox_grid[i][j].rectObj)
                drawPrevGuess(letterBox_grid[i][j].rectObj, tempGuess)
                
                tempTuple = kb_hash_ref[tempGuess]
                tempX = tempTuple[0]
                tempY = tempTuple[1]
                tempLetterKey = keyboard_grid[tempX][tempY]
                tempLetterKey.setPerfection(True)

                tempRect = tempLetterKey.rectObj
                pygame.draw.rect(screen, (53, 133, 71), tempRect)
                text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))
            
            elif letterBox_grid[i][j].validGuess == True:
                pygame.draw.rect(screen, (200, 175, 0), letterBox_grid[i][j].rectObj)
                drawPrevGuess(letterBox_grid[i][j].rectObj, tempGuess)

                tempTuple = kb_hash_ref[tempGuess]
                tempX = tempTuple[0]
                tempY = tempTuple[1]
                tempLetterKey = keyboard_grid[tempX][tempY]
                if tempLetterKey.perfect == False:
                    tempRect = tempLetterKey.rectObj
                    pygame.draw.rect(screen, (200, 175, 0), tempRect)
                    text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                    screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))


            


    drawCurrentGuess(curRect)
    pygame.display.flip()
    #pygame.display.update()

pygame.quit()
