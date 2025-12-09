#!/usr/bin/env python3

import socket
from dico_local import *

def format_request(dico, command, arg): #prépare le message pour l'envoi (client -> serveur)
    msg = f"{dico} {command} {arg}"
    return msg.encode("utf-8")

def parse_request(data): #découpe le message reçu (serveur <- client)
    try:
        text = data.decode("utf-8").strip()
        parts = text.split(" ", 2) #on divise en 3 parties max (pour gérer les espaces dans l'argument)
        if len(parts) < 3:
            return None
        return parts #retourne [dico, command, arg]
    except:
        return None

def command_get(key, dico, s, master, hostmaster, portmaster, data):
    if key in dico: 
        print(f"Clé trouvée localement: {key}") 
        s.sendall(dico[key].encode("utf-8")) #on renvoie la valeur associée à la clé envoyée par le client
    elif master and hostmaster and portmaster: #on verifie que le master, son adresse et son port d'écoute son bien définis
        # on contacte le maître
        sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Clé non trouvée, je demande au maître")
        sm.connect((hostmaster, int(portmaster)))
        sm.sendall(data)
        s.sendall(sm.recv(1500))
        sm.close()
    else:
        s.sendall("Key not found".encode("utf-8"))

def command_pref(prefix, dico, s, master, hostmaster, portmaster, data):
    char = ""
    found = False
    for k, v in dico.items():
        if k.startswith(prefix):
            char += f"\"{k}\": \"{v}\" "
            found = True
    if found:
        print(f"Préfixe trouvé localement: {prefix}")
        s.sendall(char.encode("utf-8")) #on renvoie la ou les valeurs associées à la clé envoyée par le client
    elif master and hostmaster and portmaster: #on verifie que le master, son adresse et son port d'écoute son bien définis
        sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Préfixe non trouvé, je demande au maître")
        sm.connect((hostmaster, int(portmaster)))
        sm.sendall(data)
        s.sendall(sm.recv(1500))
        sm.close()
    else:
        s.sendall("Prefix not found".encode("utf-8"))

def command_set(cmdarg, dico, dicoarg, s):
    try:
        args_set = cmdarg.split("|", 1) # On sépare la clé de la valeur
        key = args_set[0]
        value = args_set[1]
        dico[key] = value
        save_dico(f"data/{dicoarg}", dico) #on sauvegarde le dico modifié
        s.sendall(f"Set {key} = {value}".encode("utf-8"))
    except:
        s.sendall("Error in set arguments".encode("utf-8"))
                        
def command_del(key, dico, dicoarg, s):
    if key in dico:
        del dico[key] #on supprime la clé du dico
        save_dico(f"data/{dicoarg}", dico)
        s.sendall(f"Deleted {key}".encode("utf-8"))
    else:
        s.sendall("Key not found".encode("utf-8"))
