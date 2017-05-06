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

        self.generate()

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
        pygame.display.flip()
        
    def generate(self):
        while not self._generate_step():
            pass

    def _generate_step(self): 
        #Do one step of generating a layout.
        
        #Pick a cell and mark it as part of the maze
        self.layout[self.x][self.y] = FLOOR
        #Mark as visited
        self.visited[self.x][self.y] = True
        
        self.neighbours = [] #Reset neighbours
        
        #Look for unvisited neighbours    
        if (self.y-2) >= 0:
            if not self.visited[self.x][self.y-2]: #Above
                self.neighbours.append((self.x,self.y-2))
        
        if (self.x-2) >= 0:
            if not self.visited[self.x-2][self.y]: #Left
                self.neighbours.append((self.x-2,self.y))
        
        if (self.x+2) < BOARD_WIDTH:
            if not self.visited[self.x+2][self.y]: #Right
                self.neighbours.append((self.x+2,self.y))
        
        if (self.y+2) < BOARD_HEIGHT:
            if not self.visited[self.x][self.y+2]: #Down
                self.neighbours.append((self.x,self.y+2))
        
        if self.neighbours:
            #Now choose one randomly
            newCell = self.neighbours[random.randint(0,len(self.neighbours)-1)]
        
            #Add current cell to the stack
            self.stack.append((self.x,self.y))
                     
            #Remove the wall between current and chosen cell
            new_x, new_y = newCell
        
            #Cell is above
            if new_x == self.x and (new_y+2) == self.y:
                self.layout[new_x][new_y+1] = FLOOR
            #Cell is below
            elif new_x == self.x and (new_y-2) == self.y:
                self.layout[new_x][new_y-1] = FLOOR
            #Cell is left
            elif (new_x+2) == self.x and new_y == self.y:
                self.layout[new_x+1][new_y] = FLOOR
            #Cell is right
            elif (new_x-2) == self.x and new_y == self.y:
                self.layout[new_x-1][new_y] = FLOOR
            
            self.x = new_x
            self.y = new_y
            
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
        self.x = x
        self.y = y
        self.maze = maze
        self.neighbours = []
        self.stack = []
        
    def solve(self): 
        #Call this to find and make next move
        self.neighbours = []
        self.maze.layout[self.x][self.y] = PATH
        
        #Look for open cells    
        if (self.y-1) >= 0:
            if self.maze.layout[self.x][self.y-1] == FLOOR: #Above
                self.neighbours.append((self.x,self.y-1))
    
        if (self.x-1) >= 0:
            if self.maze.layout[self.x-1][self.y] == FLOOR: #Left
                self.neighbours.append((self.x-1,self.y))
        
        if (self.x < BOARD_WIDTH):
            if self.maze.layout[self.x+1][self.y] == FLOOR: #Right
                self.neighbours.append((self.x+1,self.y))

        if (self.y < BOARD_HEIGHT):
            if self.maze.layout[self.x][self.y+1] == FLOOR: #Down
                self.neighbours.append((self.x,self.y+1))
        
        if self.neighbours: #If we found some neighbours that are open
            newX, newY = self.neighbours[0] #Take the first option
            self.stack.append((self.x,self.y)) #Save old position to stack
            self.x = newX
            self.y = newY
            
        else: #Cell has no open neighbours
            if self.stack:
                #Go back to the previous current cell
                self.x, self.y = self.stack.pop()

        return self.x, self.y

def checkControls(maze): 
    #check player controls (return False if we need to quit)
    pygame.event.pump()    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_ESCAPE]:
        return False
        
    if key[pygame.K_TAB]:
        screen.fill(FLOOR_COLOUR)
        maze.__init__()
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

try:
    newMaze = maze()
    solver = mazeSolver(newMaze)
    run = True 
    solver_x, solver_y = 0, 0
    while run:
        newMaze.draw(*solver.solve())
        run = checkControls(newMaze)
finally:
    pygame.quit()