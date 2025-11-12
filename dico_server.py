import socket

s_serveur = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM)
s_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_serveur.bind(("",7777))
s_serveur.listen(1)

l = []

while True :