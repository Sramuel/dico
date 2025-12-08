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

def command_get(key, dico, s):
    if key in dico:
        print(f"Clé trouvée localement: {key}") #print pour debug entre maître et esclave
        s.sendall(f"{dico[key]}".encode("utf-8"))
    else:
        s.sendall("Key not found".encode("utf-8"))

def command_pref(prefix, dico, s):
    char="" #chaîne de caractère qui contiendra le dico des préfixes (dico_pref) pour l'envoyer au client
    found = False
    for k, v in dico.items():
        if k.startswith(prefix):
            char+=(f"\"{k}\": \"{v}\" ")
            found = True
    if found: #si on a trouvé au moins un préfixe alors on envoie la liste des clés:valeurs associées au préfixe
        print(f"Préfixe trouvé localement: {prefix}") #print pour debug entre maître et esclave
        s.sendall(char.encode("utf-8"))
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

def command_with_master(key, dico, hostmaster, portmaster, data, s):
    sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sm.connect((hostmaster, int(portmaster)))
    print("J'ai pas trouvé donc je demande au maitre") #print pour debug entre maître et esclave
    sm.sendall(data) #on transfère la requête brute
    s.sendall(sm.recv(1500)) #on renvoie la réponse du maître au client
    sm.close()