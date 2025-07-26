from Engine import Display,Image,Object,Input,Sound,Font

screen = Display((800,800),60)

cat = Object(Image('Cat2.png',0.2),[400,400])

cat.squeeze.x = 2

a = 0

inputs = Input()

song = Sound('meow.mp3',0.5)

song.play()

meow = Sound('Cat meow sound effect.mp3',0.5)

arr:list[list[float]] = []

frame = 0

font = Font('consolas',20)

while Display.checkExit():
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
        cat.vel.y = -30
    
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
        arr.append(list(cat.pos))

    if len(arr) > 20:
        del arr[0]

    screen.lines((0,255,0),False,arr) # type: ignore

    for i,pos in enumerate(arr):
        tObj = Object(cat.surface,pos,cat.size-(20-i)/20,cat.angle,squeeze=cat.squeeze)
        screen.blitObject(tObj)

    screen.blitObject(cat)

    cat.angle += 2

    screen.blit(font.renderText(f'{screen.getFps()}',(100,100,255)),anchor='TL')

    screen.update()