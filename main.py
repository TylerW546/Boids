# -----------------------------------------------------------
# Description: A Bird-oid (Boid) simulation with a settings panel built using pygame.
# Date: September 27, 2021
# Name: Tyler Weed
# -----------------------------------------------------------

import math
import pygame
from pygame.locals import *
import random
import time

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
panelWidth = 300

white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)
background = (30,30,40)

# Pygame initialization
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 15)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + panelWidth, SCREEN_HEIGHT))

from Functions import *

def main():
    from Settings import Settings
    from PositionFormatter import PositionFormatter
    from Environment import Environment
    
    # Starting up classes
    Settings.startup()
    PositionFormatter.startup()
    Environment.startup()
    
    while (True):
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            Settings.handle_event(event)
        
        # Clear screen
        screen.fill(background)
        
        # Update Classes
        PositionFormatter.update() 
        Settings.update()
        Settings.writeInfo()
        Environment.update()

        textsurface = myfont.render("Click and drag to draw lines, hold backspace while dragging to box-delete.", False, (0, 0, 0))
        screen.blit(textsurface,(10, SCREEN_HEIGHT-30))
        
        # Finish Loop
        pygame.display.update()
    
        time.sleep(.025)
        
if __name__ == "__main__":
    main()