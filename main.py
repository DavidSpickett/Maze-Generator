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

font = pygame.font.Font(pygame.font.get_default_font(),20) #Use default system font

screen = pygame.display.set_mode((swidth,sheight))
pygame.display.set_caption('Maze Game')        #Set window title

class maze(): #The main maze class
    def __init__(self):
        self.layout = [[1 for i in range(boardHeight)] for i in range(boardWidth)]
        #1 is a wall, 0 is floor
        self.oldLayout = [[0 for i in range(boardHeight)] for i in range(boardWidth)]
        
        #Init the visited list
        self.visited = [[0 for i in range(boardHeight)] for i in range(boardWidth)]
        
        #Init the neighbours list
        self.neighbours = []
        
        #Stack
        self.stack = []
        
        #Used for generation
        self.currentX = 0
        self.currentY = 0
        
    def drawMaze(self): #Draws out the maze to the screen
        global screen, tileSize, boardWidth, boardHeight
        
        for i in range(boardWidth):
            for j in range(boardHeight):
                if (self.layout[i][j] != self.oldLayout[i][j] or (i == playerOne.oldX and j == playerOne.oldY)):
                    #or playerOne.known[i][j] == 1):
                    if self.layout[i][j] == 0:
                        screen.fill((0,0,0), (i*tileSize,j*tileSize,tileSize,tileSize))
                    if self.layout[i][j] == 1:
                        screen.fill((255,255,255), (i*tileSize,j*tileSize,tileSize,tileSize))
                    if self.layout[i][j] == 2:
                        screen.fill((0,255,0), (i*tileSize,j*tileSize,tileSize,tileSize))
        
    def generate(self): #Generates a new layout
        
        #Pick a cell and mark it as part of the maze
        self.layout[self.currentX][self.currentY] = 0
        #Mark as visited
        self.visited[self.currentX][self.currentY] = 1
        
        self.neighbours = [] #Reset neighbours
        
        #Look for unvisited neighbours    
        try:
            if (self.currentY-2) >= 0:
                if self.visited[self.currentX][self.currentY-2] == 0: #Above
                    self.neighbours.append((self.currentX,self.currentY-2))
        except:
            pass
        
        try:
            if (self.currentX-2) >= 0:
                if self.visited[self.currentX-2][self.currentY] == 0: #Left
                    self.neighbours.append((self.currentX-2,self.currentY))
        except:
            pass
        
        try:
            if self.visited[self.currentX+2][self.currentY] == 0: #Right
                self.neighbours.append((self.currentX+2,self.currentY))
        except:
            pass
        
        try:
            if self.visited[self.currentX][self.currentY+2] == 0: #Down
                self.neighbours.append((self.currentX,self.currentY+2))
        except:
            pass
        
        if len(self.neighbours) > 0: #If the current cell has neighbours
            #Now choose one randomly
            newCell = self.neighbours[random.randint(0,len(self.neighbours)-1)]
        
            #Add current cell to the stack
            self.stack.append((self.currentX,self.currentY))
                     
            #Remove the wall between current and chosen cell
            newX, newY = newCell
        
            #Cell is above
            if newX == self.currentX and (newY+2) == self.currentY:
                self.layout[newX][newY+1] = 0 #Remove the wall
        
            #Cell is below
            if newX == self.currentX and (newY-2) == self.currentY:
                self.layout[newX][newY-1] = 0
        
            #Cell is left
            if (newX+2) == self.currentX and newY == self.currentY:
                self.layout[newX+1][newY] = 0
        
            #Cell is right
            if (newX-2) == self.currentX and newY == self.currentY:
                self.layout[newX-1][newY] = 0
            
            self.currentX = newX
            self.currentY = newY
            
        else: #Cell has no neighbours
            if len(self.stack) > 0:
                self.currentX, self.currentY = self.stack[len(self.stack)-1] #Go back to the previous current cell
                del self.stack[len(self.stack)-1]
                
            if len(self.stack) == 0:
                return 9

class player(): #The player
    def __init__(self):
        #set = 0
        #while set == 0:
        #    randomX = random.randint(0,boardWidth-1)
        #    randomY = random.randint(0,boardHeight-1)
        #    
        #    if newMaze.layout[randomX][randomY] == 0:
        #        self.X = randomX
        #        self.Y = randomY #X and Y in terms of the grid
        #        set = 1
        
        #This represents a mask showing what the player knows of the maze
        self.known    = [[0 for i in range(boardHeight)] for i in range(boardWidth)]
         
        self.X = 0
        self.Y = 0       
        self.oldX = 99
        self.oldY = 99 
        
    def checkControls(self): #check player controls
        global done
        
        pygame.event.pump()            #Refresh events
        key = pygame.key.get_pressed() #State of all keys
        
        if key[pygame.K_ESCAPE]:
            done = 1 #Quit emulator
            
        if key[pygame.K_TAB]:
            newMaze.__init__()
            screen.fill((0,0,0))
            while newMaze.generate() != 9: pass
            playerOne.__init__()
            solver.__init__()
            
        if key[pygame.K_UP]:
            if self.Y != 0:
                if newMaze.layout[self.X][self.Y-1] == 0 or newMaze.layout[self.X][self.Y-1] == 2:
                    newMaze.layout[self.X][self.Y] = 2
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.Y -= 1
        
        if key[pygame.K_DOWN]:
            if self.Y != (boardHeight-1):
                if newMaze.layout[self.X][self.Y+1] == 0 or newMaze.layout[self.X][self.Y+1] == 2:
                    newMaze.layout[self.X][self.Y] = 2
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.Y += 1
        
        if key[pygame.K_LEFT]:
            if self.X != 0:
                if newMaze.layout[self.X-1][self.Y] == 0 or newMaze.layout[self.X-1][self.Y] == 2:
                    newMaze.layout[self.X][self.Y] = 2
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.X -= 1
        
        if key[pygame.K_RIGHT]:
            if self.Y != (boardWidth-1):
                if newMaze.layout[self.X+1][self.Y] == 0 or newMaze.layout[self.X+1][self.Y] == 2:
                    newMaze.layout[self.X][self.Y] = 2
                    self.oldX = self.X
                    self.oldY = self.Y
                    self.X += 1
                    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX,mouseY = pygame.mouse.get_pos()
                solver.__init__() #Reset solver
                self.X = mouseX/tileSize
                self.Y = mouseY/tileSize
    
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
        
        self.checkControls()
        self.draw()
        
class mazeSolver(): #Assists in solving the maze
    def __init__(self):
        self.currentX = playerOne.X
        self.currentY = playerOne.Y
        
        self.neighbours = []
        self.stack = []
        
    def solve(self): #Call this to find and make next move
        
        self.neighbours = [] #Reset neighbours
        newMaze.layout[self.currentX][self.currentY] = 2 #Mark path green
        
        #Look for open cells    
        try:
            if (self.currentY-1) >= 0:
                if newMaze.layout[self.currentX][self.currentY-1] == 0: #Above
                    self.neighbours.append((self.currentX,self.currentY-1))
        except:
            print self.neighbours
        
        try:
            if (self.currentX-1) >= 0:
                if newMaze.layout[self.currentX-1][self.currentY] == 0: #Left
                    self.neighbours.append((self.currentX-1,self.currentY))
        except:
            print self.neighbours
        
        try:
            if newMaze.layout[self.currentX+1][self.currentY] == 0: #Right
                self.neighbours.append((self.currentX+1,self.currentY))
        except:
            print self.neighbours
        
        try:
            if newMaze.layout[self.currentX][self.currentY+1] == 0: #Down
                self.neighbours.append((self.currentX,self.currentY+1))
        except:
            print self.neighbours
        
        if len(self.neighbours) > 0: #If we found some neighbours that are open
            newX, newY = self.neighbours[0] #Take the first option
            self.stack.append((self.currentX,self.currentY)) #Save old position to stack
            playerOne.oldX = self.currentX
            playerOne.oldY = self.currentY
            self.currentX = newX
            self.currentY = newY
            playerOne.X = self.currentX
            playerOne.Y = self.currentY
            
        else: #Cell has no open neighbours
            if len(self.stack) > 0:
                playerOne.oldX = self.currentX
                playerOne.oldY = self.currentY
                self.currentX, self.currentY = self.stack[len(self.stack)-1] #Go back to the previous current cell
                playerOne.X, playerOne.Y = self.stack[len(self.stack)-1]
                del self.stack[len(self.stack)-1]
               
newMaze = maze()
done = 0
while newMaze.generate() != 9: pass
playerOne = player()
solver = mazeSolver()
newMaze.drawMaze()
 
while done == 0: #main loop
    
    newMaze.drawMaze()
    newMaze.oldLayout= newMaze.layout #Save layout
    playerOne.update()
    pygame.display.flip()
    solver.solve()
    
    #for i in range(len(playerOne.known)):
    #    print playerOne.known[i]
        
    #deltat = clock.tick(framesPerSecond)

