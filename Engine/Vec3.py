from math import sqrt,sin,cos,radians

from random import uniform

class Vec3:
    def __init__(self,x:'Vec3|float'=0,y:float=0,z:float=0):
        if isinstance(x,Vec3):
            self.x:float = x.x
            self.y:float = x.y
            self.z:float = x.z
        else:
            self.x = x
            self.y = y
            self.z = z
    
    def __iter__(self):
        return iter([self.x,self.y,self.z])
        
    def __add__(self,other:'Vec3|float'):
        if isinstance(other,Vec3):
            return Vec3(self.x+other.x,self.y+other.y,self.z+other.z)
        return Vec3(self.x+other,self.y+other,self.z+other)
    def __radd__(self,other:float):
        return Vec3(other+self.x,other+self.y,other+self.z)
            
    def __sub__(self,other:'Vec3|float'):
        if isinstance(other,Vec3):
            return Vec3(self.x-other.x,self.y-other.y,self.z-other.z)
        return Vec3(self.x-other,self.y-other,self.z-other)
    def __rsub__(self,other:float):
        return Vec3(other-self.x,other-self.y,other-self.z)
        
    def __mul__(self,other:'Vec3|float'):
        if isinstance(other,Vec3):
            return Vec3(self.x*other.x,self.y*other.y,self.z*other.z)
        return Vec3(self.x*other,self.y*other,self.z*other)
    def __rmul__(self,other:float):
        return Vec3(other*self.x,other*self.y,other*self.z)
    
    def __truediv__(self,other:'Vec3|float'):
        if isinstance(other,Vec3):
            return Vec3(self.x/other.x,self.y/other.y,self.z/other.z)
        return Vec3(self.x/other,self.y/other,self.z/other)
    def __rtruediv__(self,other:float):
        return Vec3(other/self.x,other/self.y,other/self.z)
        
    def __floordiv__(self,other:'Vec3|float'):
        if isinstance(other,Vec3):
            return Vec3(self.x//other.x,self.y//other.y,self.z//other.z)
        return Vec3(self.x//other,self.y//other,self.z//other)
    def __rfloordiv__(self,other:float):
        return Vec3(other//self.x,other//self.y,other//self.z)
    
    def __pow__(self,other:float):
        return Vec3(self.x**other,self.y**other,self.z**other)
    
    def __str__(self):
        return f'Vec3({self.x} {self.y} {self.z})'
    
    def length(self):
        return sqrt(self.lengthSquared())
    
    def lengthSquared(self):
        return Vec3.dot(self,self)
    
    def normalized(self):
        return self/self.length()

    @staticmethod
    def dot(a:'Vec3',b:'Vec3'):
        return a.x*b.x+a.y*b.y+a.z*b.z
    
    @staticmethod
    def matrixMul(a:'Vec3',b:list[list]):
        x = b[0][0]*a.x+b[0][1]*a.y+b[0][2]*a.z
        y = b[1][0]*a.x+b[1][1]*a.y+b[1][2]*a.z
        z = b[2][0]*a.x+b[2][1]*a.y+b[2][2]*a.z
        return Vec3(x,y,z)
    
    @staticmethod
    def rotate(point:'Vec3',angle:'Vec3'):
        aX,aY,aZ = Vec3(radians(angle.x),radians(angle.y),radians(angle.z))
        
        x = [[1,0,0],
             [0,cos(aX),sin(aX)],
             [0,-sin(aX),cos(aX)]]
        y = [[cos(aY),0,-sin(aY)],
             [0,1,0],
             [sin(aY),0,cos(aY)]]
        z = [[cos(aZ),sin(aZ),0],
             [-sin(aZ),cos(aZ),0],
             [0,0,1]]
        
        return Vec3.matrixMul(Vec3.matrixMul(Vec3.matrixMul(point,z),y),x)