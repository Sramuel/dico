#!/usr/bin/python3

import socket
import select
from dico_local import *
from dico_protocol import *

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l=[] #liste sockets clients
try: #crée le serveur et ouvre les connexion
    port = int(sys.argv[1])
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #évite le Adress already in use
    ss.bind(("",port))
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
                buffer = data.decode("utf-8").strip()
                cmdarg=buffer.split(" ",1)
                command = cmdarg[0]
                dico: Dict[str, str] = load_dico(f"data/{sys.argv[2]}")
                if command == 'get':
                    key: str = cmdarg[1]
                    if key in dico:
                        s.sendall(f"{dico[key]}".encode("utf-8"))
                    else:
                        s.sendall("Key not found".encode("utf-8"))
                else:
                    s.sendall(f"Unknown command: {command}".encode("utf-8"))
ss.close()