from copy import copy

try:
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

import pygame

from Engine.Constants import posIntLike,colorLike,circle,posLike,rectLike

from Engine.Image import Image
from Engine.Object import Object
from Engine.Vec2 import Vec2
from Engine.Tileset import Tileset
from Engine.ThreeDim import Object3D,rotate,offset,plot,Cam3D

from math import dist

from Engine.Vec3 import Vec3

class Display:
    def __init__(self,size:posIntLike,fps:int=60):
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        
        self.size = size
        self.width = self.size[0]
        self.height = self.size[0]

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

    def drawTileset(self,tileset:Tileset,tiles:list[list[list[int]]],offset:Vec2):
        pos:tuple[float,float]
        
        xStart = max(0,-int(offset.x)//tileset.tileSize)
        yStart = max(0,-int(offset.y)//tileset.tileSize)

        xEnd = min(len(tiles[0][0]),self.width+int(offset.x)//tileset.tileSize+1)
        yEnd = min(len(tiles[0]),self.width+int(offset.y)//tileset.tileSize+1)
        
        for z in range(len(tiles)):
            # for y in range(len(tiles[0])):
            for y in range(yStart,yEnd):
                # for x in range(len(tiles[0][0])):
                for x in range(xStart,xEnd):
                    pos = (x*tileset.tileSize+offset.x,y*tileset.tileSize+offset.y)

                    idx = tiles[z][y][x]

                    img = tileset.images[idx]

                    self.surface.blit(img,pos)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def circle(self,color:colorLike,pos:posLike,radius:int,width:int=0):
        pygame.draw.circle(self.surface,color,pos,radius,width)
    
    def rect(self,color:colorLike,rect:rectLike,width:int=0,borderRadius:int=-1):
        pygame.draw.rect(self.surface,color,rect,width,borderRadius)
    
    def line(self,color:colorLike,a:posLike,b:posLike,width:int=1):
        pygame.draw.line(self.surface,color,a,b,width)
    
    def lines(self,color:colorLike,closed:bool,points:list[posLike],width:int=1):
        if len(points) >= 2:
            pygame.draw.lines(self.surface,color,closed,points,width)
    
    def draw3D(self,obj:Object3D,cam:Cam3D):

        m = max(self.mid)
        
        polygons = []
        for triangle in obj.triangles:
            avg = [
                (triangle.a.x+triangle.b.x+triangle.c.x)/3,
                (triangle.a.y+triangle.b.y+triangle.c.y)/3,
                (triangle.a.z+triangle.b.z+triangle.c.z)/3,
            ]
            polygons.append([dist(cam.pos,avg),[rotate(point,cam.dir,cam.pos) for point in triangle],triangle.normal])
        
        polygons = sorted(polygons,key=lambda x:-x[0])
                
        normals = [triangle[2] for triangle in polygons]
        
        polygons = [triangle[1] for triangle in polygons]
        
        for i,triangle in enumerate(polygons):
            polygons[i] = ([offset(plot(point,m,cam.zNear,cam.zFar,cam.FOV),self.mid) for point in triangle])
                
        for triangle,normal in zip(polygons,normals):
            if self.mid not in triangle:
                brightness = (Vec3.dot(normal,Vec3(1,2,3).normalized())+1)/2
                pygame.draw.polygon(self.surface,(int(obj.color[0]*brightness),int(obj.color[1]*brightness),int(obj.color[2]*brightness)),triangle)
    
    def getFps(self):
        return self.clock.get_fps()

def checkExit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True