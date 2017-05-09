# Tic Tac Toe
# Nikita Hovratov
# Pygame version of the tictactoe game from Al Sweigart

import sys, pygame, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 645
PADDING = 25

# Grid
GRIDSIZE = int(WINDOWWIDTH * 2/5)
WINDOWHEIGHT = int(2 * PADDING + GRIDSIZE)
CELLSIZE = int(GRIDSIZE / 3)
GRIDRECT = (PADDING, PADDING)

# UI
UISIZE = int(WINDOWWIDTH - GRIDSIZE - 3 * PADDING)
UIRECT = (GRIDSIZE + 2 * PADDING, PADDING)

#           R    G    B
GRAY  =   (175, 175, 175)
WHITE =   (255, 255, 255)
BLACK =   (0,   0,   0)
BLUE  =   (0,   0,   255)

# Text Margin
MARGIN = 35
MARGINBIG = 45

# Letter Selection
LETTERSIZE = 65
POSX = (2 * PADDING + GRIDSIZE, PADDING + MARGINBIG + MARGIN)
POSO = (2 * PADDING + GRIDSIZE + LETTERSIZE + PADDING, PADDING + MARGINBIG + MARGIN)
SIZEX = (LETTERSIZE, LETTERSIZE)
SIZEO = (LETTERSIZE, LETTERSIZE)

# X and O sprites
imageX = pygame.image.load("x.png")
imageX = pygame.transform.scale(imageX, (LETTERSIZE, LETTERSIZE))
imageO = pygame.image.load("o.png")
imageO = pygame.transform.scale(imageO, (LETTERSIZE, LETTERSIZE))

def main():
    # Define globals
    global FPSCLOCK, DISPLAYSURF, GRIDSURF, INTERFACE, BASICFONT, BIGFONT
    pygame.init()
    
    # Create Clock
    FPSCLOCK = pygame.time.Clock()

    # Create Surfaces
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GRIDSURF = pygame.Surface((GRIDSIZE, GRIDSIZE))
    INTERFACE = pygame.Surface((UISIZE, WINDOWHEIGHT - 2 * PADDING))
    
    # Define Fonts
    BASICFONT = pygame.font.SysFont('MonoSpace', 18)
    BIGFONT = pygame.font.SysFont('MonoSpace', 24)
    
    mousex = 0
    mousey = 0

    while True:
        # Set caption
        pygame.display.set_caption('Tic Tac Toe')

        # Draw backgrounds
        DISPLAYSURF.fill(WHITE)
        GRIDSURF.fill(GRAY)
        INTERFACE.fill(WHITE)

        # Paint
        renderInitialText()
        drawBoard()
        
        # Merge Surfaces
        DISPLAYSURF.blit(GRIDSURF, GRIDRECT)
        DISPLAYSURF.blit(INTERFACE, UIRECT)
        
        # Update view
        pygame.display.update()

        # Init variables
        turn = whoGoesFirst()
        playerLetter, computerLetter = playerLetterChoice()

        printChoiceAndTurn(playerLetter, turn)
        pygame.display.update()
        
        # Now the game can start :)
        runGame(playerLetter, computerLetter, turn)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def playerLetterChoice():
    while True:
        mouseClicked = False
        checkForQuit()
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if mouseClicked:
            playerLetter = getLetterAtPixel(mousex, mousey)
            if playerLetter != None:
                if playerLetter == 'X':
                    computerLetter = 'O'
                    return (playerLetter, computerLetter)
                else:
                    computerLetter = 'X'
                    return (playerLetter, computerLetter)
        FPSCLOCK.tick(FPS)

def runGame(playerLetter, computerLetter, turn):
    theBoard = []
    for i in range(3):
        theBoard.append([' '] * 3)

    gameIsPlaying = True    
    while gameIsPlaying:
        if turn == 'player':
            playerDecidesMove = True
            while playerDecidesMove:
                mouseClicked = False
                checkForQuit();
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouseClicked = True
                        
                if mouseClicked:
                    cellClicked = getCellAtPixel(mousex, mousey)
                    if cellClicked != None:
                        if isSpaceFree(theBoard, cellClicked):
                            playerDecidesMove = False
                            makeMove(theBoard, playerLetter, cellClicked)
                            updateGrid(theBoard)
                            if isWinner(theBoard, playerLetter):
                                print("Player has won!")
                                gameIsPlaying = False
                            if isBoardFull(theBoard):
                                print("Its a tie!")
                                gameIsPlaying = False
                            turn = 'computer'
                FPSCLOCK.tick(FPS)
        else:
            computerMove = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, computerMove)
            updateGrid(theBoard)
            if isWinner(theBoard, computerLetter):
                print("computer won")
                gameIsPlaying = False
            if isBoardFull(theBoard):
                print("Its a tie")
                gameIsPlaying = False
            turn = 'player'

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def getCopyOfBoard(board):
    copy = []
    for row in range(3):
        copy.append(board[row][:])
    return copy
            
def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # 1. Can we win in the next move?
    for row in range(3):
        for col in range(3):
            copy = getCopyOfBoard(board)
            if isSpaceFree(copy, (row, col)):
                makeMove(copy, computerLetter, (row, col))
                if isWinner(copy, computerLetter):
                    return (row, col)
    # 2. Can the player win in the next move? Block him!
    for row in range(3):
        for col in range(3):
            copy = getCopyOfBoard(board)
            if isSpaceFree(copy, (row, col)):
                makeMove(copy, playerLetter, (row, col))
                if isWinner(copy, playerLetter):
                    return (row, col)
    # 3. I try take one of the corners
    move = chooseRandomMoveFromList(board, [(0,0), (0,2), (2,0), (2,2)])
    if move != None:
        return move
    # 4. I try to take the center if its free
    if isSpaceFree(board, (1,1)):
        return (1,1)
    # 5. Move on one of the sides
    return chooseRandomMoveFromList(board, [(1,0),(0,1),(2,1),(1,2)])
                

def chooseRandomMoveFromList(board, moveList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in moveList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def isBoardFull(board):
    for row in range(3):
        for col in range(3):
            if isSpaceFree(board, (row, col)):
                return False
    return True

def isWinner(bo, le):
    return ((bo[0][0] == le and bo[1][0] == le and bo[2][0] == le) or # across the top
            (bo[0][1] == le and bo[1][1] == le and bo[2][1] == le) or # across the middle
            (bo[0][2] == le and bo[1][2] == le and bo[2][2] == le) or # across the bottom
            (bo[0][0] == le and bo[0][1] == le and bo[0][2] == le) or # down the left side
            (bo[1][0] == le and bo[1][1] == le and bo[1][2] == le) or # down the middle
            (bo[2][0] == le and bo[2][1] == le and bo[2][2] == le) or # down the right side
            (bo[0][0] == le and bo[1][1] == le and bo[2][2] == le) or # diagonal topleft downright
            (bo[0][2] == le and bo[1][1] == le and bo[2][0] == le)) # diagonal bottomleft topright

def updateGrid(board):
    for row in range(3):
        for col in range(3):
            letter = board[row][col]
            if letter != ' ':
                if letter == 'X':
                    imageToBlit = imageX
                else:
                    imageToBlit = imageO
                DISPLAYSURF.blit(imageToBlit, (getDistanceOfCell(row) + 10, getDistanceOfCell(col) + 10))

def isSpaceFree(board, move):
    return board[move[0]][move[1]] == ' '

def makeMove(board, letter, move):
    board[move[0]][move[1]] = letter

def printChoiceAndTurn(pLetter, turn):
    # Reset Interface
    INTERFACE.fill(WHITE)
    
    choiceSurf, choiceRect = makeTextObjs("You are " + pLetter, BASICFONT)
    INTERFACE.blit(choiceSurf, choiceRect)

    if turn == 'player':
        text = "You go first"
    else:
        text = "The computer goes first"
        
    turnSurf, turnRect = makeTextObjs(text, BASICFONT)
    turnRect.top = MARGIN
    INTERFACE.blit(turnSurf, turnRect)
    DISPLAYSURF.blit(INTERFACE, UIRECT)

def renderInitialText():
    welcomeSurf, welcomeRect = makeTextObjs("Welcome to TicTacToe!", BIGFONT)
    chooseSurf, chooseRect = makeTextObjs("Do you want to be X or O?", BASICFONT)
    chooseRect.top = MARGINBIG
    
    INTERFACE.blit(welcomeSurf, welcomeRect)
    INTERFACE.blit(chooseSurf, chooseRect)
    INTERFACE.blit(imageX, (0, MARGINBIG + MARGIN))
    INTERFACE.blit(imageO, (LETTERSIZE + PADDING, MARGINBIG + MARGIN))

def drawBoard():                
    pygame.draw.line(GRIDSURF, WHITE, (CELLSIZE, 0), (CELLSIZE, GRIDSIZE))
    pygame.draw.line(GRIDSURF, WHITE, (CELLSIZE * 2, 0), (CELLSIZE * 2, GRIDSIZE))
    pygame.draw.line(GRIDSURF, WHITE, (0, CELLSIZE), (GRIDSIZE, CELLSIZE))
    pygame.draw.line(GRIDSURF, WHITE, (0, CELLSIZE * 2), (GRIDSIZE, CELLSIZE * 2))

def whoGoesFirst():
     # Randomly choose the player who goes first.
     if random.randint(0, 1) == 0:
         return 'computer'
     else:
         return 'player'

def getDistanceOfCell(coord):
    return coord * (CELLSIZE + 1) + PADDING

def leftTopCoordsOfCell(row, col):
    left = getDistanceOfCell(row)
    top = getDistanceOfCell(col)
    return (left, top)

def getCellAtPixel(x, y):
    for row in range(3):
        for col in range(3):
            left, top = leftTopCoordsOfCell(row, col)
            cellRect = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if cellRect.collidepoint(x, y):
                return (row, col)
    return None

def getLetterAtPixel(x, y):
    letterRect = pygame.Rect(POSX, SIZEX)
    if letterRect.collidepoint(x, y):
        return 'X'
    else:
        letterRect = pygame.Rect(POSO, SIZEO)
        if letterRect.collidepoint(x, y):
            return 'O'
    return None
    

def makeTextObjs(text, font, color = BLACK):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()
    
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

if __name__ == '__main__':
    main()
