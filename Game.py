
import pygame

screen = pygame.display.set_mode((1200,700))
clock = pygame.time.Clock()

screen_size = screen.get_size()

def checkExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            pygame.quit()
            exit()

def save():
    pass
    # try:
    #     with open('save','w') as file:
    #         file.write('global tiles\n')
    #         file.write(f'{tiles = }\n')
    # except:
    #     print('save error')

def load():
    try:
        with open('save','r') as file:
            exec(file.read())
    except:
        print('load error')

#initialize
tile_res = [100,40]
tile_size = 72

player_size = [60,60]

tiles = [[0 for i in range(tile_res[0])] for i in range(tile_res[1])]

tile_sprites = load_sprites('tiles',(tile_size,tile_size))

background_sprites = load_sprites('backgrounds',8)

character_sprites = load_sprites('characters',player_size)

player_pos = [0,0]
player_vel = [0,0]

camera_pos = [0,0]

frame = 0

speed = 10

player_vel = [0,0]

load()

check_tiles = [[-1,-1],[0,-1],[1,-1],
               [-1,0],[0,0],[1,0],
               [-1,1],[0,1],[1,1]]

while True:
    checkExit()
    
    screen.fill((0,0,0))
    
    frame += 1
    
    frame %= 60

    key = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    if key[pygame.K_ESCAPE]:
        save()
        pygame.quit()
        exit()
    
    if key[pygame.K_LSHIFT]:
        speed = 1.5
    else:
        speed = 1
    
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]
    
    percentage = [(player_pos[0]/tile_size)%1,(player_pos[1]/tile_size)%1]
    
    distance_top = (player_pos[1]-player_size[1]/2)%tile_size/tile_size
    distance_bottom = (-(player_pos[1]+player_size[1]/2))%tile_size/tile_size
    
    distance_left = (player_pos[0]-player_size[0]/2)%tile_size/tile_size
    distance_right = (-(player_pos[0]+player_size[0]/2))%tile_size/tile_size
            
    player_tiles = [[int(round((player_pos[0]+i[0]*player_size[0]/2-tile_size/2)/tile_size)),int(round((player_pos[1]+i[1]*player_size[1]/2-tile_size/2)/tile_size))] for i in check_tiles]
    
    solid = [tiles[1][i[1]][i[0]] != 0 for i in player_tiles]
    
    semi = [tiles[3][i[1]][i[0]] != 0 for i in player_tiles]
    
    climb = [tiles[2][i[1]][i[0]] != 0 for i in player_tiles]

    if climb[4]:
        player_vel[0] *= 0.9
        player_vel[1] *= 0.9
    else:
        player_vel[1] += 0.3
        player_vel[0] *= 0.95
        player_vel[1] *= 0.99

    #top
    if solid[1]:
        if player_vel[1] < 0:
            player_vel[1] = 0
            player_pos[1] = round(player_pos[1]/tile_size)*tile_size+player_size[1]/2
    
    if distance_top > 0.9:
        if solid[0] or solid[2]:
            if not (solid[3] or solid[5]):
                if (distance_left > 0.01 and distance_right > 0.01):
                    if player_vel[1] < 0:
                        player_vel[1] = 0
                        player_pos[1] = round(player_pos[1]/tile_size)*tile_size+player_size[1]/2
    
    touch_ground = False
    #bottom
    if solid[7] or (semi[7] and (distance_bottom < 0.1 or distance_bottom > 0.9)):
        if player_vel[1] > 0:
            player_vel[1] = 0
            player_pos[1] = round(player_pos[1]/tile_size)*tile_size-player_size[1]/2

            touch_ground = True
    
    if distance_bottom > 0.9:
        if (solid[6]) or (solid[8]) or ((semi[6] or semi[8]) and (distance_bottom < 0.1 or distance_bottom > 0.9)):
            if not (solid[3] or solid[5]):
                if (0.9 > distance_left > 0.01 and 0.9 > distance_right > 0.01):
                        if player_vel[1] > 0:
                            player_vel[1] = 0
                            player_pos[1] = round(player_pos[1]/tile_size)*tile_size-player_size[1]/2
    
                            touch_ground = True
    
    #left
    if solid[3]:
        player_vel[0] = 0
        player_pos[0] = round(player_pos[0]/tile_size)*tile_size+player_size[0]/2
    
    if distance_left < 0.1 or distance_left > 0.9:
        if solid[0] or solid[6]:
            if not (solid[1] or solid[7]):
                if player_vel[0] < 0:
                    player_vel[0] = 0
                    player_pos[0] = round(player_pos[0]/tile_size)*tile_size+player_size[0]/2
    #right
    if solid[5]:
        player_vel[0] = 0
        player_pos[0] = round(player_pos[0]/tile_size)*tile_size-player_size[0]/2

    if distance_right < 0.1 or distance_right > 0.9:
        if solid[2] or solid[8]:
            if not (solid[1] or solid[7]):
                if player_vel[0] > 0:
                    player_vel[0] = 0
                    player_pos[0] = round(player_pos[0]/tile_size)*tile_size-player_size[0]/2
    
    if key[pygame.K_w]:
        if climb[4]:
            player_vel[1] -= speed
        # elif any(solid[6:9]) or semi[7]:
        elif touch_ground:
            player_vel[1] = -9
    elif key[pygame.K_s]:
        player_vel[1] += speed
    if key[pygame.K_a]:
        player_vel[0] -= speed
    elif key[pygame.K_d]:
        player_vel[0] += speed
    
    camera_pos = [player_pos[0]-screen_size[0]/2+player_size[0]/2,player_pos[1]-screen_size[1]/2+player_size[1]/2]
    
    camera_pos = [int(camera_pos[0]),int(camera_pos[1])]
    
    camera_pos[0] = min(max(camera_pos[0],0),tile_size*tile_res[0]-screen_size[0])
    camera_pos[1] = min(max(camera_pos[1],0),tile_size*tile_res[1]-screen_size[1])
    
    mouse_tile = [(mouse_pos[0]+camera_pos[0])//tile_size,(mouse_pos[1]+camera_pos[1])//tile_size]
    
    background_pos = [-camera_pos[0]/5,-camera_pos[1]/12]
    
    if camera_pos[0] <= 4000:
        screen.blit(background_sprites[0],background_pos)
    screen.blit(background_sprites[0],(background_pos[0]+96*8,background_pos[1]))
    if camera_pos[0] >= 1650:
        screen.blit(background_sprites[0],(background_pos[0]+96*8*2,background_pos[1]))
        screen.blit(background_sprites[0],(background_pos[0]+96*8*3,background_pos[1]))
    
    top_left = [camera_pos[0]//tile_size,camera_pos[1]//tile_size]
    top_left = [min(top_left[0],tile_res[0]),min(top_left[1],tile_res[1])]

    bottom_right = [(camera_pos[0]+screen_size[0])//tile_size+1,(camera_pos[1]+screen_size[1])//tile_size+1]
    bottom_right = [min(bottom_right[0],tile_res[0]),min(bottom_right[1],tile_res[1])]
    
    for z in range(len(tiles)):
        for y in range(top_left[1],bottom_right[1]):
            for x in range(top_left[0],bottom_right[0]):
                
                tile_pos = [x*tile_size-camera_pos[0],y*tile_size-camera_pos[1]]
                
                t = tiles[z][y][x]
                
                screen.blit(tile_sprites[t],(tile_pos))
                
                if [x,y] in player_tiles:
                    pygame.draw.rect(screen,(255,0,255),(*tile_pos,tile_size,tile_size),2)

    screen.blit(character_sprites[0],[player_pos[0]-camera_pos[0]-player_size[0]/2,player_pos[1]-camera_pos[1]-player_size[0]/2])
    
    for i in check_tiles:
        pygame.draw.circle(screen,(0,255,0),(i[0]*player_size[0]/2+player_pos[0]-camera_pos[0],i[1]*player_size[1]/2+player_pos[1]-camera_pos[1]),4)
    
    pygame.display.update()
    clock.tick(60)