from copy import copy

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

import pygame

from Engine.Constants import *

from Engine.Image import Image
from Engine.Object import Object
from Engine.Vec2 import Vec2
from Engine.Tileset import Tileset

class Display:
    def __init__(self,size:posLike,fps:int=60):
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.mid:tuple[float,float] = (size[0]/2,size[1]/2)
    
    def fill(self,color:colorLike):
        self.surface.fill(color)
    
    def blit(self,surface:Image|pygame.Surface,pos:Vec2=Vec2(),size:float=1,angle:float=0,anchor:str=''):
        img = surface

        if isinstance(img,pygame.Surface):
            img = Image(img)

        s = img.image.size

        img.image = pygame.transform.scale(img.image,(s[0]*size,s[1]*size))

        img,rect = Image.rotate(img,angle,pos)
        
        s = img.size

        if anchor == 'TL':
            rect.topleft = rect.center
        elif anchor == 'TR':
            rect.topright = rect.center
        elif anchor == 'BL':
            rect.bottomleft = rect.center
        elif anchor == 'BR':
            rect.bottomright = rect.center
        
        elif anchor == 'U':
            rect.top = rect.centery
        elif anchor == 'D':
            rect.bottom = rect.centery
        elif anchor == 'L':
            rect.left = rect.centerx
        elif anchor == 'R':
            rect.right = rect.centerx
        
        
        self.surface.blit(img,rect)
    
    def blitObject(self,obj:Object,fillcolor:colorLike|None=None,fillType:str='fill',padding:int=0,paddingColor:colorLike=(0,0,0,0)):
        img = copy(obj.surface)

        s = img.image.size

        img.image = pygame.transform.scale(img.image,(s[0]*obj.size,s[1]*obj.size))

        img,rect = Image.rotate(img,obj.angle,obj.pos)

        s = img.size

        if obj.debug:
            self.rect((255,0,0),rect,1)

        img = pygame.transform.scale(img,(s[0]*obj.squeeze.x,s[1]*obj.squeeze.y))
        
        rect.centerx += s[0]*(1-obj.squeeze.x)/2
        rect.centery += s[1]*(1-obj.squeeze.y)/2
        
        if padding:
            img2 = copy(img)
            img2 = Image.fillColor(img2,paddingColor)
            for x,y in circle:
                self.surface.blit(img2,rect.move(x*padding,y*padding))

        if fillcolor != None:
            if fillType == 'fill':
                img = Image.fillColor(img,fillcolor)
            elif fillType == 'overlay':
                img = Image.overlay(img,fillcolor)  

        self.surface.blit(img,rect)

    def drawTileset(self,tiles:list[list[int]],offset:posIntLike,tileset:Tileset):
        pos:tuple[float,float]
        for y in range(len(tiles)):
            for x in range(len(tiles[0])):
                pos = (x*tileset.tileSize+offset[0],y*tileset.tileSize+offset[1])

                idx = tiles[y][x]

                img = tileset.images[idx]

                self.surface.blit(img,pos)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)
    
    @staticmethod
    def checkExit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def circle(self,color:colorLike,pos:posLike,radius:int,width:int=0):
        pygame.draw.circle(self.surface,color,pos,radius,width)
    
    def rect(self,color:colorLike,rect:rectLike,width:int=0,borderRadius:int=-1):
        pygame.draw.rect(self.surface,color,rect,width,borderRadius)
    
    def line(self,color:colorLike,a:posLike,b:posLike,width:int=1):
        pygame.draw.line(self.surface,color,a,b,width)
    
    def lines(self,color:colorLike,closed:bool,points:list[posLike],width:int=1):
        if len(points) >= 2:
            pygame.draw.lines(self.surface,color,closed,points,width)

    def getFps(self):
        return self.clock.get_fps()