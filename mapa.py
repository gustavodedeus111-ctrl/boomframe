from ursina import *
from random import uniform

class Mapa:
    def __init__(self):
        self.blocos = []
        self.direcoes = []
        self.trees = []
        self.mpedras = []
        self.matin = []

        self.criar_chao()
        self.criar_objetos()
        self.criar_arvores()
        self.criar_pedras()
        self.criar_matinhos()

    def criar_chao(self):
        self.chao = Entity(
            model='plane',
            texture='assets/cenario/chao4.png',
            collider='box',   # MUITO mais leve
            scale=(300, 1, 300),
            texture_scale=(30, 30)
        )

    def criar_objetos(self):
        Entity(
            model='cube',
            texture='brick',
            collider='box',
            position=(15, 0.5, 5),
            scale=(20, 6, 0.4)
        )

        Entity(model='cube', texture='brick', collider='box',
               position=(149, 10, 0), scale=(0.8, 20, 305))
        Entity(model='cube', texture='brick', collider='box',
               position=(-149, 10, 0), scale=(0.8, 20, 305))
        Entity(model='cube', texture='brick', collider='box',
               position=(0, 10, 149), scale=(305, 20, 0.8))
        Entity(model='cube', texture='brick', collider='box',
               position=(0, 10, -149), scale=(305, 20, 0.8))

    def criar_arvores(self):
        quantidade_de_arvores = 200
        
        for i in range(quantidade_de_arvores):
            x_aleatorio = uniform(-145, 145)
            z_aleatorio = uniform(-145, 145)
            
            tree = Entity(
                model='quad',
                texture='assets/cenario/arvore.png',
                scale=(10, 11),
                position=(x_aleatorio, 5, z_aleatorio),
                collider='box'
            )
            self.trees.append(tree)

    def criar_pedras(self):
        quantidade_de_pedras = 50
        
        for i in range(quantidade_de_pedras):
            x_aleatorio = uniform(-145, 145)
            z_aleatorio = uniform(-145, 145)
            
            minepedras = Entity(
                model='quad',
                texture='assets/cenario/minepedras.png',
                scale=(1, 0.4),
                position=(x_aleatorio, 0.5, z_aleatorio)
            )
            self.mpedras.append(minepedras)

    def criar_matinhos(self):
        quantidade_de_matinhos = 250
        
        for i in range(quantidade_de_matinhos):
            x_aleatorio = uniform(-145, 145)
            z_aleatorio = uniform(-145, 145)
            
            matinhos = Entity(
                model='quad',
                texture='assets/cenario/matinho.png',
                scale=(1, 1),
                position=(x_aleatorio, 0.5, z_aleatorio)
            )
            self.matin.append(matinhos)


