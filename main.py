'''
Created on Aug 5, 2010

@author: davidspickett
'''

import pygame, random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock() #Clock to limit frames per second
framesPerSecond = 30        #We want to run the game at 30fps

boardWidth  = 100
boardHeight = 50
tileSize    = 10

swidth  = boardWidth*tileSize
sheight = boardHeight*tileSize

font = pygame.font.Font(pygame.font.get_default_font(),20)

screen = pygame.display.set_mode((swidth,sheight))
pygame.display.set_caption('Maze Game')

FLOOR = 0 
WALL  = 1
PATH  = 2

FLOOR_COLOUR = (0,0,0)
WALL_COLOUR = (255,255,255)
PATH_COLOUR = (0,255,0)
COLOURS = [FLOOR_COLOUR, WALL_COLOUR, PATH_COLOUR]

class maze(): #The main maze class
    def __init__(self):
        self.layout = [[WALL]*boardHeight for i in range(boardWidth)]
        self.oldLayout = [[FLOOR]*boardHeight for i in range(boardWidth)]
        
        self.visited = [[0]*boardHeight for i in range(boardWidth)]
        self.neighbours = []
        self.stack = []
        
        #Used for generation
        self.currentX = 0
        self.currentY = 0
        
    def drawMaze(self):
        for i in range(boardWidth):
            for j in range(boardHeight):
                cell_type = self.layout[i][j]
                if (cell_type != self.oldLayout[i][j] or (i == playerOne.oldX and j == playerOne.oldY)):
                    screen.fill(COLOURS[cell_type], (i*tileSize,j*tileSize,tileSize,tileSize))
        
    def generate(self):
        while not self._generate():
            pass

    def _generate(self): 
        #Do one step of generating a layout.
        
        #Pick a cell and mark it as part of the maze
        self.layout[self.currentX][self.currentY] = FLOOR
        #Mark as visited
        self.visited[self.currentX][self.currentY] = True
        
        self.neighbours = [] #Reset neighbours
        
        #Look for unvisited neighbours    
        try:
            if (self.currentY-2) >= 0:
                if not self.visited[self.currentX][self.currentY-2]: #Above
                    self.neighbours.append((self.currentX,self.currentY-2))
        except IndexError:
            pass
        
        try:
            if (self.currentX-2) >= 0:
                if not self.visited[self.currentX-2][self.currentY]: #Left
                    self.neighbours.append((self.currentX-2,self.currentY))
        except IndexError:
            pass
        
        try:
            if not self.visited[self.currentX+2][self.currentY]: #Right
                self.neighbours.append((self.currentX+2,self.currentY))
        except IndexError:
            pass
        
        try:
            if not self.visited[self.currentX][self.currentY+2]: #Down
                self.neighbours.append((self.currentX,self.currentY+2))
        except IndexError:
            pass
        
        if self.neighbours:
            #Now choose one randomly
            newCell = self.neighbours[random.randint(0,len(self.neighbours)-1)]
        
            #Add current cell to the stack
            self.stack.append((self.currentX,self.currentY))
                     
            #Remove the wall between current and chosen cell
            newX, newY = newCell
        
            #Cell is above
            if newX == self.currentX and (newY+2) == self.currentY:
                self.layout[newX][newY+1] = FLOOR
            #Cell is below
            elif newX == self.currentX and (newY-2) == self.currentY:
                self.layout[newX][newY-1] = FLOOR
            #Cell is left
            elif (newX+2) == self.currentX and newY == self.currentY:
                self.layout[newX+1][newY] = FLOOR
            #Cell is right
            elif (newX-2) == self.currentX and newY == self.currentY:
                self.layout[newX-1][newY] = FLOOR
            
            self.currentX = newX
            self.currentY = newY
            
        else: #Cell has no neighbours
            if self.stack:
                #Go back to the previous current cell
                self.currentX, self.currentY = self.stack.pop() 
                
            if not self.stack:
                #Generation has finished
                return True

class player(): #The player
    def __init__(self):
        #This represents a mask showing what the player knows of the maze
        self.known = [[0]*boardHeight for i in range(boardWidth)]
         
        self.X = 0
        self.Y = 0       
        self.oldX = 99
        self.oldY = 99 
        
    def checkControls(self): 
        #check player controls (return False if we need to quit)
        pygame.event.pump()    
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:
            return False
            
        if key[pygame.K_TAB]:
            newMaze.__init__()
            screen.fill((0,0,0))
            newMaze.generate()
            playerOne.__init__()
            solver.__init__()
            
        if key[pygame.K_UP]:
            if self.Y != 0:
                if newMaze.layout[self.X][self.Y-1] == FLOOR or newMaze.layout[self.X][self.Y-1] == PATH:
                    newMaze.layout[self.X][self.Y] = PATH
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.Y -= 1
        
        if key[pygame.K_DOWN]:
            if self.Y != (boardHeight-1):
                if newMaze.layout[self.X][self.Y+1] == FLOOR or newMaze.layout[self.X][self.Y+1] == PATH:
                    newMaze.layout[self.X][self.Y] = PATH
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.Y += 1
        
        if key[pygame.K_LEFT]:
            if self.X != 0:
                if newMaze.layout[self.X-1][self.Y] == FLOOR or newMaze.layout[self.X-1][self.Y] == PATH:
                    newMaze.layout[self.X][self.Y] = PATH
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.X -= 1
        
        if key[pygame.K_RIGHT]:
            if self.Y != (boardWidth-1):
                if newMaze.layout[self.X+1][self.Y] == FLOOR or newMaze.layout[self.X+1][self.Y] == PATH:
                    newMaze.layout[self.X][self.Y] = PATH
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.X += 1
                    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX,mouseY = pygame.mouse.get_pos()
                solver.__init__()
                self.X = mouseX/tileSize
                self.Y = mouseY/tileSize

        return True
    
    def draw(self): #draw the player
        screen.fill((255,0,0), (self.X*tileSize,self.Y*tileSize,tileSize,tileSize))
        
    def update(self): #Combine all the previous
        
        #Note parts of the maze we have discovered
        self.known[self.X][self.Y] = 1
        self.known[self.X+1][self.Y] = 1
        self.known[self.X-1][self.Y] = 1
        self.known[self.X][self.Y+1] = 1
        self.known[self.X][self.Y-1] = 1
        self.known[self.X-1][self.Y+1] = 1
        self.known[self.X+1][self.Y+1] = 1
        self.known[self.X+1][self.Y-1] = 1
        self.known[self.X-1][self.Y-1] = 1
        
        self.draw()
        
class mazeSolver(): #Assists in solving the maze
    def __init__(self):
        self.currentX = playerOne.X
        self.currentY = playerOne.Y
        
        self.neighbours = []
        self.stack = []
        
    def solve(self): #Call this to find and make next move
        
        self.neighbours = [] #Reset neighbours
        newMaze.layout[self.currentX][self.currentY] = PATH
        
        #Look for open cells    
        try:
            if (self.currentY-1) >= 0:
                if newMaze.layout[self.currentX][self.currentY-1] == FLOOR: #Above
                    self.neighbours.append((self.currentX,self.currentY-1))
        except:
            print self.neighbours
        
        try:
            if (self.currentX-1) >= 0:
                if newMaze.layout[self.currentX-1][self.currentY] == FLOOR: #Left
                    self.neighbours.append((self.currentX-1,self.currentY))
        except:
            print self.neighbours
        
        try:
            if newMaze.layout[self.currentX+1][self.currentY] == FLOOR: #Right
                self.neighbours.append((self.currentX+1,self.currentY))
        except:
            print self.neighbours
        
        try:
            if newMaze.layout[self.currentX][self.currentY+1] == FLOOR: #Down
                self.neighbours.append((self.currentX,self.currentY+1))
        except:
            print self.neighbours
        
        if self.neighbours: #If we found some neighbours that are open
            newX, newY = self.neighbours[0] #Take the first option
            self.stack.append((self.currentX,self.currentY)) #Save old position to stack
            playerOne.oldX = self.currentX
            playerOne.oldY = self.currentY
            self.currentX = newX
            self.currentY = newY
            playerOne.X = self.currentX
            playerOne.Y = self.currentY
            
        else: #Cell has no open neighbours
            if self.stack:
                playerOne.oldX = self.currentX
                playerOne.oldY = self.currentY
                #Go back to the previous current cell
                self.currentX, self.currentY = self.stack.pop() 
                playerOne.X, playerOne.Y = self.currentX, self.currentY
               
newMaze = maze()
newMaze.generate()
playerOne = player()
solver = mazeSolver()
newMaze.drawMaze()

run = True 
while run:
    newMaze.drawMaze()
    newMaze.oldLayout= newMaze.layout #Save layout
    run = playerOne.checkControls()
    playerOne.update()
    pygame.display.flip()
    solver.solve()

pygame.quit()