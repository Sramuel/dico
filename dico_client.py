#!/usr/bin/python3

import socket
import sys
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
host = ""
port = 7777
s.connect((host, port))
while True:
    data = sys.stdin.readline()
    cmdarg=data.split(" ",1)
    if len(cmdarg) < 2:
        print("Usage: <command>")
        print("Commands:")
        print("get <key> : Récupère la valeur associée à la clé. Affiche 'Key not found' si la clé n'existe pas.")
        print("set <key> <value> : Définit la valeur associée à la clé.")
        print("del <key> : Supprime la clé du dictionnaire. Affiche 'Key not found' si la clé n'existe pas.")
        print("pref <prefix> : Affiche toutes les couples clé-valeur dont la clé commence par le préfixe donné.")
        s.close()
    buffer = data.encode("utf-8")
    s.sendall(buffer)
    print((s.recv(1500)).decode("utf-8"))
    break
s.close()