import pygame
from pygame.locals import *

from main import *
from Buttons import *
from TextBox import *
from Boid import Boid

class Settings():
   backgroundColor = (100,100,200)
   panelWidth = panelWidth
   
   
   entitySight = True
   objectSight = True
   centerOfMass = True
   velocities = True
   neighbors = True
   highlightMainBoid = True
   linePoints = True
   subdivLinePoints = True
   seenPoints = True
   
   buttons = []
   texts = []
   textBoxes = []
   
   @staticmethod
   def startup():
      # Set up buttons
      Settings.buttons.append(ToggleButton(y = 20, text="Highlight Boid 0", initialValue=True))
      Settings.buttons.append(ToggleButton(y = 50, text="Entity Sight", initialValue=True))
      Settings.buttons.append(ToggleButton(y = 80, text="Object Sight", initialValue=True))
      Settings.buttons.append(ToggleButton(y = 110, text="Center of Mass"))
      Settings.buttons.append(ToggleButton(y = 140, text="Velocities", initialValue=True))
      Settings.buttons.append(ToggleButton(y = 170, text="Neighbors", initialValue=True))
      Settings.buttons.append(ToggleButton(y = 200, text="Line Points"))
      Settings.buttons.append(ToggleButton(y = 230, text="Sub-Line Points"))
      Settings.buttons.append(ToggleButton(y = 260, text="Seen Points", initialValue=True))
      
      # Set up "Radius:" static texts
      Settings.texts.append(Text(y=20, text="Radius: "))
      Settings.texts.append(Text(y=50, text="Radius: "))
      Settings.texts.append(Text(y=80, text="Radius: "))
      Settings.texts.append(Text(y=110, text="Radius: "))
      Settings.texts.append(Text(y=140, text="Length: "))
      Settings.texts.append(Text(y=170, text="Radius: "))
      Settings.texts.append(Text(y=200, text="Radius: "))
      Settings.texts.append(Text(y=230, text="Radius: "))
      Settings.texts.append(Text(y=260, text="Radius: "))
      
      # Set up clickable textBoxes
      Settings.textBoxes.append(TextBox(y = 20, text=str(Boid.mainSize)))
      Settings.textBoxes.append(TextBox(y = 50, text=str(Boid.objectSightRadius)))
      Settings.textBoxes.append(TextBox(y = 80, text=str(Boid.sightRadius)))
      Settings.textBoxes.append(TextBox(y = 110, text=str(Boid.centerOfMassSize)))
      Settings.textBoxes.append(TextBox(y = 140, text=str(Boid.drawModifier)))
      Settings.textBoxes.append(TextBox(y = 170, text=str(Boid.neighborSize)))
      Settings.textBoxes.append(TextBox(y = 200, text=str(Boid.mainPointSize)))
      Settings.textBoxes.append(TextBox(y = 230, text=str(Boid.subdivideSize)))
      Settings.textBoxes.append(TextBox(y = 260, text=str(Boid.pointHighlightSize)))
   
   @staticmethod
   def handle_event(event):
      """Sends events to every button and clickable text box"""
      for button in Settings.buttons:
         button.handle_event(event)
      for box in Settings.textBoxes:
         box.handleEvent(event)
   
   @staticmethod
   def update():
      """Updates and draws and sets variables based on the user inputs."""
      pygame.draw.rect(screen, Settings.backgroundColor, (SCREEN_WIDTH, 0, Settings.panelWidth, SCREEN_HEIGHT), 0)
      
      mousePos = pygame.mouse.get_pos()
      pressed = pygame.mouse.get_pressed()[0]
      
      for button in Settings.buttons:
         button.update()
         button.draw()
      
      for box in Settings.textBoxes:
         box.draw()
      
      for text in Settings.texts:
         text.draw()
      
      Settings.highlightMainBoid = Settings.buttons[0].on
      Settings.entitySight = Settings.buttons[1].on
      Settings.objectSight = Settings.buttons[2].on
      Settings.centerOfMass = Settings.buttons[3].on
      Settings.velocities = Settings.buttons[4].on
      Settings.neighbors = Settings.buttons[5].on
      Settings.linePoints = Settings.buttons[6].on
      Settings.subdivLinePoints = Settings.buttons[7].on
      Settings.seenPoints = Settings.buttons[8].on
   
   @staticmethod
   def writeInfo():
      # try try again...
      # Any error should be ignored, they should not effect the program. Text should stay without breaking anything. 
      # This assumes the user will usually not type text, and will notice if they do, as I don't want to create an error message text are. 
      # This would decrease ability to create more settings down the line as it would take up space.
      # This transfer of variables from Settings to Boid does two things: it makes it easy to reference the booleans from Boid, and by creating a new variable, it is easier to ignore when the textBox.text contains non-numerical characters
      try:
         Boid.mainSize = int(Settings.textBoxes[0].text)
      except:
         pass
      try:
         Boid.sightRadius = int(Settings.textBoxes[1].text)
      except:
         pass
      try:
         Boid.objectSightRadius = int(Settings.textBoxes[2].text)
      except:
         pass
      try:
         Boid.centerOfMassSize = int(Settings.textBoxes[3].text)
      except:
         pass
      try:
         Boid.drawModifier = int(Settings.textBoxes[4].text)
      except:
         pass
      try:
         Boid.neighborSize = int(Settings.textBoxes[5].text)
      except:
         pass
      try:
         Boid.mainPointSize = int(Settings.textBoxes[6].text)
      except:
         pass
      try:
         Boid.subdivideSize = int(Settings.textBoxes[7].text)
      except:
         pass
      try:
         Boid.pointHighlightSize = int(Settings.textBoxes[8].text)
      except:
         pass

      # Set booleans
      Boid.entitySight = Settings.entitySight
      Boid.objectSight = Settings.objectSight
      Boid.centerOfMass = Settings.centerOfMass
      Boid.velocities = Settings.velocities
      Boid.neighbors = Settings.neighbors
      Boid.highlightMainBoid = Settings.highlightMainBoid
      Boid.linePoints = Settings.linePoints
      Boid.subdivLinePoints = Settings.subdivLinePoints
      Boid.seenPoints = Settings.seenPoints