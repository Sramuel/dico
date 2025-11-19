#!/usr/bin/python3

import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 4:
    print("Usage: dico_client.py <server> <port> <command> <arg>")
    s.close()
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host, port))
command = sys.argv[3]
if command == "get" or command == "pref" :
    arg = sys.argv[4]
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
data=(command+" "+arg).encode()
s.sendall(data)
print((s.recv(1500)).decode("utf-8"))
s.close()