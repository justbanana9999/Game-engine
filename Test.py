from Engine.All import *

screen = Display((800,800),60)

cat = Object(Image('Cat/Cat2.png',0.2),[400,400])

inputs = Input()

song = Sound('Cat/meow.mp3',0.1)

song.play()

meow = Sound('Cat/Cat meow sound effect.mp3',0.5)

arr:list[posLike] = []

frame = 0
offset = 0

font = Font('consolas',20)

while checkExit():
    screen.fill((20,20,20))

    cat.vel.y += 1

    cat.useVel()

    inputs.updateInputs()

    if inputs['SPACE'] and not inputs.pressed:
        meow.play()

    if inputs[2] and not inputs.clicked:
        song.fadeout(2)
    
    if inputs['LEFT'] or inputs['a']:
        cat.vel.x -= 1
    
    if inputs['RIGHT'] or inputs['d']:
        cat.vel.x += 1
    
    cat.vel.x *= 0.95

    if cat.pos.y >= 800:
        cat.pos.y = 800
        cat.vel.y = -35

    if cat.pos.y >= 700 and cat.vel.y < 0:

        cat.squeeze.x = 1.2
        cat.squeeze.y = 0.5
    else:
        cat.squeeze.x = 1/(abs(cat.vel.y)/100+1)
        cat.squeeze.y = abs(cat.vel.y)/50+1
    
    if cat.pos.x <= 0:
        cat.pos.x = 0
        cat.vel.x = abs(cat.vel.x)
    
    if cat.pos.x >= 800:
        cat.pos.x = 800
        cat.vel.x = -abs(cat.vel.x)

    inputs.updateClicked()
    inputs.updatePressed(['SPACE'])
    
    frame += 1
    if frame >= 2:
        frame = 0
        offset += 1
        offset %= 4
        arr.append(list(cat.pos))

        if len(arr) > 20:
            del arr[0]
    
    screen.lines((0,255,0),False,arr)

    s = 0
    for i,pos in enumerate(arr):
        s += cat.size/len(arr)
        tObj = Object(cat.surface,pos,s,cat.angle)
        screen.blitObject(tObj,(0,0,255) if (i+offset)%2 == 0 else None,'overlay' if (i+offset)%4 == 0 else 'fill')

    screen.blitObject(cat,padding=5,paddingColor=(255,255,0))

    cat.angle += 2

    screen.circle((0,255,0),inputs.mousePos,10)

    screen.blit(font.renderText(f'{screen.getFps():.2f}',(100,100,255)),anchor='TL')

    screen.update()