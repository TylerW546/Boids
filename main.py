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

pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 20)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + panelWidth, SCREEN_HEIGHT))

from Functions import *

def main():
    from Settings import Settings
    from PositionFormatter import PositionFormatter
    from Environment import Environment
    
    Settings.startup()
    PositionFormatter.startup()
    Environment.startup()
    
    while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            Settings.handle_event(event)
                
        screen.fill(background)
        
        PositionFormatter.update() 
        Settings.update()
        Settings.writeInfo()
        Environment.update()
        
        pygame.display.update()
    
        time.sleep(.025)
        
if __name__ == "__main__":
    main()