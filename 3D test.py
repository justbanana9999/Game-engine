from Engine.All import *

screen = Display((1600,900),60)

obj = Object3D('Objects/Banana.obj',color=(255,255,0))

camera = Cam3D(Vec3(0,0,0),Vec3(0,0,3),0.05,10,90)

inputs = Input()

inputs.setMouseVisibility(False)

while screen.checkExit():

    screen.fill((20,20,20))
    
    inputs.updateInputs()
    
    inputs.setMousePos(screen.mid)
    
    speed = 0.2 if inputs['LSHIFT'] else 0.1
    
    if inputs['d']:
        camera.pos += moveR(camera.dir,speed)
    if inputs['a']:
        camera.pos -= moveR(camera.dir,speed)
    
    if inputs['w']:
        camera.pos += moveF2(camera.dir,speed)
    if inputs['s']:
        camera.pos -= moveF2(camera.dir,speed)
    
    if inputs['SPACE']:
        camera.pos.y -= speed
    if inputs['LCTRL']:
        camera.pos.y += speed
    
    if inputs['LEFT']:
        camera.dir.y += 5
    if inputs['RIGHT']:
        camera.dir.y -= 5
    
    if inputs['UP']:
        camera.dir.x += 5
    if inputs['DOWN']:
        camera.dir.x -= 5
    
    camera.dir.y += (screen.mid[0]-inputs.mousePos[0])/10
    camera.dir.x += (screen.mid[1]-inputs.mousePos[1])/10
    
    camera.dir.y %= 360
    camera.dir.x = min(max(camera.dir.x,-90),90)
    
    inputs.setMousePos(screen.mid)
    
    screen.draw3D(obj,camera)
    
    if inputs['ESCAPE']:
        break
    
    screen.update()