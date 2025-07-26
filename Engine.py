import ctypes
ctypes.windll.user32.SetProcessDPIAware()

from copy import copy

import pygame

from pygame import mixer
mixer.init()

pygame.font.init()

colorLike = pygame.typing.ColorLike
posLike = pygame.typing.Point
rectLike = pygame.typing.RectLike

class vec2:
    def __init__(self,x:float=0,y:float=0):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return iter([self.x,self.y])

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
    def rotate(img:'Image|pygame.Surface',angle:float=0,pos:vec2=vec2()):
        if isinstance(img,pygame.Surface):
            img = Image(img)
        rotated = pygame.transform.rotate(img.image,-angle)
        rect = rotated.get_rect(center=img.image.get_rect(center=(list(pos))).center)
        return rotated,rect

class Object:
    def __init__(self,img:Image,pos:posLike=[0,0],size:float=1,angle:float=0,vel:posLike=[0,0],squeeze:posLike|vec2=(1,1)):
        self.surface = img
        self.pos = vec2(*pos)
        self.size = size
        self.angle = angle
        self.vel = vec2(*vel)

        self.squeeze = vec2(*squeeze)
    
        self.debug:bool = False

    def useVel(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

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

class Display:
    def __init__(self,size:posLike,fps:int=60):
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.mid:tuple[float,float] = (size[0]/2,size[1]/2)
    
    def fill(self,color:colorLike):
        self.surface.fill(color)
    
    def blit(self,surface:Image|pygame.Surface,pos:vec2=vec2(),size:float=1,angle:float=0,anchor:str=''):
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
    
    def blitObject(self,obj:Object):
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
        
        self.surface.blit(img,rect)

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

class Input:
    def __init__(self):
        self.alphabet = 'q e r t y u i o p a s d f g h j k l z x c v b n m ' \
        '1 2 3 4 5 6 7 8 9 0 ' \
        'SPACE LSHIFT RSHIFT LCTRL RCTRL LALT RALT ' \
        'PERIOD COMMA SLASH BACKSLASH TAB ESCAPE SPACE ' \
        'UP DOWN LEFT RIGHT ' \
        'F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 ' \
        'PAGEUP PAGEDOWN'.split()

        self.keys:dict[str,bool] = {}
        self.mousePos:tuple[int,int] = (0,0)
        self.mouseInput:tuple[bool,bool,bool] = (False,False,False)

        self.pressed = False
        self.clicked = False

    def __getitem__(self,key:str|int):
        if type(key) == str:
            return self.keys[key]
        elif type(key) == int:
            return self.mouseInput[key]

    def updateInputs(self):
        key = pygame.key.get_pressed() # type: ignore
        for character in self.alphabet:
            self.keys[character] = eval(f'key[pygame.K_{character}]')
        
        self.mousePos = pygame.mouse.get_pos()
        self.mouseInput = pygame.mouse.get_pressed()
    
    def updatePressed(self,keys:list[str]=[]):
        if keys:
            self.pressed = any([self.keys[k] for k in keys])
        else:
            self.pressed = any(self.keys)
    
    def updateClicked(self):
        self.clicked = any(self.mouseInput)

class Sound:
    def __init__(self,path:str,volume:float=1):
        self.sound = mixer.Sound(path)
        self.volume = volume
    
    def play(self,volume:float=-1):
        if volume == -1:
            volume = self.volume
        self.sound.set_volume(volume)
        self.sound.play()
    
    def stop(self):
        self.sound.stop()

    def fadeout(self,seconds:float):
        self.sound.fadeout(int(seconds*1000))