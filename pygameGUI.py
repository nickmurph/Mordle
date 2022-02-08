from tabnanny import check
import pygame
from pygameAlphaKeys import pygame_alpha_keys 
from main import fiveLetterWords
from main import getRandomWord
import tkinter as tk
from tkinter import messagebox
import time

# PyGame basic global vars to set up the GUI box
pygame.init()
screen = pygame.display.set_mode([460,750])
# using the below screen declaration will create a window with the title bar or min/close buttons, this is a workaround for the GUI warping issue caused by user moving the window, but unsatisfactory for final product
# screen = pygame.display.set_mode([460,750], pygame.NOFRAME)
user_font = pygame.font.Font(None, 80)
keyboard_font = pygame.font.Font(None, 40)
qwertyList = list("QWERTYUIOPASDFGHJKLZXCVBNM")
pygame.display.set_caption('Moredle')
screen.fill((0,0,0))
#set the Window icon
iconIMG = pygame.image.load('icon.png')
pygame.display.set_icon(iconIMG)

# creating a Tkinter window, then hiding it 
# this allows the usage of messagebox popups
tk_root = tk.Tk()
tk_root.withdraw()

# the commented out lines below show a greeting message when the app opens
# commented out for now because it feels like too much friction; anyone playing Mordle will be familiar with Wordle

#tk.messagebox.askyesno("askyesno", "Find the value?")
# greeting_message = """                      Welcome to Mordle!

# Mordle is a Wordle-clone for the desktop, written in Python.

# You have 6 attempts to guess the word, good luck!

# """

# messagebox.showinfo("Welcome", greeting_message)



# LetterBox class wraps around a PyGame rectangle object and helper attributes
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

# KeyboardLetter class wraps around a Pygame rectangle object and helper attributes
# At the bottom of the GUI is a crude representation of a QWERTY keyboard
# Each of these 26 letters is represented by a KeyboardLetter object in a 3x(10,9,7) grid
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



# Creates a LetterBox object and stores it in the 2D grid at the appropriate row,col coordinate
# Each LetterBox is wrapped around a PyGame Rect object, which needs left, top, width, and height coordinates
# The coordinates are adjusted within the loop to provide for proper spacing on the GUI, depending on row and col
# the various kb_xyz variables represent coordinates for a letter box to be placed at, incremented according to their place on the GUI
def populate_letterbox_grid(lb_grid):
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
            lb_grid[i][j] = LetterBox((i,j), pygame.Rect(lb_left,lb_top,lb_width,lb_height))


# Creates a KeyboardLetter object and stores it in the 2D grid representing a QWERTY layout (1x10, 1x9, 1x7)
# the various kb_xyz variables represent coordinates for a keyboard letter to be placed at, incremented according to their place on the GUI
def populate_keyboard(kb_grid, kb_dict):
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
                kb_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_dict[tempLetter] = (i,j)
                counter += 1
            elif i == 1 and j < 9:
                tempLetter = qwertyList[counter]
                if j > 0:
                    kb_left = kb_left + 49
                kb_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_dict[tempLetter] = (i,j)
                counter += 1
            elif i == 2 and j < 7:
                tempLetter = qwertyList[counter]
                if j > 0:
                    kb_left = kb_left + 55
                kb_grid[i][j] = KeyboardLetter(tempLetter, pygame.Rect(kb_left, kb_top, kb_width, kb_height))
                kb_dict[tempLetter] = (i,j)
                counter += 1                

# draws the guess, whatever is currently in user_input, into the rect provided as an argument
def drawCurrentGuess(rect):
    text_surface = user_font.render(user_input, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))
    pygame.display.flip()

# draw a previously guessed letter onto the Rect in a LetterBox
# used when the loop updates the GUI each frame, so that previous letters persist
def drawPrevGuess(rect, guessText):
    text_surface = user_font.render(guessText, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))

# Currently deprecated, used previously to specifically draw a letter that was perfectly placed, meaning its LetterBox rect turned green
# def drawPerfectGuess(rect, guessLetter):
#     text_surface = user_font.render(guessLetter, True, (50,255,168))
#     screen.blit(text_surface, (rect.x+30, rect.y+5))


def drawEmptyBox(rect):
    text_surface = user_font.render("", True, (255, 255, 255))
    screen.blit(text_surface, (rect.x+30, rect.y+5))

# returns the LetterKey object that represents the Rect holding the letter, "guess"
# e.g., the player has entered the letter A into a LetterBox during gameplay and that is our "guess" argument
# Use the keyboard_lookup_dict to get the coordinates mapped to the letter A
# Use those coordinates to access the relevant space in the keyboard_grid for that letter (in the case of A, (1,0), the second row and first letter in that row)
def getLetterKeyFromGuess(guess):
    tempTuple = keyboard_lookup_dict[guess]
    tempX = tempTuple[0]
    tempY = tempTuple[1]
    tempLetterKey = keyboard_grid[tempX][tempY]
    return tempLetterKey

# Given a row, get the five letter stored in that row, combine them
# while adding each letter to the row word, check whether its a perfect, valid, or invalid letter
# update the validity/perfection status of the word in letterbox and keyboard grids
# return the letters from the row as one word, currentRowWord
def getAndValidateRowWord(row, guess_storage_grid, letterbox_grid):
    currentRowWord = []
    for i in range(5):
        currentRowWord.append(guess_storage_grid[row][i])
        if currentRowWord[i] in targetWord:
            letterbox_grid[row][i].validGuess = True
        if currentRowWord[i] == targetWord[i]:
            letterbox_grid[row][i].perfectGuess = True
        if currentRowWord[i] not in targetWord:
            tempKBobject = getLetterKeyFromGuess(currentRowWord[i])
            tempKBobject.valid = False
            tempKBobject.perfect = False
    return currentRowWord

# main game loop
game_running = True
while game_running:

    #game-scoped variables that reset with each new round
    user_input = ""
    targetWord = getRandomWord(fiveLetterWords)
    letterbox_grid = [[None]*5 for i in range(6)]
    guess_storage_grid = [[None]*5 for i in range(6)]
    keyboard_grid = [[None]*10, [None]*9, [None]*7]
    keyboard_lookup_dict = {}
    currentWordLen = 0

    # Fill the letterbox and keyboard grids with their relative objects, then set tracking variables for current letterbox and Rect
    populate_letterbox_grid(letterbox_grid)
    populate_keyboard(keyboard_grid, keyboard_lookup_dict)
    curBox = letterbox_grid[0][0]
    curRect = curBox.rectObj


# individual round loop
    round_in_progress = True
    while round_in_progress:    

        # if the user has entered a letter into an empty box, the cursor will progress to the next box
        if len(user_input) == 1 and currentWordLen < 5:
            row = curBox.placement[0]
            col = curBox.placement[1]

            guess_storage_grid[row][col] = user_input
            user_input = ""
            curBox = letterbox_grid[row][col+1]
            curRect = curBox.rectObj



        # handling user generated events     
        for event in pygame.event.get():

            # attempting to solve issue of moving window messing up the pygame Rect objects drawn to screen
            # did not solve issue, but keeping here for potential alternate solutions based on this approach
            # if not bool(pygame.mouse.get_focused()):
            #     screen.fill((0,0,0))
            #     pygame.display.flip()


            if event.type == pygame.QUIT:
                round_in_progress = False
                game_running = False

            # if any key has been pressed
            if event.type == pygame.KEYDOWN:
                # end the game when user hits ESC    
                if event.key == pygame.K_ESCAPE:
                    round_in_progress = False
                    game_running = False
                
                # if the user has entered backspace, and there are any entered letters capable of being removed, do so
                if event.key == pygame.K_BACKSPACE:
                    row = curBox.placement[0]
                    col = curBox.placement[1]

                    if currentWordLen == 0:
                        break     
                    elif currentWordLen == 1:
                        guess_storage_grid[row][0] = None
                        curBox = letterbox_grid[row][0]
                    elif currentWordLen == 5:
                        guess_storage_grid[row][4] = None
                    elif guess_storage_grid[row][col] == None:
                        guess_storage_grid[row][col-1] = None
                        curBox = letterbox_grid[row][col-1]
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
                        curBox = letterbox_grid[row+1][0]
                        curRect = curBox.rectObj
                        currentWordLen = 0
                    
                    currentRowWord = getAndValidateRowWord(row, guess_storage_grid, letterbox_grid)
        
                    # Check if user got the word correct
                    if list(targetWord) == currentRowWord:
                        print(f"VICTORY, YOU GUESSED {targetWord} IN {row+1} TRIES!")
                        round_in_progress = False
                        victory_message = f"""You correctly guessed {targetWord} in {row+1} tries. Would you like to try a new word?"""
                        victory_response = messagebox.askyesno("Correct", victory_message)
                        if victory_response == 'yes':
                            pass
                        else:
                            round_in_progress = False
                            break
                    elif row == 5:
                        # game lost here unless last guess is correct
                        print(f"YOU FAILED TO GUESS {targetWord} IN SIX TRIES")
                        #round_in_progress = False
                        failure_message = f"""You failed to guess {targetWord} in six tries. Would you like to try a new word?"""
                        failure_response = messagebox.askyesno("Incorrect", failure_message)
                        if failure_response == 'yes':
                            pass
                        else:
                            round_in_progress = False
                            break


        # paint the background black again, to avoid any bleed-through
        screen.fill((0,0,0))

        # draw the main Mordle logo onto the GUI
        # This must be done each frame because of the above background painting
        logoIMG = pygame.image.load('logo.png').convert()
        logoRect = logoIMG.get_rect()
        logoRect.left = 20
        logoRect.top = 20
        screen.blit(logoIMG, logoRect)


        # loop through the 2D grid of letterboxes and draw each one to the GUI
        # O(n^2) time here is of no concern due to the small size (n = 30) of the grid
        for i in range(6):
            for j in range(5):
                tempLB = letterbox_grid[i][j]
                pygame.draw.rect(screen, (70,70,70), tempLB.rectObj)


        # loop through 2D grid of keyboard letters and draw each one to the GUI
        for i in range(3):
            for j in range(10):
                # these checks necessary because the keyboard has decreasingly smaller rows, as a QWERTY does
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
                    drawPrevGuess(letterbox_grid[i][j].rectObj, tempGuess)
                    tempLetterKey = getLetterKeyFromGuess(tempGuess)
                    if tempLetterKey.valid == False and tempLetterKey.perfect == False:
                        tempRect = tempLetterKey.rectObj
                        pygame.draw.rect(screen, (161, 33, 31), tempRect)
                        text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                        screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))
                
                if tempGuess == None:
                    drawEmptyBox(letterbox_grid[i][j].rectObj)
                
                if letterbox_grid[i][j].perfectGuess == True:
                    pygame.draw.rect(screen, (53, 133, 71), letterbox_grid[i][j].rectObj)
                    drawPrevGuess(letterbox_grid[i][j].rectObj, tempGuess)
                    tempLetterKey = getLetterKeyFromGuess(tempGuess)
                    tempLetterKey.setPerfection(True)
                    tempRect = tempLetterKey.rectObj

                    pygame.draw.rect(screen, (53, 133, 71), tempRect)
                    text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                    screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))
                
                elif letterbox_grid[i][j].validGuess == True:
                    pygame.draw.rect(screen, (200, 175, 0), letterbox_grid[i][j].rectObj)
                    drawPrevGuess(letterbox_grid[i][j].rectObj, tempGuess)
                    tempLetterKey = getLetterKeyFromGuess(tempGuess)
                    
                    if tempLetterKey.perfect == False:
                        tempRect = tempLetterKey.rectObj
                        pygame.draw.rect(screen, (200, 175, 0), tempRect)
                        text_surface =  keyboard_font.render(tempGuess, True, (255, 255, 255))
                        screen.blit(text_surface, (tempRect.x+10, tempRect.y+5))

        # at the end of each frame, draw the current guess to the board
        # then update all pygame objects                
        drawCurrentGuess(curRect)
        pygame.display.flip()
pygame.quit()
