import pygame
from pygame.locals import *

from main import *

class Text:
   """Simple class that stores information needed for a pygame text object"""
   font = pygame.font.SysFont('Arial', 10)
   
   def __init__(self, x = SCREEN_WIDTH + 164, y = 20, w = 40, h = 20, color = (0,0,0), text = "Null", font=font):
      self.x = x
      self.y = y
      self.width = w
      self.height = h
      self.color = color
      self.text = text
      self.remember_text = text
      
      self.font=font
      
      self.textSurface = font.render(self.text, True, self.color)
      self.textCoord = self.textSurface.get_rect(center = (self.x+self.width/2+2, self.y + self.height/2))
   
   def draw(self):
      pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 1)
      screen.blit(self.textSurface, self.textCoord)

class TextBox(Text):
   font = pygame.font.SysFont('Arial', 15)
   COLOR_INACTIVE = (200,200,200)
   COLOR_ACTIVE = (100,200,100)

   def __init__(self, x=SCREEN_WIDTH+210, y=20, w=80, h=20, color=COLOR_INACTIVE, text=""):
      super(TextBox, self).__init__(x,y,w,h,color,text,font=TextBox.font)      
      self.rect = pygame.Rect(x, y, w, h)
      self.active = False

   def isMax(self):
      """Returns whether text width is greater than the box's width"""
      if self.textSurface.get_width() >= self.width-12:
         return True
      return False
   
   def handleEvent(self, event):
      """Handles events such as mouse clicks and text inputs"""
      if event.type == pygame.MOUSEBUTTONDOWN: # If user clicks anywhere
         if self.rect.collidepoint(event.pos): # If user clicks on this object
            # Flip active status. If active, should no longer be active, if not active, should be
            self.active = not self.active
            # Back up the current text, in case the user clicks off without entering a value
            self.remember_text = self.text
            # Clear text to give an open input area
            self.text = ""
         else: # Clicked, but not on the text box. Clears active status and reinstates remembered text if text is blank
            self.active = False
            if self.text == "":
               self.text = self.remember_text
         # Get correct color
         self.color = TextBox.COLOR_ACTIVE if self.active else TextBox.COLOR_INACTIVE
         # Render surface
         self.textSurface = self.font.render(self.text, True, self.color)
      if event.type == pygame.KEYDOWN: # Key pressed
         if self.active: # Will only affect this box if box is active, so check for that
            if event.key == pygame.K_RETURN: # Enter key is treated as a click off, deselects the textbox
               self.active = False
               self.color = TextBox.COLOR_INACTIVE
               if self.text == "":
                  self.text = self.remember_text 
            elif event.key == pygame.K_BACKSPACE: # Backspace removes the last character
               if self.text:
                  self.text = self.text[:-1]
            else: # Any other character should be typed in to the box, error won't be thrown for special characters, it just won't change anything other than graphically
               self.text += event.unicode
               if self.isMax():
                  self.text = self.text[:-1]
            self.textSurface = self.font.render(self.text, True, self.color) # Render text surface

   def draw(self):
      """Draws the box"""
      screen.blit(self.textSurface, (self.x+4,self.y+1))
      pygame.draw.rect(screen, self.color, self.rect, 2)
