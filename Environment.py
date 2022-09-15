import pygame
from pygame.locals import *

from main import *

class Environment():
   # Start with lines around the screen
   lines = [[0,0,SCREEN_WIDTH,0,background],[SCREEN_WIDTH,0,SCREEN_WIDTH,SCREEN_HEIGHT,background],[SCREEN_WIDTH,SCREEN_HEIGHT,0,SCREEN_HEIGHT,background],[0,SCREEN_HEIGHT,0,0,background]]
   # If a lines is shorter than minLength, it will be deleted
   minLength = 1
   destroyBoxColor = (255,100,100,100)
   
   boxStart = None
   
   @staticmethod
   def startup():
      Environment.lastMouse = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
   
   @staticmethod
   def update():
      Environment.mouseDraw()
      Environment.draw()
      for line in Environment.lines:
         if distance(line[0], line[1], line[2], line[3]) < Environment.minLength:
            Environment.lines.remove(line)

   @staticmethod
   def mouseDraw():
      mousePos = pygame.mouse.get_pos()
      pressed = pygame.mouse.get_pressed()
      keysPressed = pygame.key.get_pressed()
      
      if mousePos[0] < SCREEN_WIDTH:
         if keysPressed[K_BACKSPACE]:
            if pressed[0]:
               if Environment.boxStart == None:
                  Environment.boxStart = mousePos
               Environment.intermediateDeleteBox(Environment.boxStart,mousePos)
            else:
               if Environment.boxStart != None:
                  Environment.endDeleteBox(Environment.boxStart, mousePos)
                  Environment.boxStart = None
         else:
            if pressed[0]:
               Environment.lines.append([mousePos[0], mousePos[1], Environment.lastMouse[0], Environment.lastMouse[1], (255,0,100)])
   
         Environment.lastMouse[0] = mousePos[0]
         Environment.lastMouse[1] = mousePos[1]
   
   @staticmethod
   def intermediateDeleteBox(start, end):
      topLeft = [min(start[0], end[0]), min(start[1], end[1])]
      width = max(start[0], end[0]) - min(start[0], end[0])
      height = max(start[1], end[1]) - min(start[1], end[1])
      
      pygame.draw.rect(screen, Environment.destroyBoxColor, (topLeft[0], topLeft[1], width, height), 1)
   
   @staticmethod
   def endDeleteBox(start, end):
      topLeft = [min(start[0], end[0]), min(start[1], end[1])]
      width = max(start[0], end[0]) - min(start[0], end[0])
      height = max(start[1], end[1]) - min(start[1], end[1])
      bottomRight = [max(start[0], end[0]), max(start[1], end[1])]
      
      pygame.draw.rect(screen, Environment.destroyBoxColor, (topLeft[0], topLeft[1], width, height), 0)
      index = 0
      while index < len(Environment.lines[4:]):
         line = Environment.lines[4:][index]
         if pointInCube([line[0], line[1]], topLeft, bottomRight):
            Environment.lines.remove(line)
            index -= 1
         elif pointInCube([line[2], line[3]], topLeft, bottomRight):
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
     