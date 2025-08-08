class Vec2:
    def __init__(self,x:float=0,y:float=0):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return iter([self.x,self.y])
    
    def __neg__(self):
        return Vec2(-self.x,-self.y)