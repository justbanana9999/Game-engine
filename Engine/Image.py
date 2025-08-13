import pygame

from Engine.Constants import colorLike,rectLike

from Engine.Vec2 import Vec2

class Image:
    def __init__(self,path:str|pygame.Surface,size:float=1):
        if isinstance(path,pygame.Surface):
            self.surface = path
        else:
            self.surface = pygame.image.load(path).convert_alpha()

        self.updateSize()

        self.surface = pygame.transform.scale(self.surface,(self.width*size,self.height*size))

        self.updateSize()

    def updateSize(self):
        self.size = self.surface.size
        self.width = self.surface.width
        self.height = self.surface.height

    @staticmethod
    def rotate(img:'Image|pygame.Surface',angle:float=0,pos:Vec2=Vec2()):
        if isinstance(img,pygame.Surface):
            img = Image(img)
        rotated = pygame.transform.rotate(img.surface,-angle)
        rect = rotated.get_rect(center=img.surface.get_rect(center=(list(pos))).center)
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
    
    @staticmethod
    def aaBorder(surf:pygame.Surface,rect:rectLike,radius:int):
        pygame.draw.rect(surf,(255,255,255),(rect[0]+radius,rect[1],rect[2]-2*radius,rect[3]))
        pygame.draw.rect(surf,(255,255,255),(rect[0],rect[1]+radius,rect[2],rect[3]-2*radius))
        pygame.draw.aacircle(surf,(255,255,255),(rect[0]+radius,rect[1]+radius),radius)
        pygame.draw.aacircle(surf,(255,255,255),(rect[0]+rect[2]-radius,rect[1]+radius),radius)
        pygame.draw.aacircle(surf,(255,255,255),(rect[0]+radius,rect[1]+rect[3]-radius),radius)
        pygame.draw.aacircle(surf,(255,255,255),(rect[0]+rect[2]-radius,rect[1]+rect[3]-radius),radius)

    @staticmethod
    def roundedBorders(img:'Image',radius:int,antiAliasing:bool=True):
        surf = img.surface
        mask = pygame.Surface(img.size,pygame.SRCALPHA)
        if antiAliasing:
            Image.aaBorder(mask,list(mask.get_rect()),radius)
        else:
            pygame.draw.rect(mask,(255,255,255),mask.get_rect(),border_radius=radius)
        rounded = surf.copy()
        rounded.blit(mask,special_flags=pygame.BLEND_RGBA_MULT)
        img.surface = rounded
        return img