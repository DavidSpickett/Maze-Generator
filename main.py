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
SOLVER_COLOUR = (255,0,0)
MAZE_COLOURS = [FLOOR_COLOUR, WALL_COLOUR, PATH_COLOUR]

def mazeArray(value):
    return [[value]*BOARD_HEIGHT for i in range(BOARD_WIDTH)]

def cellRect(x, y):
        return (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

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
        
    def draw(self, solver_x, solver_y):
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                cell_type = self.layout[i][j]
                screen.fill(MAZE_COLOURS[cell_type], cellRect(i, j))
        
        screen.fill(SOLVER_COLOUR, cellRect(solver_x, solver_y))
        
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
        
class mazeSolver():
    def __init__(self, maze, x=0, y=0):
        #Initial position in the maze given
        self.currentX = x
        self.currentY = y
        self.maze = maze
        self.neighbours = []
        self.stack = []
        
    def solve(self): 
        #Call this to find and make next move
        self.neighbours = []
        self.maze.layout[self.currentX][self.currentY] = PATH
        
        #Look for open cells    
        if (self.currentY-1) >= 0:
            if self.maze.layout[self.currentX][self.currentY-1] == FLOOR: #Above
                self.neighbours.append((self.currentX,self.currentY-1))
    
        if (self.currentX-1) >= 0:
            if self.maze.layout[self.currentX-1][self.currentY] == FLOOR: #Left
                self.neighbours.append((self.currentX-1,self.currentY))
        
        if (self.currentX < BOARD_WIDTH):
            if self.maze.layout[self.currentX+1][self.currentY] == FLOOR: #Right
                self.neighbours.append((self.currentX+1,self.currentY))

        if (self.currentY < BOARD_HEIGHT):
            if self.maze.layout[self.currentX][self.currentY+1] == FLOOR: #Down
                self.neighbours.append((self.currentX,self.currentY+1))
        
        if self.neighbours: #If we found some neighbours that are open
            newX, newY = self.neighbours[0] #Take the first option
            self.stack.append((self.currentX,self.currentY)) #Save old position to stack
            self.currentX = newX
            self.currentY = newY
            
        else: #Cell has no open neighbours
            if self.stack:
                #Go back to the previous current cell
                self.currentX, self.currentY = self.stack.pop()

        return self.currentX, self.currentY

def checkControls(maze): 
    #check player controls (return False if we need to quit)
    pygame.event.pump()    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_ESCAPE]:
        return False
        
    if key[pygame.K_TAB]:
        maze.__init__()
        screen.fill(FLOOR_COLOUR)
        maze.generate()
        solver.__init__(maze)
        
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x /= TILE_SIZE
            mouse_y /= TILE_SIZE
            
            if (newMaze.layout[mouse_x][mouse_y] != WALL):
                maze.ClearPath()
                solver.__init__(maze, x=mouse_x, y=mouse_y)
        elif event.type == pygame.QUIT:
            return False

    return True
               
newMaze = maze()
newMaze.generate()
solver = mazeSolver(newMaze)

try:
    run = True 
    solver_x, solver_y = 0, 0
    while run:
        newMaze.draw(solver_x, solver_y)
        run = checkControls(newMaze)
        pygame.display.flip()
        solver_x, solver_y = solver.solve()
finally:
    pygame.quit()