#!/usr/bin/python3

import socket
import sys
from dico_protocol import format_request
from dico_protocol import format_request_set

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 5 :
    print("Usage: dico_admin.py <server> <port> <login> <password>")
    s.close()
    sys.exit(1)

dico_admin = sys.argv[0]
host = sys.argv[1]
port = int(sys.argv[2])
login = sys.argv[3]
password = sys.argv[4]

s.connect((host, port))

secured_data = format_request(dico_admin, login, password)
s.sendall(secured_data)
print((s.recv(1500)).decode("utf-8"))

while True :
    sarg="" #ici je reconstruis les arguments parce que si on tape "Mike Tyson", sys.argv le coupe en deux. Donc je recolle tout avec des espaces
    cptarg =0
    while(cptarg < len(sys.argv)-1):
        sarg+=(sys.argv[cptarg]+" ")
        cptarg+=1
    sarg+=(sys.argv[cptarg]) #on évite ici d'ajouter un espace après pour contourner de possibles erreurs

    buffer = sarg.split(" ",2)
    dico = buffer[0]
    if dico=="exit":
        s.sendall(f"exit".encode("utf-8"))
    command = buffer[1]
    if command == "set":
        arg_and_value = buffer[2].split("|",1)
        arg=arg_and_value[0]
        value = arg_and_value[1]
    elif command == "del":
        value = buffer[2]

    else :
        print("Usage: dico_client.py <server> <port> <command> <arg>")
        print("Commands:")
        print("get <key> : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.")
        print("pref <prefix> : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.")
        s.close()
        sys.exit(1)
    if command == "set":
        data = format_request_set(dico, command, arg, value)
    elif command =="del":
        data = format_request(dico, command, value)
    s.sendall(data)
s.close()