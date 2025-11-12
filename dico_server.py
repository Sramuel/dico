#!/usr/bin/python3

import socket
import sys
import select


ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
l=[] #liste sockets clients
try: #crée le serveur et ouvre les connexion
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #évite le Adress already in use
    ss.bind(("",7777))
    ss.listen(1)

except Exception as e: #si erreur pour créer le serveur
    print("socket error!", e)
    sys.exit(1)
while True: #on reçoit les données envoyé par le client, si elles sont vide on ferme la connexion avec break
    #attente surveillance de plusieurs socket
    rlist,_,_=select.select(l+[ss],[],[]) #rlist contient les sockets disponible en lecture
    for s in rlist:
        if s ==ss: #Si c’est la socket "serveur", c’est qu’un client vient de se connecter
            conn, addr = ss.accept()
            l.append(conn) #on ajoute la socket client
        else : #le client de cette socket nous a envoyé des donnée
            data = s.recv(1500)
            if not data:
                l.remove(s) #on retire la socket client qui nous a envoyé des données une fois la connexion fermé
                s.close()
            else:
                
ss.close()