import pygame
from pygame.locals import *

from main import *

# A surplus of lines can make the program very laggy.

class Environment():
   """Environment stores and creates lines in the viewing window"""
   # Start with lines around the screen
   lines = [[0,0,SCREEN_WIDTH,0,background],[SCREEN_WIDTH,0,SCREEN_WIDTH,SCREEN_HEIGHT,background],[SCREEN_WIDTH,SCREEN_HEIGHT,0,SCREEN_HEIGHT,background],[0,SCREEN_HEIGHT,0,0,background]]
   # If a lines is shorter than minLength, it will be deleted
   minLength = 1
   destroyBoxColor = (255,100,100,100)
   
   # Will be a set of coordinates defining the start point of a box select if use is in the proccess of box selecting, otherwise is set to None 
   boxStart = None
   
   @staticmethod
   def startup():
      Environment.lastMouse = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
   
   @staticmethod
   def update():
      # Takes in mouse input to add/remove lines to the list
      Environment.mouseDraw()
      # Draws the lines on the screen
      Environment.draw()
      # Deletes lines that are too short to keep lag low(er)
      for line in Environment.lines:
         if distance(line[0], line[1], line[2], line[3]) < Environment.minLength:
            Environment.lines.remove(line)

   @staticmethod
   def mouseDraw():
      """Adds new lines based on mouse input"""
      mousePos = pygame.mouse.get_pos() # returns [x,y] of current mouse position
      pressed = pygame.mouse.get_pressed() # returns list of pressed mouse keys
      keysPressed = pygame.key.get_pressed() # returns list of pressed keyboard keys
      
      if mousePos[0] < SCREEN_WIDTH: # Checks to make sure mouse is not in the Settings panel
         if keysPressed[K_BACKSPACE]: # Deleting lines
            if pressed[0]: # If left clicking
               if Environment.boxStart == None: # If this is the first frame of deletion
                  Environment.boxStart = mousePos # set this position as the start for the box selection
               Environment.intermediateDeleteBox(Environment.boxStart,mousePos) # Render the current box selection
            else: # Left mouse is not clicked
               if Environment.boxStart != None: # If the box has been started, it means user has just let go of the mouse
                  Environment.endDeleteBox(Environment.boxStart, mousePos) # Run the delete method within the box selection
                  Environment.boxStart = None # No longer box selecting, clear boxStart variable
         else: # Drawing lines
            # If mouse is pressed, create new line
            if pressed[0]:
               Environment.lines.append([mousePos[0], mousePos[1], Environment.lastMouse[0], Environment.lastMouse[1], (255,0,100)])
   
         Environment.lastMouse[0] = mousePos[0]
         Environment.lastMouse[1] = mousePos[1]
   
   @staticmethod
   def intermediateDeleteBox(start, end):
      """Renders an outline of the box select before it is complete"""
      topLeft = [min(start[0], end[0]), min(start[1], end[1])]
      width = max(start[0], end[0]) - min(start[0], end[0])
      height = max(start[1], end[1]) - min(start[1], end[1])
      
      pygame.draw.rect(screen, Environment.destroyBoxColor, (topLeft[0], topLeft[1], width, height), 1)
   
   @staticmethod
   def endDeleteBox(start, end):
      """Renders a solid box over the final box select, delete any lines with points within the selection"""
      topLeft = [min(start[0], end[0]), min(start[1], end[1])]
      width = max(start[0], end[0]) - min(start[0], end[0])
      height = max(start[1], end[1]) - min(start[1], end[1])
      bottomRight = [max(start[0], end[0]), max(start[1], end[1])]
      
      pygame.draw.rect(screen, Environment.destroyBoxColor, (topLeft[0], topLeft[1], width, height), 0)
      
      # Checks 
      index = 0
      while index < len(Environment.lines[4:]): # Starts at 4 as the first 4 lines are the permanent outlines of the screen
         line = Environment.lines[4:][index]
         if pointInSquare([line[0], line[1]], topLeft, bottomRight): # If the first point of the line is in the box select, delete it
            Environment.lines.remove(line)
            index -= 1
         elif pointInSquare([line[2], line[3]], topLeft, bottomRight):# If the second point of the line is in the box select, delete it
            Environment.lines.remove(line)
            index -= 1
         index += 1
         
   @staticmethod
   def draw():
      for line in Environment.lines:
         pygame.draw.lines(screen, line[4], False, [(line[0], line[1]), (line[2], line[3])], 1)
         
         #textsurface = myfont.render("(" + str(int(line[0])) + ", " + str(int(line[1])) + ")", False, (0, 0, 0))
         #screen.blit(textsurface,(int(line[0]), int(line[1])))
         
         #textsurface = myfont.render("(" + str(int(line[2])) + ", " + str(int(line[3])) + ")", False, (0, 0, 0))
         #screen.blit(textsurface,(int(line[2]), int(line[3])))
     