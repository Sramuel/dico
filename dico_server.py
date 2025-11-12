#!/usr/bin/python3

import socket
from typing import Dict
import sys
import os
import json
import select

def load_dico(dico_file: str) -> Dict[str, str]:
    """Load JSON dictionary from file, return empty dict on missing/invalid file."""
    if not os.path.exists(dico_file):
        return {}
    with open(dico_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Ensure the loaded object is a dict; otherwise return empty dict
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            return {}


def save_dico(dico_file: str, dico: Dict[str, str]) -> None:
    with open(dico_file, 'w', encoding='utf-8') as f:
        json.dump(dico, f, ensure_ascii=False, indent=2)

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
                buffer = data.decode("utf-8").strip()
                cmdarg=buffer.split(" ",1)
                command = cmdarg[0]
                dico: Dict[str, str] = load_dico("data/mois_duree.json")
                if command == 'get':
                    key: str = cmdarg[1]
                    if key in dico:
                        s.sendall(f"{dico[key]}".encode("utf-8"))
                        l.remove(s)
                        s.close()
                    else:
                        s.sendall("Key not found".encode("utf-8"))
                        l.remove(s)
                        s.close()
                else:
                    s.sendall(f"Unknown command: {command}".encode("utf-8"))
                    l.remove(s)
                    s.close()
ss.close()