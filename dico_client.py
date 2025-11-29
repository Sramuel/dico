#!/usr/bin/python3

import socket
import sys
from dico_protocol import format_request

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 6:
    print("Usage: dico_client.py <server> <port> <dico> <command> <arg>")
    s.close()
    sys.exit(1)

sarg="" #ici je reconstruis les arguments parce que si on tape "Mike Tyson", sys.argv le coupe en deux. Donc je recolle tout avec des espaces
cptarg =0
while(cptarg < len(sys.argv)-1):
    sarg+=(sys.argv[cptarg]+" ")
    cptarg+=1
sarg+=(sys.argv[cptarg]) #on évite ici d'ajouter un espace après pour contourner de possibles erreurs

#maintenant je recoupe proprement en limitant à 5 morceaux pour que le dernier argument reste entier
buffer = sarg.split(" ",5) #[dico_client.py, host, port, dico, command, argument_avec_espaces]
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
data = format_request(dico, command, arg)
s.sendall(data)
print((s.recv(1500)).decode("utf-8"))
s.close()