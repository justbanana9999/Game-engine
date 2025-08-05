from Engine.Image import Image
from Engine.Vec2 import Vec2

from Engine.Constants import posLike

class Object:
    def __init__(self,img:Image,pos:posLike=[0,0],size:float=1,angle:float=0,vel:posLike=[0,0],squeeze:posLike|Vec2=(1,1)):
        self.surface = img
        self.pos = Vec2(*pos)
        self.size = size
        self.angle = angle
        self.vel = Vec2(*vel)

        self.squeeze = Vec2(*squeeze)
    
        self.debug:bool = False

    def useVel(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y