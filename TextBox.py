import pygame
from pygame.locals import *

from main import *

class Text:
   font = pygame.font.SysFont('Arial', 10)
   
   def __init__(self, x = SCREEN_WIDTH + 164, y = 20, w = 40, h = 20, color = (0,0,0), text = "Null", font=font):
      self.x = x
      self.y = y
      self.width = w
      self.height = h
      self.color = color
      self.text = text
      
      self.font=font
      
      self.textSurface = font.render(self.text, True, self.color)
      self.textCoord = self.textSurface.get_rect(center = (self.x+self.width/2+2, self.y + self.height/2))
   
   def draw(self):
      pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 1)
      screen.blit(self.textSurface,self.textCoord)

class TextBox(Text):
   font = pygame.font.SysFont('Arial', 15)
   COLOR_INACTIVE = (200,200,200)
   COLOR_ACTIVE = (100,200,100)

   def __init__(self, x=SCREEN_WIDTH+210, y=20, w=80, h=20, color=COLOR_INACTIVE, text=""):
      super(TextBox, self).__init__(x,y,w,h,color,text,font=TextBox.font)      
      self.rect = pygame.Rect(x, y, w, h)
      self.active = False

   def isMax(self):
      if self.textSurface.get_width() >= self.width-12:
         return True
      return False
   
   def handleEvent(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
         if self.rect.collidepoint(event.pos):
            self.active = not self.active
         else:
            self.active = False
         self.color = TextBox.COLOR_ACTIVE if self.active else TextBox.COLOR_INACTIVE
         self.textSurface = self.font.render(self.text, True, self.color)
      if event.type == pygame.KEYDOWN:
         if self.active:
            if event.key == pygame.K_RETURN:
               self.active = False
               self.color = TextBox.COLOR_INACTIVE
            elif event.key == pygame.K_BACKSPACE:
               self.text = ""
            else:
               self.text += event.unicode
               if self.isMax():
                  self.text = self.text[:-1]
            self.textSurface = self.font.render(self.text, True, self.color)

   def draw(self):
      screen.blit(self.textSurface, (self.x+4,self.y+1))
      pygame.draw.rect(screen, self.color, self.rect, 2)
