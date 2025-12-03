#!/usr/bin/python3

import socket
import select
import sys

from dico_local import *
from dico_protocol import parse_request

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l=[] #liste sockets clients
try: #crée le serveur et ouvre les connexion
    master = False
    port = int(sys.argv[1])
    if len(sys.argv)>4:
        if (sys.argv[2]== "master"):
            hostmaster=sys.argv[3]
            portmaster=sys.argv[4]
            master=True
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #évite le Adress already in use
    ss.bind(("",port))
    ss.listen(1)

except Exception as e: #si erreur pour créer le serveur
    print("socket error!", e)
    sys.exit(1)
while True: #on reçoit les données envoyé par le client
    rlist,_,_=select.select(l+[ss],[],[]) #rlist contient les sockets disponible en lecture
    for s in rlist:
        if s ==ss: #si c’est la socket "serveur", c’est qu’un client vient de se connecter
            conn, addr = ss.accept()
            l.append(conn) #on ajoute la socket client
        else : #le client de cette socket nous a envoyé des donnée
            data = s.recv(1500)
            if not data:
                l.remove(s) #on retire la socket client qui nous a envoyé des données une fois la connexion fermé
                s.close()
            else:
                cmdarg = parse_request(data)
                if cmdarg != None: #sécurité si message vide ou malformé
                    dicoarg = cmdarg[0] #réception du nom du fichier dico envoyé par le client
                    command = cmdarg[1] #réception de la commande envoyé par le client
                    dico = load_dico(f"data/{dicoarg}")

                    
                    if command == 'get':
                        key = cmdarg[2] #réception de la clé du dictionnaire envoyé dans les arguments par le client
                        if key in dico:
                            s.sendall(f"{dico[key]}".encode("utf-8"))
                        elif master: #pas trouvé localement, mais on a un maitre
                            sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sm.connect((hostmaster, int(portmaster)))
                            sm.sendall(data) #on transfère la requête brute
                            s.sendall(sm.recv(1500)) #on renvoie la réponse du maître au client
                            sm.close()
                        else:
                            s.sendall("Key not found".encode("utf-8"))

                    
                    elif command == 'pref':
                        char="" #chaîne de caractère qui contiendra le dico des préfixes (dico_pref) pour l'envoyer au client
                        dico_pref = {} #création du dico des préfixes valides
                        cpt=0 #nombre de lettres dans le préfixe envoyé par le client
                        pref_key = cmdarg[2] #on reçoit le prefixe de la clé envoyé par le clint
                        len_p = len(pref_key)
                        for key in dico: #on parcourt tout le dictionnaire
                            i = 0
                            while i<len(key) and i<len_p : #on vérifie si le préfixe est valide en taille par rapport à la clé
                                if pref_key[i] == key[i]: #si la lettre correspond, on regarde la suivante
                                    cpt+=1
                                i+=1 
                            if cpt == len_p: #si toutes les lettres correspondent à un préfixe valide, alors on le met dans le dico des préfixes
                                dico_pref[key]=dico[key]
                            cpt=0
                        for key in dico_pref: #on parcourt tous les préfixes valides du dico_pref pour les mettre dans une seule chaîne de caractères pour l'envoyer au client
                            char+=(f"\"{key}\": \"{dico_pref[key]}\" ")
                        if char != "": #si le dico des préfixes n'est pas vide alors on envoie la liste des clés:valeurs associées au préfixe
                            s.sendall(char.encode("utf-8"))
                        elif master: #pas trouvé localement, on demande au maître
                            sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sm.connect((hostmaster, int(portmaster)))
                            sm.sendall(data)
                            s.sendall(sm.recv(1500))
                            sm.close()
                        else:
                            s.sendall("Prefix not found".encode("utf-8"))

                        
                    else:
                        s.sendall(f"Unknown command: {command}".encode("utf-8"))
                else:
                    s.sendall("Malformed request".encode("utf-8"))
ss.close()