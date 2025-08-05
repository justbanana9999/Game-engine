from Engine.Constants import colorLike

import pygame
pygame.font.init()

class Font:
    def __init__(self,path:str,size:int):
        self.name = path
        self.size = size

        if path in pygame.font.get_fonts():
            self.font = pygame.font.SysFont(path,size)
        else:
            self.font = pygame.font.Font(path,size)
    
    def renderText(self,text:str,color:colorLike,bgColor:colorLike|None=None):
        return self.font.render(text,True,color,bgColor)