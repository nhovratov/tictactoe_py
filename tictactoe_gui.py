# Tic Tac Toe
# Nikita Hovratov
# Pygame version of the tictactoe game from Al Sweigart

import sys, pygame, random
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 645

PADDING = 25
GRIDSIZE = int(WINDOWWIDTH * 2/5)
WINDOWHEIGHT = int(2 * PADDING + GRIDSIZE)
UISIZE = int(WINDOWWIDTH - GRIDSIZE - 3 * PADDING)
CELLSIZE = int(GRIDSIZE / 3)

#           R    G    B
GRAY  =   (175, 175, 175)
WHITE =   (255, 255, 255)
BLACK =   (0,   0,   0)
BLUE  =   (0,   0,   255)

MARGIN = 35
MARGINBIG = 45

# Letter Selection
# (need to find a smart way to get positions other than count pixels)
POSX = (429, 110)
POSO = (480, 110)
SIZEX = (15, 18)
SIZEO = (20, 17)

def main():
    # setup variables
    global FPSCLOCK, DISPLAYSURF, GRIDSURF, INTERFACE, BASICFONT, BIGFONT
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    GRIDSURF = pygame.Surface((GRIDSIZE, GRIDSIZE))
    INTERFACE = pygame.Surface((UISIZE, WINDOWHEIGHT - 2 * PADDING))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 26)
    
    mousex = 0
    mousey = 0
    
    letterSelected = False
    playerLetter = None
    computerLetter = None
    turn = whoGoesFirst()

    pygame.display.set_caption('Tic Tac Toe')

    # Draw backgrounds
    DISPLAYSURF.fill(WHITE)
    GRIDSURF.fill(GRAY)
    INTERFACE.fill(WHITE)
    
    renderInitialText()
    drawBoard()
    
    # Merge Surfaces
    DISPLAYSURF.blit(GRIDSURF, (PADDING, PADDING))
    DISPLAYSURF.blit(INTERFACE, (GRIDSIZE + 2 * PADDING, PADDING))
    
    # Update view
    pygame.display.update()

    while True: # entry loop
        
        while not letterSelected: # wait for player to select letter
            mouseClicked = False
            checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

            # Onclick
            if mouseClicked:
                playerLetter = getLetterAtPixel(mousex, mousey)
                if playerLetter != None:
                    if playerLetter == 'X':
                        computerLetter = 'O'
                        printChoiceAndTurn(playerLetter, turn)
                    else:
                        computerLetter = 'X'
                        printChoiceAndTurn(playerLetter, turn)
                        
                    letterSelected = True
                    # Update view
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    
        # Now the game can start :)
        runGame(playerLetter, computerLetter, turn)


def runGame(playerLetter, computerLetter, turn):
    print("run the game")
    # Reset the board
    theBoard = [' '] * 10
    gameIsPlaying = True
    
    while gameIsPlaying: # game loop

        if turn == 'player':
            playerChoseCell = False
            
            while not playerChoseCell: # Player is choosing cell
                mouseClicked = False
                # Eventloop
                checkForQuit();
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouseClicked = True
                        
                # Onclick
                if mouseClicked:
                    cellClicked = getCellAtPixel(mousex, mousey)
                    if cellClicked != None:
                        playerChoseCell = True
                        print("player makes turn")
                        turn = 'computer'
        else:
            print("Computer turn")
            print("Computer makes turn")
            turn = 'player'

            pygame.display.update()
            FPSCLOCK.tick(FPS)

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
    # Blit Interface with main display again
    DISPLAYSURF.blit(INTERFACE, (GRIDSIZE + 2 * PADDING, PADDING))

def renderInitialText():
    welcomeSurf, welcomeRect = makeTextObjs("Welcome to TicTacToe!", BIGFONT)
    INTERFACE.blit(welcomeSurf, welcomeRect)

    chooseSurf, chooseRect = makeTextObjs("Do you want to be X or O?", BASICFONT)
    chooseRect.top = MARGINBIG
    INTERFACE.blit(chooseSurf, chooseRect)

    selectSurf, selectRect = makeTextObjs("X     O", BIGFONT, BLUE)
    selectRect.top = MARGINBIG + MARGIN
    selectRect.centerx = UISIZE / 2
    INTERFACE.blit(selectSurf, selectRect)

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
    
def leftTopCoordsOfCell(row, col):
    left = row * (CELLSIZE + 1) + PADDING
    top = col * (CELLSIZE + 1) + PADDING
    return (left, top)

def getCellAtPixel(x, y):
    for row in range(3):
        for col in range(3):
            left, top = leftTopCoordsOfCell(row, col)
            cellRect = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if cellRect.collidepoint(x, y):
                print(row, col)
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
