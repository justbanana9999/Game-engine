import pygame

class Tileset:
    def __init__(self,tileSize:int,tilePath:str,scale:int):
        self.tileSize = tileSize
        self.path = tilePath
        self.tileSet = pygame.image.load(self.path).convert_alpha()
        self.scale = scale
        self.images = Tileset.cutImage(self.tileSet,self.tileSize,self.scale)

        self.tileSize = scale
    
    @staticmethod
    def cutImage(img:pygame.Surface,size:int,scale:int):
        tiles:list[pygame.Surface] = []
        
        x,y = 0,0
        while y < img.height:
            while x < img.width:
                tSurf = pygame.Surface.subsurface(img,(x,y,min(size+x,img.width)-x,min(size+y,img.height)-y))

                tSurf = pygame.transform.scale(tSurf,(scale,scale))
                
                tiles.append(tSurf)
                
                x += size
            x = 0
            y += size
        
        return tiles