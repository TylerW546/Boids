import pygame
from pygame.locals import *

from main import *
from TextBox import *

class Point():
   selectRadiusModifier = 1.5

   def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, color=(255,255,255), radius=5):
      self.x = x
      self.y = y
      self.color = color

      self.clicked = False
      
      self.radius = radius
      self.selectRadius = self.radius * Point.selectRadiusModifier
      
      self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)

   def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
         if self.rect.collidepoint(event.pos):
            self.clicked = True
      if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
         self.clicked = False
      if event.type == pygame.MOUSEMOTION and self.clicked == True:
         self.x=event.pos[0]
         self.y=event.pos[1]
         self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)
   
   def draw(self):
      pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
      
class Slider():
   pointColor = (100,200,100)
   lineColor = (255,255,255)
   font = pygame.font.SysFont('Arial', 10)
   
   def __init__(self,x=SCREEN_WIDTH+20,y=230,w=panelWidth-40,h=2,pR=4,pointC=pointColor,lineC=lineColor,min=0,max=1,subdivisions=3):
      self.x = x
      self.y = y
      self.width = w
      self.height = h
      
      self.pointRadius = pR
      self.pointColor = pointC
      self.lineColor = lineC
      
      self.value = .5
      
      self.min = min
      self.max = max
      self.subdivisions = subdivisions
      
      self.point = SliderPoint(self.x+self.width/2,self.y+self.height/2,self.pointColor,self.pointRadius,minX=self.x,maxX=self.x+self.width,minY=self.y+.5*self.height,maxY=self.y+.5*self.height)
   
   def handle_event(self, event):
      self.point.handle_event(event)
   
   def update(self):
      percent = (self.point.x-self.x)/self.width
      self.value = self.min+percent*(self.max-self.min)
   
   def setValue(self,value):
      self.value = value
      self.point.x = self.x + self.width*value
   
   def drawSub(self, percent):
      pygame.draw.rect(screen, self.lineColor, (self.x+percent*self.width,self.y-self.height,self.height,self.height*3), 0)
   
   def textSub(self, percent):
      textLayer = Slider.font.render(str(self.min+percent*(self.max-self.min)), False, (0, 0, 0))
      textCoord = textLayer.get_rect(center = (self.x+percent*self.width,self.y+2*self.height))
      textCoord.y = self.y+5
      screen.blit(textLayer,textCoord)
   
   def draw(self):
      pygame.draw.rect(screen, self.lineColor, (self.x, self.y, self.width, self.height), 0)
      for i in range(0,1001,1000//(self.subdivisions+1)):
         self.drawSub(i/1000)
         self.textSub(i/1000)
      self.point.draw()
      
class SliderPoint(Point):
   def __init__(self,x,y,color,radius,minX=SCREEN_WIDTH,maxX=SCREEN_WIDTH+panelWidth,minY=10,maxY=10):
      super(SliderPoint, self).__init__(x,y,color,radius)
      self.minX = minX
      self.maxX = maxX
      self.minY = minY
      self.maxY = maxY
   
   def handle_event(self, event):
      super(SliderPoint, self).handle_event(event)
      self.x = max(min(self.x, self.maxX), self.minX)
      self.y = max(min(self.y, self.maxY), self.minY)
      self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)
