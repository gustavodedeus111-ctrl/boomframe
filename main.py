from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController 
from ursinanetworking import *
from random import uniform 
from panda3d.core import CardMaker, TransparencyAttrib
from mapa import Mapa
import os

app = Ursina(development_mode=False)




# Configuração do jogador
jogador = FirstPersonController(collider='box')  
jogador.cursor.visible = False 

mapa = Mapa()

# Configuração do céu
ceu = Sky()

# Configurar uma arma para o jogador
arma = Entity(
    parent=camera.ui,    
    model='quad',
    texture='assets/arma.png',
    scale=(2, 0.5),    
    position=(0.80, -0.70),
    rotation=(0, 0, 70),
    color=color.white,
    always_on_top=True
)

# === MIRA =========================================================================================
mira = Entity(
    model='quad',
    parent=camera.ui,
    color=color.white,
    position=(0, 0, 0),
    scale=0.005, # Ajuste para o tamanho desejado
    always_on_top=True
)

#==================================================================================================

velocidade_normal = 19
velocidade_corrida = 27
jogador.jump_height = 3
jogador.gravity = 1

def input(key):
    if key == 'left shift' and held_keys['w']:
        jogador.speed = velocidade_corrida

    if key == 'left shift up':
        jogador.speed = velocidade_normal



# ================================================================================================
# Criar função de disparo
def disparar():
    posicao_inicial = camera.ui.get_position(relative_to=scene) + Vec3(0.9, -0.5, 0)
    direcao_disparo = camera.forward.normalized()
    projétil = Entity(
        model='sphere',
        color=color.yellow,
        scale=1,
        position=posicao_inicial,
        collider='box',
        always_on_top=True
    )
    projétil.animate_position(
        projétil.position + direcao_disparo * 50,
        duration=0.2,
        curve=curve.linear
    )
    destroy(projétil, delay=1)




# --- LÓGICA DO MENU INICIAL ---

# 1. Desativar o jogador e elementos do jogo no início============================================
jogador.enabled = False
arma.enabled = False
mira.enabled = False
mouse.visible = True  

# 2. Criar o Fundo do Menu =======================================================================
fundo_menu = Entity(
    parent=camera.ui,
    model='quad',
    texture='assets/telas/tela_botoes.png', 
    scale=(camera.aspect_ratio, 1),
    z=1 
)

# Vesão ==========================================================================================
versao_texto = "v?.?.?" 
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'version.txt')
try:
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            versao_texto = f.read().strip()
    else:
        print("Erro: Arquivo version.txt não encontrado na pasta!")
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")

exibir_versao = Text(
    text=f"{versao_texto}",
    parent=camera.ui,
    position=(0.8, -0.45), 
    scale=1.2,
    color=color.white,    
    z=-10                  
)


# 3. Criar o Botão de Iniciar====================================================================
def iniciar_jogo():
    jogador.enabled = True
    arma.enabled = True
    mira.enabled = True
    fundo_menu.enabled = False
    botao_play.enabled = False
    botao_multiplayer.enabled = False
    exibir_versao.enabled = False
    jogador.cursor.visible = False
    mouse.visible = False
#================================================================================================




menu_principal = Entity(parent=camera.ui)

def mostrar_multiplayer():
    menu_principal.disable()  
    menu_multiplayer.enable()   

botao_play = Button(
    texture='assets/telas/btn_play.png',
    parent=menu_principal,    
    color=color.white,
    model='quad',
    scale=(0.4, 0.10),
    y=-0.1,
    z=-0.01,
    highlight_color=color.light_gray, 
    pressed_color=color.gray,
    on_click=iniciar_jogo
)

botao_multiplayer = Button(
    texture='assets/telas/btn_multi.png',
    scale=(0.4, 0.10),
    y=-0.25,
    z=-0.02,
    model='quad',
    parent=menu_principal,
    color=color.white,
    highlight_color=color.light_gray,
    on_click=mostrar_multiplayer 
)

# --- CONTAINER DO MENU MULTIPLAYER ---=====================================================================================||||
menu_multiplayer = Entity(parent=camera.ui, enabled=False) 


fundo_ip = Entity(
    parent=menu_multiplayer,
    model='quad',
    texture='assets/telas/ipcam.png',

    highlight_color=color.black,
    scale=(0.5, 0.11),
    y=0.1,
    color=color.white
)

#  O campo de entrada (sem fundo próprio)===============================================================
campo_ip = InputField(
    parent=fundo_ip,
    scale=(0.9, 0.8), 
    color=color.black, 
    default_value='000.0.0.0',
    character_limit=22
    
)
campo_ip.text_field.y = 0.15





# Botão para conectar=====================================================================================
botao_conectar = Button(
    texture='assets/telas/btn_conectar.png',
    scale=(0.4, 0.10),
    color=color.white,
    y=-0.1,
    z=-0.01,
    parent=menu_multiplayer,
    model='quad',
    highlight_color=color.light_gray,
    on_click=lambda: print(f"Conectando ao IP: {campo_ip.text}")
)


# =======================================================================================================

client = UrsinaNetworkingClient("localhost", 25565)
fantasmas = {}

# 2. Criar o modelo dos outros jogadores
def criar_fantasma(id):
    fantasma = Entity(
        model='cube', 
        color=color.orange, 
        scale=(1, 2, 1), 
        collider='box',
        position=(0, 5, 0)
    )
    fantasmas[id] = fantasma

# 3. Processar mensagens da rede
@client.event
def on_player_pos(data):
    id_inimigo = data["id"]
    posicao = data["pos"]
    
    if id_inimigo not in fantasmas:
        criar_fantasma(id_inimigo)
    
    fantasmas[id_inimigo].position = posicao

def update():
    # ... seu código existente ...
    for tree in mapa.trees:
        tree.look_at_2d(jogador, 'y')
        tree.rotation_y += 180

    for minepedras in mapa.mpedras:
        minepedras.look_at_2d(jogador, 'y')
        minepedras.rotation_y += 180

    for matinhos in mapa.matin:
        matinhos.look_at_2d(jogador, 'y')
        matinhos.rotation_y += 180

    
    
    # Enviar sua posição para os outros
    if client.connected:
        client.send_message("update_pos", {
            "id": client.id, 
            "pos": jogador.position
        })
    
    client.process_net_events()





# Botão para voltar=====================================================================================
botao_voltar = Button(
    texture='assets/telas/btn_voltar.png',
    scale=(0.4, 0.10),
    y=-0.25,
    z=-0.02,
    model='quad',
    color=color.white,
    parent=menu_multiplayer,
    highlight_color=color.light_gray,
    on_click=lambda: [menu_multiplayer.disable(), menu_principal.enable()]
)



app.run()