import pygame

from Engine.Constants import colorLike

from Engine.Vec2 import Vec2

class Image:
    def __init__(self,path:str|pygame.Surface,size:float=1):
        if isinstance(path,pygame.Surface):
            self.image = path
        else:
            self.image = pygame.image.load(path).convert_alpha()

        self.updateSize()

        self.image = pygame.transform.scale(self.image,(self.width*size,self.height*size))

        self.updateSize()

    def updateSize(self):
        self.size = self.image.size
        self.width = self.image.width
        self.height = self.image.height

    @staticmethod
    def rotate(img:'Image|pygame.Surface',angle:float=0,pos:Vec2=Vec2()):
        if isinstance(img,pygame.Surface):
            img = Image(img)
        rotated = pygame.transform.rotate(img.image,-angle)
        rect = rotated.get_rect(center=img.image.get_rect(center=(list(pos))).center)
        return rotated,rect

    @staticmethod
    def fillColor(surf:pygame.Surface,color:colorLike):
        s = pygame.Surface(surf.size,pygame.SRCALPHA)
        s.fill((*color,0)) # type: ignore
        surf.blit(s,special_flags=pygame.BLEND_RGB_MIN)
        surf.blit(s,special_flags=pygame.BLEND_RGBA_ADD)

        return surf

    @staticmethod
    def overlay(surf:pygame.Surface,color:colorLike):
        s = pygame.Surface(surf.size,pygame.SRCALPHA)
        s.fill(color)
        surf.blit(s,special_flags=pygame.BLEND_RGB_MULT)

        return surf