#!/usr/bin/python3

import socket
import sys
from dico_protocol import format_request

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 5 : 
    print("Usage: dico_admin.py <server> <port> <login> <password>")
    s.close()
    sys.exit(1)

dico_admin = "dico_admin.py" #pas sys.argv[0] car il enregistrerait "./dico_admin.py" comme nom de dico au lieu de "dico_admin.py"
host = sys.argv[1]
port = int(sys.argv[2])
login = sys.argv[3]
password = sys.argv[4]

s.connect((host, port))

secured_data = format_request(dico_admin, login, password)
s.sendall(secured_data)
msg = s.recv(1500).decode("utf-8")
print(msg)
if msg != "Nice ! You are logged in !!!": #si échec de login, on quitte
    s.close()
    sys.exit(1)

while True :
    sarg = input() #on lit la commande entrée par l'utilisateur
    if sarg == "": #évite le crash si on appuie juste sur entrée sans rien taper
        continue #prochain input
    buffer = sarg.split(" ",2)
    if len(buffer) < 2 and buffer[0] != "exit": #pour éviter le crash si n'importe quoi est tapé
        print("Format invalide")
        continue #prochain input
    dico = buffer[0]
    if dico=="exit":
        s.sendall(f"exit".encode("utf-8"))
        break #on quitte le programme
    command = buffer[1]
    data = None
    if command == "set":
        if "|" in buffer[2]: #on vérifie que l'utilisateur a bien mis le séparateur entre clé et valeur
            arg_and_value = buffer[2].split("|",1) #on sépare en deux parties seulement (clé et valeur)
            arg=arg_and_value[0] #clé
            value = arg_and_value[1] #valeur
        else:
            print("Erreur: Pour set, utilisez le format cle|valeur")
            continue #prochain input
    elif command == "del":
        value = buffer[2] #clé à supprimer

    else :
        print("Usage: <dico.json> <command> <arg>")
        print("Commands:")
        print("set <key|value>, del <key>")
        continue #prochain input
    if command == "set":
        data = format_request(dico, command, f"{arg}|{value}") #on envoie clé et valeur séparées par |
    elif command =="del":
        data = format_request(dico, command, value) #on envoie juste la clé à supprimer
    if data: 
        s.sendall(data) #envoi de la commande au serveur
        print((s.recv(1500)).decode("utf-8")) #affichage de la réponse du serveur
s.close()