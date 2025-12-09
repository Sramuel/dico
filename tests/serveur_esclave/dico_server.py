#!/usr/bin/python3

import select
import sys
from dico_protocol import *

admin_user={"admin":"admin"} #tableau des user admin (avec username:password)

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l=[] #liste sockets clients
admins=[] #liste des sockets clients admins connectés

try: #crée le serveur et ouvre les connexion
    master = False
    hostmaster = None
    portmaster = None
    port = int(sys.argv[1])
    if len(sys.argv)>4:
        if (sys.argv[2]== "master"):
            hostmaster=sys.argv[3]
            portmaster=sys.argv[4]
            master=True
            print(f"Lancement en mode esclave, maître: {hostmaster}:{portmaster}") #print pour debug entre maître et esclave
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
                if s in l: 
                    l.remove(s) #on retire la socket client qui nous a envoyé des données une fois la connexion fermé
                if s in admins: 
                    admins.remove(s) #on le retire des admins s'il part
                s.close()
            else:
                cmdarg = parse_request(data)
                admin = (s in admins)
                if cmdarg != None: #sécurité si message vide ou malformé
                    dicoarg = cmdarg[0] #réception du nom du fichier dico envoyé par le client
                    if dicoarg == "dico_admin.py": #si dicoarg est dico_admin.py, c'est une tentative de login admin
                        login = cmdarg[1]
                        password = cmdarg[2]
                        if login in admin_user and password == admin_user[login]: #vérification des identifiants
                            admins.append(s) #on ajoute la socket à la liste des admins connectés
                            s.sendall("Nice ! You are logged in !!!".encode("utf-8"))
                        else :
                            s.sendall("Wrong login or password".encode("utf-8"))
                        continue #on a passer l'étape de l'authentification, on passe à la prochaine itération

                    else:
                        command = cmdarg[1] #réception de la commande envoyé par le client
                        dico = load_dico(f"data/{dicoarg}")

                    
                    if command == 'get' and not admin:
                        command_get(cmdarg[2], dico, s, master, hostmaster, portmaster, data) #appel de la commande get

                    elif command == 'pref' and not admin:
                        command_pref(cmdarg[2], dico, s, master, hostmaster, portmaster, data) #appel de la commande pref

                    elif command == 'set' and admin:
                        command_set(cmdarg[2], dico, dicoarg, s) #appel de la commande set

                    elif command == 'del' and admin:
                        command_del(cmdarg[2], dico, dicoarg, s) #appel de la commande del


                    else:
                        s.sendall(f"Unknown command: {command}".encode("utf-8"))
                else:
                    s.sendall("Malformed request".encode("utf-8"))
ss.close()