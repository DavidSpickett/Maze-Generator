'''
Created on Aug 5, 2010

@author: davidspickett
'''

import pygame, random
from pygame.locals import *

pygame.init()

BOARD_WIDTH  = 100
BOARD_HEIGHT = 50
TILE_SIZE    = 10

SCREEN_WIDTH  = BOARD_WIDTH*TILE_SIZE
SCREEN_HEIGHT = BOARD_HEIGHT*TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Maze Solver')

FLOOR = 0 
WALL  = 1
PATH  = 2

FLOOR_COLOUR = (0,0,0)
WALL_COLOUR = (255,255,255)
PATH_COLOUR = (0,255,0)
PLAYEER_COLOUR = (255,0,0)
MAZE_COLOURS = [FLOOR_COLOUR, WALL_COLOUR, PATH_COLOUR]

def mazeArray(value):
    return [[value]*BOARD_HEIGHT for i in range(BOARD_WIDTH)]

class maze(): #The main maze class
    def __init__(self):
        self.layout = mazeArray(WALL)
        self.visited = mazeArray(0)
        self.neighbours = []
        self.stack = []
        self.x = 0
        self.y = 0

    def ClearPath(self):
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                if self.layout[i][j] == PATH:
                    self.layout[i][j] = FLOOR
        
    def drawMaze(self):
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                cell_type = self.layout[i][j]
                screen.fill(MAZE_COLOURS[cell_type], (i*TILE_SIZE,j*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        
    def generate(self):
        while not self._generate():
            pass

    def _generate(self): 
        #Do one step of generating a layout.
        
        #Pick a cell and mark it as part of the maze
        self.layout[self.x][self.y] = FLOOR
        #Mark as visited
        self.visited[self.x][self.y] = True
        
        self.neighbours = [] #Reset neighbours
        
        #Look for unvisited neighbours    
        try:
            if (self.y-2) >= 0:
                if not self.visited[self.x][self.y-2]: #Above
                    self.neighbours.append((self.x,self.y-2))
        except IndexError:
            pass
        
        try:
            if (self.x-2) >= 0:
                if not self.visited[self.x-2][self.y]: #Left
                    self.neighbours.append((self.x-2,self.y))
        except IndexError:
            pass
        
        try:
            if not self.visited[self.x+2][self.y]: #Right
                self.neighbours.append((self.x+2,self.y))
        except IndexError:
            pass
        
        try:
            if not self.visited[self.x][self.y+2]: #Down
                self.neighbours.append((self.x,self.y+2))
        except IndexError:
            pass
        
        if self.neighbours:
            #Now choose one randomly
            newCell = self.neighbours[random.randint(0,len(self.neighbours)-1)]
        
            #Add current cell to the stack
            self.stack.append((self.x,self.y))
                     
            #Remove the wall between current and chosen cell
            newX, newY = newCell
        
            #Cell is above
            if newX == self.x and (newY+2) == self.y:
                self.layout[newX][newY+1] = FLOOR
            #Cell is below
            elif newX == self.x and (newY-2) == self.y:
                self.layout[newX][newY-1] = FLOOR
            #Cell is left
            elif (newX+2) == self.x and newY == self.y:
                self.layout[newX+1][newY] = FLOOR
            #Cell is right
            elif (newX-2) == self.x and newY == self.y:
                self.layout[newX-1][newY] = FLOOR
            
            self.x = newX
            self.y = newY
            
        else: #Cell has no neighbours
            if self.stack:
                #Go back to the previous current cell
                self.x, self.y = self.stack.pop() 
                
            if not self.stack:
                #Generation has finished
                return True

class player(): #The player
    def __init__(self):
        #This represents a mask showing what the player knows of the maze
        self.known = mazeArray(0)
        self.x = 0
        self.y = 0
        
    def checkControls(self): 
        #check player controls (return False if we need to quit)
        pygame.event.pump()    
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:
            return False
            
        if key[pygame.K_TAB]:
            newMaze.__init__()
            screen.fill(FLOOR_COLOUR)
            newMaze.generate()
            playerOne.__init__()
            solver.__init__(playerOne.x, playerOne.y)
            
        if key[pygame.K_UP]:
            if self.y != 0:
                if newMaze.layout[self.x][self.y-1] == FLOOR or newMaze.layout[self.x][self.y-1] == PATH:
                    newMaze.layout[self.x][self.y] = PATH
                    self.y -= 1
        
        if key[pygame.K_DOWN]:
            if self.y != (BOARD_HEIGHT-1):
                if newMaze.layout[self.x][self.y+1] == FLOOR or newMaze.layout[self.x][self.y+1] == PATH:
                    newMaze.layout[self.x][self.y] = PATH
                    self.y += 1
        
        if key[pygame.K_LEFT]:
            if self.x != 0:
                if newMaze.layout[self.x-1][self.y] == FLOOR or newMaze.layout[self.x-1][self.y] == PATH:
                    newMaze.layout[self.x][self.y] = PATH
                    self.x -= 1
        
        if key[pygame.K_RIGHT]:
            if self.Y != (BOARD_WIDTH-1):
                if newMaze.layout[self.x+1][self.y] == FLOOR or newMaze.layout[self.x+1][self.y] == PATH:
                    newMaze.layout[self.x][self.y] = PATH
                    self.x += 1
                    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX,mouseY = pygame.mouse.get_pos()
                self.x = mouseX/TILE_SIZE
                self.y = mouseY/TILE_SIZE
                newMaze.ClearPath()
                solver.__init__(self.x, self.y)
            elif event.type == pygame.QUIT:
                return False

        return True
    
    def draw(self):
        screen.fill(PLAYEER_COLOUR, self.TileRect())
        
    def TileRect(self):
        return (self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def update(self):
        #Note parts of the maze we have discovered
        self.known[self. x][self. y] = True
        self.known[self. x+1][self. y] = True
        self.known[self. x-1][self. y] = True
        self.known[self. x][self. y+1] = True
        self.known[self. x][self. y-1] = True
        self.known[self. x-1][self. y+1] = True
        self.known[self. x+1][self. y+1] = True
        self.known[self. x+1][self. y-1] = True
        self.known[self. x-1][self. y-1] = True
        
        self.draw()
        
class mazeSolver(): #Assists in solving the maze
    def __init__(self, x, y):
        self.currentX = x
        self.currentY = y
        self.neighbours = []
        self.stack = []
        
    def solve(self): 
        #Call this to find and make next move
        self.neighbours = []
        newMaze.layout[self.currentX][self.currentY] = PATH
        
        #Look for open cells    
        if (self.currentY-1) >= 0:
            if newMaze.layout[self.currentX][self.currentY-1] == FLOOR: #Above
                self.neighbours.append((self.currentX,self.currentY-1))
    
        if (self.currentX-1) >= 0:
            if newMaze.layout[self.currentX-1][self.currentY] == FLOOR: #Left
                self.neighbours.append((self.currentX-1,self.currentY))
        
        if (self.currentX < BOARD_WIDTH):
            if newMaze.layout[self.currentX+1][self.currentY] == FLOOR: #Right
                self.neighbours.append((self.currentX+1,self.currentY))

        if (self.currentY < BOARD_HEIGHT):
            if newMaze.layout[self.currentX][self.currentY+1] == FLOOR: #Down
                self.neighbours.append((self.currentX,self.currentY+1))
        
        if self.neighbours: #If we found some neighbours that are open
            newX, newY = self.neighbours[0] #Take the first option
            self.stack.append((self.currentX,self.currentY)) #Save old position to stack
            self.currentX = newX
            self.currentY = newY
            playerOne.X = self.currentX
            playerOne.Y = self.currentY
            
        else: #Cell has no open neighbours
            if self.stack:
                #Go back to the previous current cell
                self.currentX, self.currentY = self.stack.pop() 
                playerOne.X, playerOne.Y = self.currentX, self.currentY
               
newMaze = maze()
newMaze.generate()
playerOne = player()
solver = mazeSolver(playerOne.x, playerOne.y)
newMaze.drawMaze()

try:
    run = True 
    while run:
        newMaze.drawMaze()
        run = playerOne.checkControls()
        playerOne.update()
        pygame.display.flip()
        solver.solve()
finally:
    pygame.quit()