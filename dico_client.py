#!/usr/bin/python3

import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 6:
    print("Usage: dico_client.py <server> <port> <dico> <command> <arg>")
    s.close()
    sys.exit(1)

sarg="" #pour pouvoir accueillir l'argument "Mike Tyson" qui contient un espace, sys.argv n'est plus efficace pour la gestion du nombre d'arguments donc on crée une chaîne de caractères pour pouvoir la diviser
cptarg =0 #initialisation du compteur d'arguments
while(cptarg < len(sys.argv)-1):
    sarg+=(sys.argv[cptarg]+" ") #on concatène tout les arguments donnés par le client
    cptarg+=1
sarg+=(sys.argv[cptarg]) #on évite ici d'ajouter un espace après pour contourner de possibles erreurs

buffer = sarg.split(" ",5)
host = buffer[1]
port = int(buffer[2])
dico = buffer[3]
s.connect((host, port))
command = buffer[4]
if command == "get" or command == "pref" :
    arg = buffer[5]
elif command == "set" or command == "del":
    print("VOUS DEVEZ ÊTRE ADMIN")
    s.close()
    sys.exit(1)
else :
    print("Usage: dico_client.py <server> <port> <command> <arg>")
    print("Commands:")
    print("get <key> : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.")
    print("pref <prefix> : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.")
    s.close()
    sys.exit(1)
data=(dico+" "+command+" "+arg).encode()
s.sendall(data)
print((s.recv(1500)).decode("utf-8"))
s.close()