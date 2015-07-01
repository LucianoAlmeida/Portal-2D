# -*- coding: utf8 -*-

''''
Game: Portal 2D
Semestre: 1/2015

Alunos: Guilherme Willer Dias Araujo          13/0045080
        Luciano Henrique Nunes de Almeida     11/0063392       
'''
from FGAme import *

world = World(background=(255,255,255),gravity=800,
              dfriction=2, restitution=0.0)

conf.set_resolution(1280,600)

# Carregando imagens
imgs = [pygame.image.load('images/char%s.gif' % i) for i in range(0, 8)]
imgs_carry = [pygame.image.load('images/cube_char%s.gif' % i) for i in range(0, 8)]
floor = pygame.image.load('images/fullfloor.gif')
background = pygame.image.load('images/fullbackground.gif')
ceiling = pygame.image.load('images/fullceiling.gif')
column = pygame.image.load('images/column_left.gif')
door = pygame.image.load('images/door.gif')
open_door = pygame.image.load('images/door_open.gif')
barier = pygame.image.load('images/barier.gif')
portal_surface = pygame.image.load('images/portal_surface.gif')
companion_cube = pygame.image.load('images/companion_cube.gif')
button = pygame.image.load('images/button.gif')
portal_blue1 = pygame.image.load('images/portal_blue1.gif')
portal_orange1 = pygame.image.load('images/portal_orange1.gif')
the_end = pygame.image.load('images/the_end.gif')

# Pegando dimensões das imagens
_x, _y, dx, dy = imgs[0].get_rect()
_xcube, _ycube, dxcube, dycube = companion_cube.get_rect()
objs_cenario = []
tipo_tiro = None
ativa_portal = False


#Adicionando AABBs ao mundo
box = AABB(200, dx+200, 200, dy+200, color=None, world=world)
box.make_static_angular()
cube = AABB(752, dxcube + 752, 97, dycube + 97, color=None, world=world)
cube.make_static_angular()
objs_cenario.append(cube)

#AABBs chão
ground_left = AABB(shape=(1280, 100), mass='inf', pos=(640, 53), 
              world=world, color=None)

objs_cenario.append(ground_left)

# AABBs teto
ceilling_left = AABB(shape=(1280, 100), mass='inf', pos=(103, 640), 
                 world=world, color=None, col_layer=1)
objs_cenario.append(ceilling_left)

column_left = AABB(shape=(85, 500), mass='inf', pos=(18, 340), 
                   world=world, color=None)
objs_cenario.append(column_left)
column_right = AABB(shape=(85, 500), mass='inf', pos=(1278, 340), 
                    world=world, color=None)
objs_cenario.append(column_right)
barier_block = AABB(shape=(85, 236), mass='inf', pos=(644, 207), 
                    world=world, color=None)
objs_cenario.append(barier_block)

surface_down_left = AABB(shape=(206, 30), mass='inf', pos=(422, 106),
                         world=world, color=None, col_layer=1)

surface_up_right = AABB(shape=(206, 30), mass='inf', pos=(955, 588),
                        world=world, color=None, col_layer=1)

surface_up_left = AABB(shape=(206, 30), mass='inf', pos=(422, 588),
                       world=world, color=None, col_layer=1)

surface_down_right = AABB(shape=(206, 30), mass='inf', pos=(955, 106),
                          world=world, color=None, col_layer=1)

button_aabb = AABB(shape=(102,13), mass='inf', pos=(140, 103), world=world, color=None)

idx = 0
moving = 1
jumping = False
jumping_state = 0
carry_on = False
has_shot = False
tiro = None
tipo_tiro = None
botao_acionado = False
movido = False
parede1 = 0
parede2 = 5
ativa_portal = False
azul = 0
laranja = 0

def colidiu (objeto1=None, objeto2=None, eixo=None):
    global box
    global cube
    if (objeto1 == None or objeto2 == None and eixo==None):
        if(box.xmin - 20 < cube.xmax + 20 and box.xmax + 20 > cube.xmin - 20):
            return True
        else:
            return False
    elif (eixo == 'y'):
        if (objeto1.ymin < objeto2.ymax and objeto1.ymax > objeto2.ymin):
            return True
        else:
            return False
    else:
        if (objeto1.xmin < objeto2.xmax and objeto1.xmax > objeto2.xmin):
            if (objeto1.ymin < objeto2.ymax and objeto1.ymax > objeto2.ymin):
                return True
            else:
                return False
        else:
            return False
    
@world.listen('long-press', 'd')
def moving_right():
    global moving, jumping_state
    moving = 2
    jumping_state = 1
    if (box._vel[0] <= 250):
        box.boost(100, 0)
    
@world.listen('key-up', 'd')
def stopping_right():
    global moving
    moving = 1
    
@world.listen('long-press', 'a')
def moving_left():
    global moving, jumping_state
    jumping_state = -1
    moving = -2
    if (box._vel[0] >= -250):
        box.boost(-100, 0)
    
@world.listen('key-up', 'a')
def stopping_left():
    global moving
    moving = -1

@world.listen('key-down', 'w')
def jumping_true():
    global jumping
    
    if (jumping == False):
        box.boost(0, 350)
        jumping = True
        
@world.listen('pre-draw')
def draw_sprite(screen):
    global idx, has_shot, objs_cenario, entidades, tipo_tiro, movido, ativa_portal, azul
    global moving, jumping, jumping_state, tiro, botao_acionado, parede1, parede2, laranja
    idx += 0.1
    dx, dy = box.shape
    dxcube, dycube = cube.shape
    
    for objs in objs_cenario:
        if(colidiu(tiro, objs) and tiro != None):
            tiro._color = (None)
            tiro.move(99999, 99999)
            has_shot = False
    
    #Imprimindo cenário 
    pg_background = screen.get_screen()
    pg_background.blit(background, (7, -21, 0, 0))
    
    pg_floor = screen.get_screen()
    pg_floor.blit(floor, (0, 500, 0, 0))
    
    pg_ceiling = screen.get_screen()
    pg_ceiling.blit(ceiling, (-2, 0, 0, 0))
    
    pg_column = screen.get_screen()
    pg_column.blit(column, (-23, -63, 0, 0))
    
    pg_barier = screen.get_screen()
    pg_barier.blit(barier, (604, 275, 0, 0))
    
    pg_surface = screen.get_screen()
    pg_surface.blit(portal_surface, (320, 500, 0, 0))
    pg_surface.blit(portal_surface, (320, -1, 0, 0))
    pg_surface.blit(portal_surface, (852, 500, 0, 0))
    pg_surface.blit(portal_surface, (852, -1, 0, 0))
    
    pg_portal_orange = screen.get_screen()
    pg_portal_blue = screen.get_screen()
    
    pg_button = screen.get_screen()
    pg_button.blit(button, (90, 490, 0, 0))
    
    if(parede1 == parede2 or parede2 == parede1):
        parede1 = 0
        parede2 = 5
    
    if(tipo_tiro):
        if (colidiu(tiro, surface_down_left)):
            laranja = 1
            ativa_portal = True
            parede1 = 1
        
        elif (colidiu(tiro, surface_up_right)):
            laranja = 2
            ativa_portal = True
            parede1 = 2
            
        elif (colidiu(tiro, surface_up_left)):
            laranja = 3
            ativa_portal = True
            parede1 = 3
            
        elif (colidiu(tiro, surface_down_right)):
            laranja = 4
            ativa_portal = True
            parede1 = 4
        
    if(ativa_portal):
        if (parede1 == 1):
            pg_portal_orange.blit(portal_orange1, (320, 500, 0, 0))
        
        elif (parede1 == 2):
            pg_portal_orange.blit(portal_orange1, (852, -1, 0, 0))
            
        elif (parede1 == 3):
            pg_portal_orange.blit(portal_orange1, (320, -1, 0, 0))
          
        elif (parede1 == 4):
            pg_portal_orange.blit(portal_orange1, (852, 500, 0, 0))   
            
    if not (tipo_tiro):
        if (colidiu(tiro, surface_down_left)):
            azul = 1
            ativa_portal = True
            parede2 = 1
            
        elif (colidiu(tiro, surface_up_right)):
            azul = 2
            ativa_portal = True
            parede2 = 2
            
        elif (colidiu(tiro, surface_up_left)):
            azul = 3
            ativa_portal = True
            parede2 = 3
            
        elif (colidiu(tiro, surface_down_right)):
            azul = 4
            ativa_portal = True
            parede2 = 4
        
            
    if(ativa_portal):
        if (parede2 == 1):
            pg_portal_blue.blit(portal_blue1, (320, 500, 0, 0))
            
        elif (parede2 == 2):
            pg_portal_blue.blit(portal_blue1, (852, -1, 0, 0))
            
        elif (parede2 == 3):
            pg_portal_blue.blit(portal_blue1, (320, -1, 0, 0))
            
        elif (parede2 == 4):
            pg_portal_blue.blit(portal_blue1, (852, 500, 0, 0))

    if (azul == 1):
        if (laranja == 3):
            if (colidiu(box, surface_down_left)):
                box.move(0,400)
        if (laranja == 2):
            if (colidiu(box, surface_down_left)):
                box.move(650, 400)
    if (azul == 4):
        if (laranja == 3):
            if (colidiu(box, surface_down_right)):
                box.move(-550,400)
        if (laranja == 2):
            if (colidiu(box, surface_down_right)):
                box.move(0, 400)
    
    if (laranja == 1):
        if (azul == 3):
            if (colidiu(box, surface_down_left)):
                box.move(0,400)
        if (azul == 2):
            if (colidiu(box, surface_down_left)):
                box.move(650, 400)
    if (laranja == 4):
        if (azul == 3):
            if (colidiu(box, surface_down_right)):
                box.move(-550,400)
        if (azul == 2):
            if (colidiu(box, surface_down_right)):
                box.move(0, 400)

    # Player aterrisou
    if (colidiu(box, ground_left, 'y') 
        or colidiu(box, button_aabb, 'y')
        or colidiu(box, barier_block, 'y') 
        or colidiu(box, cube, 'y')):
        jumping = False
    else:
        jumping = True
        
    if (colidiu(cube, button_aabb)):
        botao_acionado = True
        pg_door = screen.get_screen()
        pg_door.blit(open_door, (1235, -89, 0, 0))
        if (not movido):
            movido = True
            column_right.move(5555,5555)
    else:
        botao_acionado = False
        pg_door = screen.get_screen()
        pg_door.blit(door, (1235, -89, 0, 0))
        if(movido):
            movido = False
            column_right.move(1278, 340)
        
    if colidiu():
        @world.listen('key-down', 'e')
        def carry():
                global cube
                global carry_on 
                carry_on = True
                cube.destroy()
                cube.move(7777,7777)
                
    # Animação do player
    if not carry_on:
        pg_companion_cube = screen.get_screen()
        pg_companion_cube.blit(companion_cube, (cube.xmin, 600 - cube.ymax, dxcube, dycube))
        
        if (box.ymin <= ground_left.ymax):
            jumping = False
        if(jumping == False):
            if (moving == 2):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 2) + 1], (box.xmin, 600 - box.ymax, dx, dy))
            elif(moving == 1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 1)], (box.xmin, 600 - box.ymax, dx, dy))
            elif (moving == -1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 1) + 3], (box.xmin, 600 - box.ymax, dx, dy))
            elif(moving == -2):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 2) + 4], (box.xmin, 600 - box.ymax, dx, dy))
        elif(jumping == True):
            if(jumping_state == 1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 1) + 6], (box.xmin, 600 - box.ymax, dx, dy))
            elif(jumping_state == -1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs[int(idx % 1) + 7], (box.xmin, 600 - box.ymax, dx, dy))
    else:
        if (box.ymin <= ground_left.ymax):
            jumping = False
        if(jumping == False):
            if (moving == 2):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 2) + 1], (box.xmin, 600 - box.ymax, dx, dy))
            elif(moving == 1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 1)], (box.xmin, 600 - box.ymax, dx, dy))
            elif (moving == -1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 1) + 3], (box.xmin, 600 - box.ymax, dx, dy))
            elif(moving == -2):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 2) + 4], (box.xmin, 600 - box.ymax, dx, dy))
        elif(jumping == True):
            if(jumping_state == 1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 1) + 6], (box.xmin, 600 - box.ymax, dx, dy))
            elif(jumping_state == -1):
                pg_screen = screen.get_screen()
                pg_screen.blit(imgs_carry[int(idx % 1) + 7], (box.xmin, 600 - box.ymax, dx, dy))
                
    pg_the_end = screen.get_screen() 
    testax, testay= box.pos_left
    if(testax > 1280 and testay <0): 
        pg_the_end.blit(the_end, (0,0,0,0))

if not colidiu():
    @world.listen('key-down', 'q')
    def drop_cube():
        global carry_on
        global cube
        if (carry_on):
            if (jumping_state == 1):
                carry_on = False
                cube = AABB(box.xmin + 90, dxcube + box.xmin + 90, box.ymin, dycube + box.ymin, color=None, world=world)
                cube.make_static_angular()
            elif (jumping_state == -1):
                carry_on = False
                cube = AABB(box.xmin - 70, dxcube + box.xmin - 70, box.ymin, dycube + box.ymin, color=None, world=world)
                cube.make_static_angular()
        tiro = False

class shoot(World):
    @listen('mouse-button-down', 'left')
    def blue_shot(self, pos):
        global has_shot
        global tiro
        global tipo_tiro, carry_on
        vec_direita = Vec2(pos[0]-box.pos_right[0], pos[1]-box.pos_right[1])
        vec_esquerda = Vec2(pos[0]-box.pos_left[0], pos[1]-box.pos_left[1])
        if (has_shot == False): 
            if (carry_on == False):
                if (moving == 1 or moving == 2):
                    tiro = Circle(5, pos=box.pos_right, color=(0,0,255), col_layer=1)
                    tiro.make_static()
                    tiro.boost(vec_direita.normalize()*500)
                elif(moving == -1 or moving == -2):
                    tiro = Circle(5, pos=box.pos_left, color=(0,0,255), col_layer=1)
                    tiro.make_static()
                    tiro.boost(vec_esquerda.normalize()*500)
                world.add(tiro)
            tipo_tiro = False
            has_shot = True
                
    @listen('mouse-button-down', 'right')
    def orange_shot(self, pos):
        global has_shot
        global tiro
        global tipo_tiro
        vec_direita = Vec2(pos[0]-box.pos_right[0], pos[1]-box.pos_right[1])
        vec_esquerda = Vec2(pos[0]-box.pos_left[0], pos[1]-box.pos_left[1])
        if (has_shot == False):
            if(carry_on == False):
                if (moving == 1 or moving == 2):
                    tiro = Circle(5, pos=box.pos_right, color=(255,165,0), col_layer=1)
                    tiro.make_static()
                    tiro.boost(vec_direita.normalize()*500)
                elif(moving == -1 or moving == -2):
                    tiro = Circle(5, pos=box.pos_left, color=(255,165,0), col_layer=1)
                    tiro.make_static()
                    tiro.boost(vec_esquerda.normalize()*500)
                world.add(tiro)
            tipo_tiro = True
            has_shot = True

shoot = shoot()
world.run()
