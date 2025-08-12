from Engine.All import *

screen = Display((1600,900),120)

tileset = Tileset(18,'Tiles.png',64)

file = File('save.txt')

tiles = file.load()[0]

print(len(tiles[0][0]),len(tiles[0]),len(tiles))

player = Object(Image('Cat/Cat2.png',0.5),[0,0])

inputs = Input()

while checkExit():
    
    screen.fill((20,20,20))
    
    inputs.updateInputs()
    
    speed = 20 if inputs['LSHIFT'] else 10
    
    if inputs['w']:
        player.pos.y -= speed
    if inputs['s']:
        player.pos.y += speed
    if inputs['a']:
        player.pos.x -= speed
    if inputs['d']:
        player.pos.x += speed
        
    screen.drawTileset(tileset,tiles,-player.pos)
    
    screen.update()