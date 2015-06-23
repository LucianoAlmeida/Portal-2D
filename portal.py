# -*- coding: utf8 -*-

###
# Game: Portal 2D
# Aluno: Luciano Henrique Nunes de Almeida
# Matrícula: 11/0063392
###

from FGAme import *
import numpy as np

inf = np.inf

''' Classe da fase '''
class stage(World):
    #left border
    def load(self):
        print("O cenário acabou de ser carregado!")
        # Carregando borda esquerda
        self.border = AABB(shape=(50,600), mass=inf, pos=(25,300)) 
        scenario_aabbs.append(self.border)
        # Carregando borda direita
        self.border = AABB(shape=(50,600), mass=inf, pos=(775,300)) 
        scenario_aabbs.append(self.border)
        # Carregando borda inferior
        self.border = AABB(shape=(800,100), mass=inf, pos=(400,50)) 
        scenario_aabbs.append(self.border)
        # Carregando borda superior
        self.border = AABB(shape=(800,100), mass=inf, pos=(400,550)) 
        scenario_aabbs.append(self.border)
        
        #Carregando plataforma no centro
        platform = AABB(shape=(300,200), mass=inf, pos=(400,100))
        scenario_aabbs.append(platform)
        
        # Carregando entrada da fase
        door = AABB(shape=(70,100), pos=(150,150), mass=inf, color=(200,255,255), col_layer=1)
        entities_aabbs.append(door)
        
        # Carregando Saida da fase
        door = AABB(shape=(70,100), pos=(650,150), mass=inf, color=(100,200,200), col_layer=1)
        entities_aabbs.append(door)
        
        # Adicionando elementos ao mundo
        for aabb in scenario_aabbs:
            world.add(aabb)
        for aabb in entities_aabbs:
            world.add(aabb)
            
''' Classe do personagem '''
class character(World):
    mass = 10
    shape = (25, 60)
    pos = (150,140)
    is_jumping = 0
    is_moving = 0
    
    def load(self):
        # Carregando jogador
        self.player = Rectangle(pos=self.pos, shape=self.shape, color=(250,230,185))
        self.player.make_static_angular()
        entities_aabbs.append(self.player)
        
    @listen('frame-enter')
    def update_position(self):
        print("Atualizando posições")
        
    @listen('long-press', 'd')
    def move_right(self):
        self.player.boost(10, 0)
        
    @listen('long-press', 'a')
    def move_left(self):
        self.player.boost(-10, 0)
        
    @listen('long-press', 'w')
    def jump(self):
        if(self.is_jumping == 0):
            self.player.boost(0, 300)
            self.player
            self.is_jumping = 1
            
class tiles(World):
    def load(self):
        shape_vertical = (5,98)
        shape_horizontal = (98,5)
        color = (150,150,150)
        
        # Colocando tiles no teto
        for i in range(7):
            self.tile = AABB(shape=shape_horizontal, mass=inf, pos=(100+(100*i),500), color=color) 
            scenario_aabbs.append(self.tile)
            
        # Colocando tiles no chão
        for i in range(2):
            self.tile = AABB(shape=shape_horizontal, mass=inf, pos=(100+(100*i),100), color=color) 
            scenario_aabbs.append(self.tile)
        for i in range(2):
            self.tile = AABB(shape=shape_horizontal, mass=inf, pos=(600+(100*i),100), color=color) 
            scenario_aabbs.append(self.tile)
        for i in range(3):
            self.tile = AABB(shape=shape_horizontal, mass=inf, pos=(300+(100*i),200), color=color) 
            scenario_aabbs.append(self.tile)
            
        # Colocando tiles na parede esquerda
        for i in range(4):
            self.tile = AABB(shape=shape_vertical, mass=inf, pos=(50,150+(100*i)), color=color) 
            scenario_aabbs.append(self.tile)
            
        # Colocando tiles na parede direita    
        for i in range(4):
            self.tile = AABB(shape=shape_vertical, mass=inf, pos=(750,150+(100*i)), color=color) 
            scenario_aabbs.append(self.tile)
            
        for i in range(2):
            self.tile = AABB(shape=shape_vertical, mass=inf, pos=(250+(300*i),150), color=color) 
            scenario_aabbs.append(self.tile)
    
''' Classe dos cubos '''
class companion_cube(World):
    def load(self):
        print("O companion cube acabou de ser carregado!")
    
        
''' Inicializa todos os objetos do mundo que será criado '''
def init():
    stage.load()
    tiles.load()
    character.load()
    companion_cube.load()
    
def add_to_world():
    # Adicionando elementos ao mundo
    for aabb in scenario_aabbs:
        world.add(aabb)
    for aabb in entities_aabbs:
        world.add(aabb)

# Variáveis globais

scenario_aabbs = []
entities_aabbs = []

# Criando objetos
world = World(background=(255,255,255),gravity=800,
              dfriction=0.3)
stage = stage()
character = character()
companion_cube = companion_cube()
tiles = tiles()
    
''' Loop pincipal do jogo '''
def main():
    init()
    add_to_world()
    world.run()

if (__name__ == '__main__'):
    main()
