from ursinanetworking import *

server = UrsinaNetworkingServer("localhost", 25565)

@server.event
def update_pos(client, data):
    # Retransmite a posição para todo mundo, exceto para quem enviou
    server.broadcast("on_player_pos", data, (client,))

print("Servidor Rodando...")
while True:
    server.process_net_events()